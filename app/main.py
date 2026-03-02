from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import engine, Base
import app.routes as routes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FitBuddy AI")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(routes.router)
