import jwt
from ..config import config
from ..database import conn
import time

cache = {"jwt": set([]), "refresh_token": set([])}

def error(code: int, message: str):
    return {"code": code, "message": message}

def check_token(token, type):
    # Try to decode header
    try:
        claims = jwt.decode(token, config["auth"][type]["secret"], algorithms=["HS256"])
    except:
        return None

    cur = conn.cursor()

    token_blacklisted = None

    # Try to find header in cache
    if token in cache[type]:
        token_blacklisted = True

    # If it's not in cache, search in the database
    if token_blacklisted is None:
        cur.execute("SELECT token, expiration FROM user_blacklist WHERE type = %s AND token = %s", (type, token))
        token_blacklisted = cur.fetchone() is not None
        if token_blacklisted:
            cache[type].add(token)

    # If it's blacklisted, return None
    if token_blacklisted:
        # If it's expired, remove from cache/database
        if claims["exp"] > int(time.time()):
            cur.execute("DELETE FROM user_blacklist WHERE type = %s AND token = %s", (type, token))
            cache[type].remove(token)
            conn.commit()
        cur.close()
        return None

    # If it's expired, return None
    if claims["exp"] < int(time.time()):
        cur.close()
        print("now: " + str(int(time.time())) + ", then:" + str(claims["exp"]))
        return None

    cur.close()

    return claims

def check_jwt(header):
    # If header is empty return None
    if header is None or header[:7] != "Bearer ":
        return None

    token = header[7:]

    return check_token(token, "jwt")

def check_refresh_token(header):
    if header is None:
        return None
    return check_token(header, "refresh_token")
