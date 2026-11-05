import json
from pathlib import Path


PASSWORDS_DIRECTORY = Path(__file__).resolve().parents[2] / "saved_passwords"
PASSWORDS_FILE = PASSWORDS_DIRECTORY / "passwords.txt"


def save_password(app_or_site: str, password: str) -> Path:
    name = app_or_site.strip()
    if not name:
        raise ValueError("Enter the app or site name.")
    if not password:
        raise ValueError("Generate or enter a password before saving.")

    PASSWORDS_DIRECTORY.mkdir(parents=True, exist_ok=True)
    record = json.dumps(
        {"app_or_site": name, "password": password},
        ensure_ascii=False,
    )
    with PASSWORDS_FILE.open("a", encoding="utf-8", newline="\n") as file:
        file.write(record + "\n")
    return PASSWORDS_FILE
