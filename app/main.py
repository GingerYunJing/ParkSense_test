from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import connect_to_mongo, close_mongo_connection
from app.routes.user import router as user_router
from app.routes.camera import router as camera_router
from app.routes.zone import router as zone_router
from app.routes.parking_space import router as parking_space_router
from app.routes.violation import router as violation_router
from app.routes.vehicle import router as vehicle_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix="/auth", tags=["auth"])
app.include_router(camera_router, tags=["cameras"])
app.include_router(zone_router, tags=["zones"])
app.include_router(parking_space_router, tags=["parking_spaces"])
app.include_router(violation_router, tags=["violations"])
app.include_router(vehicle_router, tags=["vehicles"])

@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

@app.get("/health")
async def health_check():
    return {"status": "ok"} 


import logging

logging.basicConfig(
    level=logging.INFO,
    format="INFO:     %(message)s",
)
