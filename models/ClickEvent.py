from datetime import datetime

from sqlmodel import Field, SQLModel


class ClickEvent(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_agent: str | None = Field()
    referrer: str | None = Field()
    ip: str = Field()
    created_at: datetime = Field(default_factory=datetime.now)

    url_id: int = Field(default=None, foreign_key='url.id')

