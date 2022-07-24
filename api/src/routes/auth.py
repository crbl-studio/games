from fastapi import APIRouter, Response, status, Header
from pydantic import BaseModel
from ..database import conn
from ..config import config
import bcrypt
import jwt
import re
import time

router = APIRouter()

jwt_key = config["auth"]["jwt"]["secret"]
refresh_token_key = config["auth"]["refresh_token"]["secret"]


class RegisterUserDto(BaseModel):
    name: str
    password: str
    email: str


class ConfirmEmailDto(BaseModel):
    token: str


class LoginDto(BaseModel):
    email: str | None;
    name: str | None;
    password: str;


class ChangeNameDto(BaseModel):
    name: str

# Example route
@router.get("/")
async def root():
    return {"message": "Hello World"}


# https://crbl-studio.github.io/games/auth/api.html#post-to-user
@router.post("/user")
async def register(user: RegisterUserDto, response: Response):
    cur = conn.cursor()

    # Check if the password is secure
    if len(user.password) < 8 or re.search(
            '[0-9]', user.password) is None or re.search(
                '[a-z]', user.password) is None or re.search(
                    '[A-Z]', user.password) is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"code": 3, "message": "password is considered insecure"}

    # Check if the username is valid
    if re.search("^[a-zA-Z0-9_-]*$", user.name) is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"code": 4, "message": "name contains invalid characters"}

    # Check if the username is already used
    cur.execute(
        "SELECT * FROM temp_users WHERE name = %s UNION SELECT * FROM temp_users WHERE name = %s",
        (user.name, user.name))
    existing_user = cur.fetchone()
    if existing_user:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"code": 1, "message": "name is already used"}

    # Check if the email is already used
    cur.execute(
        "SELECT * FROM temp_users WHERE email = %s UNION SELECT * FROM temp_users WHERE email = %s",
        (user.email, user.email))
    existing_user = cur.fetchone()
    if existing_user:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"code": 2, "message": "email is already used"}

    # Insert the user into the temporary table
    password_bytes = user.password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
    cur.execute(
        "INSERT INTO temp_users (name, email, password_hash) VALUES (%s, %s, %s)",
        (user.name, user.email, hash))
    conn.commit()
    cur.close()

# https://crbl-studio.github.io/games/auth/api.html#post-to-useremail
# This is an dev version, which allows email confirmation
# without actually sending an email
@router.post("/user/email")
async def confirm_email(data: ConfirmEmailDto):
    cur = conn.cursor()
    cur.execute("SELECT name, email, password_hash FROM temp_users WHERE email = %s", (data.token,))
    result = cur.fetchone()
    if result is None:
        return {"code": 1, "message": "invalid token"}
    name, email, password_hash = result
    cur.execute("DELETE FROM temp_users WHERE email = %s", (email,))
    cur.execute("INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)", (name, email, password_hash))
    conn.commit()
    return None

# https://crbl-studio.github.io/games/auth/api.html#post-to-userlogin
@router.put("/user/login")
async def login(data: LoginDto):
    cur = conn.cursor()
    if data.email is None and data.name is None:
        return {"code": 1, "message": "both email and name are null"}
    if data.email is not None and data.name is not None:
        return {"code": 2, "message": "both email and name are provided"}
    if data.email is not None:
        cur.execute("SELECT id, password_hash FROM users WHERE email = %s", (data.email,))
        result = cur.fetchone()
        if result is None:
            return {"code": 3, "mesasge": "no user found with this combination"}
    else:
        cur.execute("SELECT id, password_hash FROM users WHERE name = %s", (data.name,))
        result = cur.fetchone()
        if result is None:
            return {"code": 3, "mesasge": "no user found with this combination"}
    user_id, password_hash = result
    if bcrypt.checkpw(data.password.encode('utf-8'), password_hash.encode('utf-8')):
        jwt_token = jwt.encode({"sub": user_id, "exp": int(time.time()) + config["auth"]["jwt"]["duration"]}, jwt_key, algorithm="HS256")
        refresh_token = jwt.encode({"sub": user_id, "exp": int(time.time()) + config["auth"]["refresh_token"]["duration"]}, refresh_token_key, algorithm="HS256")
        return {"data": {"jwt": jwt_token, "refreshToken": refresh_token}}
    else:
        return {"code": 3, "mesasge": "no user found with this combination"}

@router.post("/user/name")
async def change_name(data: ChangeNameDto, response: Response, authorization: str | None = Header(default=None)):
    if authorization is None or authorization[:7] != "Bearer ":
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return
    try:
        decoded = jwt.decode(authorization[7:], jwt_key, algorithms=["HS256"])
    except:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return

    if decoded["exp"] > int(time.time()):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return

    if re.search("^[a-zA-Z0-9_-]*$", data.name) is None:
        return {"code": 2, "message": "name contains invalid characters"}

    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM temp_users WHERE name = %s UNION SELECT * FROM temp_users WHERE name = %s",
        (data.name, data.name))
    existing_user = cur.fetchone()
    if existing_user is not None:
        return {"code": 1, "message": "name is already used"}

    cur.execute("UPDATE users SET name = %s WHERE id = %s", (data.name, decoded["sub"]))
    conn.commit()
    cur.close()
