from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


def parse_time(time_text: str):
    time_text = time_text.strip().upper()

    for fmt in ("%I:%M %p", "%I %p"):
        try:
            return datetime.strptime(
                time_text,
                fmt
            ).time()
        except ValueError:
            pass

    raise ValueError(f"Invalid time: {time_text}")


def resolve_date(date_text: str | None):
    today = datetime.now(
        ZoneInfo("Asia/Kolkata")
    ).date()

    if not date_text:
        return today

    value = date_text.strip().lower()

    if value == "today":
        return today

    if value == "tomorrow":
        return today + timedelta(days=1)

    # For an already normalized date
    return datetime.strptime(
        value,
        "%Y-%m-%d"
    ).date()


def make_datetime(date_text, time_text):
    selected_date = resolve_date(date_text)
    selected_time = parse_time(time_text)

    result = datetime.combine(
        selected_date,
        selected_time
    )

    return result.strftime("%Y-%m-%dT%H:%M:%S")