from datetime import datetime

from sqlmodel import Field, SQLModel


class Url(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    original_url: str = Field(index=True)
    short_code: str = Field(index=True)
    tracking_token: str | None = Field()
    click_count: int = Field(default=0, nullable=True)
    created_at: datetime = Field(default_factory=datetime.now)

    user_id: int | None = Field(default=None, foreign_key="user.id")
