from datetime import datetime, timedelta, timezone

import jwt

from setting import SECRET_KEY


def verify_token(access_token):
    try:
        # get token data:
        jwt.decode(access_token, SECRET_KEY, algorithms=["HS256"])
        # if we run ↑this↑ after 2 minutes
        # jwt.exceptions.ExpiredSignatureError: Signature has expired will
        # be raised in other case we will get decoded data:
    except jwt.ExpiredSignatureError:
        raise Exception("JWT expired")

    return True


def generate_access_token(user_id, username, email):
    payload = {"user_id": user_id, "username": username, "email": email}

    # add token expiration time (2 minutes):
    payload["exp"] = datetime.now(tz=timezone.utc) + timedelta(minutes=2)

    # this token is valid for 2 minutes
    access_token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return access_token


def generate_new_token(expired_token):
    decoded_payload = jwt.decode(
        expired_token,
        SECRET_KEY,
        algorithms=["HS256"],
        options={'verify_exp': False},
    )

    # now we should update 'exp' for 2 minutes again
    decoded_payload['exp'] = \
        datetime.now(tz=timezone.utc) + timedelta(minutes=2)

    # and generate new token
    new_token = jwt.encode(decoded_payload, SECRET_KEY, algorithm="HS256")
    # after receiving this new token client will be able to use it for
    # 2 minutes before another refreshing process

    return new_token

