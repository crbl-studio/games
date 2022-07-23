from fastapi import APIRouter, Response, status
from pydantic import BaseModel
from ..database import conn
import bcrypt
import re

router = APIRouter()


class RegisterUserDto(BaseModel):
    name: str
    password: str
    email: str


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
    hash = bcrypt.hashpw(password_bytes, salt)
    cur.execute(
        "INSERT INTO temp_users (name, email, password_hash) VALUES (%s, %s, %s)",
        (user.name, user.email, hash))
    conn.commit()
    cur.close()
