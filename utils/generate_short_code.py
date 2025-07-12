import secrets
import string
from models.Url import Url
from sqlalchemy import select
from db.session import SessionDep

def generate_short_code(db: SessionDep, length: int = 8, max_attempts: int = 5) -> str:
    chars = string.ascii_letters + string.digits
    for _ in range(max_attempts):
        short_code = "".join(secrets.choice(chars) for _ in range(length))
        stmt = select(Url).where(Url.short_code == short_code)
        exists = db.scalars(stmt).first()
        if not exists:
            return short_code
    raise Exception("Failed to generate unique short code")
