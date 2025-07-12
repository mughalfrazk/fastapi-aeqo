from fastapi import APIRouter
from pydantic import BaseModel, AnyHttpUrl
from uuid import uuid4
from models.Url import Url
from sqlalchemy import select
from db.session import SessionDep
from utils.generate_short_code import generate_short_code

router = APIRouter(prefix="/url", tags=["Url"])


class UrlShortenRequest(BaseModel):
    original_url: AnyHttpUrl


@router.post("/shorten")
def url_shorten(req: UrlShortenRequest, db: SessionDep):

    # TODO: Add <user_id> in request
    # TODO: If the <user_id> is not present, utilise <tracking_token>

    original_url = str(req.original_url)

    stmt = select(Url).where(Url.original_url == original_url)
    existing = db.scalars(stmt).first()
    if existing:
        return existing

    short_code = generate_short_code(db)

    new_url = Url(
        original_text=req.original_url, tracking_token=uuid4(), short_code=short_code
    )

    return new_url
