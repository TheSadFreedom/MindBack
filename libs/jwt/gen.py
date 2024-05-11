from jwt import encode as jwt_encode

from ..http.time import generate_utc_expiration_date


def generate_token(
    id: str | bytes, key: str | bytes, algorithm: str, validity_period_in_days: float
) -> str:
    expiration_date = generate_utc_expiration_date(validity_period_in_days)

    return jwt_encode(
        payload={"id": id, "exp": expiration_date},
        key=key,
        algorithm=algorithm,
    )
