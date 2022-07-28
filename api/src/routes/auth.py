from fastapi import APIRouter, Response, status, Header, HTTPException
from pydantic import BaseModel
from ..database import conn
from ..config import config
from .util import error, check_jwt, check_refresh_token
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
    email: str | None
    name: str | None
    password: str


class ChangeNameDto(BaseModel):
    name: str


class ChangeEmailDto(BaseModel):
    email: str


def check_name(name):
    return re.search("^[a-zA-Z0-9_-]*$", name) is not None


def check_password(password: str):
    return len(password) > 8 and re.search(
        '[0-9]', password) is not None and re.search(
            '[a-z]', password) is not None and re.search('[A-Z]',
                                                         password) is not None

def generate_jwt(user_id):
    return jwt.encode(
        {
            "sub": user_id,
            "type": "jwt",
            "exp": int(time.time()) + config["auth"]["jwt"]["duration"]
        },
        jwt_key,
        algorithm="HS256")

def generate_refresh_token(user_id):
    return jwt.encode(
        {
            "sub":
            user_id,
            "type":
            "refresh_token",
            "exp":
            int(time.time()) + config["auth"]["refresh_token"]["duration"]
        },
        refresh_token_key,
        algorithm="HS256")


# Example route
@router.get("/")
async def root():
    return {"message": "Hello World"}


# https://crbl-studio.github.io/games/auth/api.html#post-to-user
@router.post("/user")
async def register(user: RegisterUserDto):
    cur = conn.cursor()

    # Check if the password is secure
    if not check_password(user.password):
        return error(3, "password is considered insecure")

    # Check if the username is valid
    if not check_name(user.name):
        return error(4, "name contains invalid characters")

    # Check if the username is already used
    cur.execute(
        """
        SELECT * FROM temp_users
        WHERE name = %s
        UNION
        SELECT * FROM temp_users
        WHERE name = %s
        """, (user.name, user.name))
    existing_user = cur.fetchone()
    if existing_user:
        return error(1, "name is already used")

    # Check if the email is already used
    cur.execute(
        """
        SELECT * FROM temp_users
        WHERE email = %s
        UNION
        SELECT * FROM temp_users
        WHERE email = %s
        """, (user.email, user.email))
    existing_user = cur.fetchone()
    if existing_user:
        return error(2, "email is already used")

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
# without actually sending an email.
@router.post("/user/email")
async def confirm_email(data: ConfirmEmailDto):
    cur = conn.cursor()
    cur.execute(
        "SELECT name, email, password_hash FROM temp_users WHERE email = %s",
        (data.token, ))
    result = cur.fetchone()
    if result is None:
        return error(1, "invalid token")
    name, email, password_hash = result
    cur.execute("DELETE FROM temp_users WHERE email = %s", (email, ))
    cur.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)",
        (name, email, password_hash))
    conn.commit()
    return None


# https://crbl-studio.github.io/games/auth/api.html#post-to-userlogin
@router.put("/user/login")
async def login(data: LoginDto):
    cur = conn.cursor()
    if data.email is None and data.name is None:
        return error(1, "both email and name are null")
    if data.email is not None and data.name is not None:
        return error(2, "both email and name are provided")
    if data.email is not None:
        cur.execute("SELECT id, password_hash FROM users WHERE email = %s",
                    (data.email, ))
        result = cur.fetchone()
        if result is None:
            return error(3, "no user found with this combination")
    else:
        cur.execute("SELECT id, password_hash FROM users WHERE name = %s",
                    (data.name, ))
        result = cur.fetchone()
        if result is None:
            return error(3, "no user found with this combination")
    user_id, password_hash = result
    if bcrypt.checkpw(data.password.encode('utf-8'),
                      password_hash.encode('utf-8')):
        return {"data": {"jwt": generate_jwt(user_id), "refreshToken": generate_refresh_token(user_id)}}
    else:
        return error(3, "no user found with this combination")


# https://crbl-studio.github.io/games/auth/api.html#put-to-username
@router.put("/user/name")
async def change_name(data: ChangeNameDto,
                      authorization: str | None = Header(default=None)):
    claims = check_jwt(authorization)
    if claims is None:
        raise HTTPException(status_code=401, detail="No jwt was provided or the jwt is invalid.")

    if not check_name(data.name):
        return error(2, "name contains invalid characters")

    cur = conn.cursor()
    cur.execute(
        """
        SELECT * FROM temp_users
        WHERE name = %s
        UNION
        SELECT * FROM users
        WHERE name = %s
        """, (data.name, data.name))
    existing_user = cur.fetchone()
    if existing_user is not None:
        return error(1, "name is already used")

    cur.execute("UPDATE users SET name = %s WHERE id = %s",
                (data.name, claims["sub"]))
    conn.commit()
    cur.close()

# https://crbl-studio.github.io/games/auth/api.html#put-to-useremail
# This is an dev version, which allows changing email
# without actually sending an email. In the future,
# this should send an email to the old and new email
# in order to confirm the change.
@router.put("/user/email")
async def change_email(data: ChangeEmailDto,
                      authorization: str | None = Header(default=None)):
    claims = check_jwt(authorization)
    if claims["sub"] is None:
        raise HTTPException(status_code=401, detail="No jwt was provided or the jwt is invalid.")

    cur = conn.cursor()
    cur.execute(
        """
        SELECT * FROM temp_users
        WHERE email = %s
        UNION
        SELECT * FROM users
        WHERE email = %s
        """, (data.email, data.email))
    existing_user = cur.fetchone()
    if existing_user is not None:
        return error(1, "email is already used")

    cur.execute("UPDATE users SET email = %s WHERE id = %s",
                (data.email, claims["sub"]))
    conn.commit()
    cur.close()

# https://crbl-studio.github.io/games/auth/api.html#post-to-userlogout
@router.post("/user/logout")
async def logout(authorization: str | None = Header(default=None), x_refresh_token: str | None = Header(default=None)):
    cur = conn.cursor()
    if authorization is not None:
        claims = check_jwt(authorization)
        cur.execute("INSERT INTO user_blacklist VALUES (%s, 'jwt', %s)", (authorization, claims["exp"]))
    if x_refresh_token is not None:
        refresh = check_refresh_token(authorization)
        cur.execute("INSERT INTO user_blacklist VALUES (%s, 'refresh', %s)", (x_refresh_token, claims["exp"]))
    conn.commit()
    cur.close()

# https://crbl-studio.github.io/games/auth/api.html#post-to-userrefresh
@router.post("/user/refresh")
async def refresh(x_refresh_token: str | None = Header(default=None)):
    cur = conn.cursor()
    if x_refresh_token is not None:
        refresh = check_refresh_token(x_refresh_token)
        if refresh is None or refresh["exp"] < int(time.time()):
            raise HTTPException(status_code=401, detail="No refresh token was provided or the refresh token is invalid.")
        return {"data": {"jwt": generate_jwt(refresh["sub"]), "refreshToken": generate_refresh_token(refresh["sub"])}}
    else:
        raise HTTPException(status_code=401, detail="No refresh token was provided or the refresh token is invalid.")
