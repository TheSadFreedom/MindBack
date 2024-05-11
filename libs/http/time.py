from datetime import datetime, timedelta, timezone


def utc_now() -> datetime:
    return datetime.now(tz=timezone.utc)


def generate_utc_expiration_date(validity_period_in_days: float) -> datetime:
    return utc_now() + generate_max_age(validity_period_in_days)


def generate_max_age(validity_period_in_days: float):
    return timedelta(days=validity_period_in_days)
