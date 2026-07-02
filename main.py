from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine

from models.user import User
from models.visitor import Visitor
from models.visit import Visit

from routes.auth import router as auth_router
from routes.visitors import router as visitors_router
from routes.visits import router as visits_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Visitor Management System"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth_router)
app.include_router(visitors_router)
app.include_router(visits_router)


@app.get("/")
def home():

    return {
        "message":
        "Visitor Management System"
    }
