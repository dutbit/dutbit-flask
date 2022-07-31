from datetime import datetime, timedelta, timezone

from flask import current_app

import jwt


def create_token(payload):
    payload["exp"] = datetime.now(timezone.utc) + timedelta(seconds=3600)
    token = jwt.encode(payload, key=current_app.config["JWT_KEY"], algorithm="HS512")
    current_app.logger.info(f"user: {token}")
    return token


def load_token(token):
    try:
        payload = jwt.decode(token, key=current_app.config["JWT_KEY"], algorithms=["HS512"])
        current_app.logger.info(f"payload: {payload}")
        return payload
    except jwt.ExpiredSignatureError:  # 'token已失效'
        return "ExpiredSignature"
    except jwt.DecodeError:  # 'token认证失败'
        return None
    except jwt.InvalidTokenError:  # '非法的token'
        return None
