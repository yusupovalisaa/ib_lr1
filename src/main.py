from contextlib import asynccontextmanager
from fastapi import FastAPI

from .database import Base, engine, SessionLocal
from .models import User
from .security import hash_password
from .routers import auth, data


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if not db.query(User).filter(User.username == "admin").first():
            db.add(User(username="admin", hashed_password=hash_password("admin123")))
            db.commit()
    finally:
        db.close()
    yield


app = FastAPI(title="MyProject API", version="0.1.0", lifespan=lifespan)
app.include_router(auth.router)
app.include_router(data.router)


@app.get("/health", tags=["meta"])
def health():
    return {"status": "ok"}