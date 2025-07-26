from fastapi import APIRouter, HTTPException, status, Depends, Query
from app.models.user import UserCreate, User, UserInDB, UserUpdate
from app.db import get_database
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import os
from typing import Optional, List
from app.auth import get_current_admin_user
from bson import ObjectId
from fastapi import Body

router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY", "secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/register", response_model=User)
async def register(user: UserCreate):
    db = get_database()
    existing = await db["users"].find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    user_doc = {
        "email": user.email,
        "hashed_password": hashed_password,
        "roles": ["public_user"],
        "is_active": True,
        "mfa_enabled": False,
        "created_at": datetime.utcnow(),
        "updated_at": None
    }
    result = await db["users"].insert_one(user_doc)
    user_doc["_id"] = str(result.inserted_id)
    return User(**user_doc)

@router.post("/login")
async def login(user: UserCreate):
    db = get_database()
    user_doc = await db["users"].find_one({"email": user.email})
    if not user_doc or not verify_password(user.password, user_doc["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({
        "sub": str(user_doc["_id"]),
        "roles": user_doc["roles"],
        "email": user_doc["email"]
    })
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users", dependencies=[Depends(get_current_admin_user)])
async def list_users(
    skip: int = 0,
    limit: int = 10,
    email: Optional[str] = None,
    sort_by: str = "created_at",
    order: int = -1
):
    db = get_database()
    query = {}
    if email:
        query["email"] = email
    total = await db["users"].count_documents(query)
    users = []
    cursor = db["users"].find(query).sort(sort_by, order).skip(skip).limit(limit)
    async for u in cursor:
        u["_id"] = str(u["_id"])
        users.append(User(**u))
    return {"items": users, "total": total}

@router.patch("/users/{user_id}", dependencies=[Depends(get_current_admin_user)])
async def update_user(
    user_id: str,
    user_update: UserUpdate = Body(..., title="User Update Data")
):
    db = get_database()
    update = {"updated_at": datetime.utcnow()}
    if user_update.roles is not None:
        update["roles"] = user_update.roles
    if user_update.is_active is not None:
        update["is_active"] = user_update.is_active
    if user_update.mfa_enabled is not None:
        update["mfa_enabled"] = user_update.mfa_enabled
    result = await db["users"].update_one({"_id": ObjectId(user_id)}, {"$set": update})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    user = await db["users"].find_one({"_id": ObjectId(user_id)})
    user["_id"] = str(user["_id"])
    return User(**user) 