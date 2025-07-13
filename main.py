from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from sqlmodel import SQLModel
from sqlalchemy import select
from db.session import engine, SessionDep
from routers import url
from models.Url import Url
from models.ClickEvent import ClickEvent

app = FastAPI()
SQLModel.metadata.create_all(engine)

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/u/{short_code}", status_code=301)
def go_to_original_url(short_code: str, req: Request, db: SessionDep):
    # STEP 01: Check if the short_code is present.
    stmt = select(Url).where(Url.short_code == short_code)
    existing = db.scalars(stmt).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Invalid url")

    # STEP 02: Get IP, referrer and user_agent from the request.
    ip = req.client.host
    user_agent = req.headers["user-agent"]
    referrer = req.headers.get("referrer")

    # STEP 03: Save click event.
    new_click_event = ClickEvent(ip=ip, user_agent=user_agent, referrer=referrer, url_id=existing.id)
    db.add(new_click_event)
    db.commit()

    # TODO: Update click_count in the url table

    # STEP 04: Get the original_url and return with 301.
    return RedirectResponse(url=existing.original_url)

app.include_router(url.router)
