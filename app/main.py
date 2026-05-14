from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from app.database import engine, Base, get_db
from app.services import (
    load_users_to_db,
    get_paginated_users,
    get_user_by_id,
    get_random_user,
    is_db_empty,
    count_users,
)
from app.schemas import LoadRequest

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

templates = Jinja2Templates(directory="app/templates")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up...")
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async for db in get_db():
        empty = await is_db_empty(db)
        if empty:
            logger.info("Database is empty. Loading 1000 users...")
            try:
                added = await load_users_to_db(db, 1000)
                logger.info(f"Loaded {added} users")
            except Exception as e:
                logger.error(f"Load failed: {e}")
        else:
            total = await count_users(db)
            logger.info(f"Database has {total} users")
        
        total = await count_users(db)
        logger.info("=" * 50)
        logger.info("SERVER IS READY TO USE")
        logger.info(f"Total users in database: {total}")
        logger.info(f"Open http://localhost:8000")
        logger.info("=" * 50)
        break
    
    yield
    logger.info("Shutting down...")

app = FastAPI(lifespan=lifespan)

@app.get("/", response_class=HTMLResponse)
async def home_page(
    request: Request, 
    page: int = 1,
    db: AsyncSession = Depends(get_db)
):
    limit = 50
    offset = (page - 1) * limit
    users, total = await get_paginated_users(db, offset, limit)
    
    total_pages = (total + limit - 1) // limit
    
    return templates.TemplateResponse(request, "index.html", {
        "users": users,
        "total": total,
        "page": page,
        "total_pages": total_pages,
        "limit": limit
    })

@app.post("/load")
async def load_users(load_request: LoadRequest, db: AsyncSession = Depends(get_db)):
    added = await load_users_to_db(db, load_request.count)
    total = await count_users(db)
    return {"success": True, "added": added, "total": total}

@app.get("/user/{user_id}", response_class=HTMLResponse)
async def user_detail(request: Request, user_id: int, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_id(db, user_id)
    if not user:
        return templates.TemplateResponse(request, "404.html", {
            "message": f"User with id {user_id} not found"
        }, status_code=404)
    
    return templates.TemplateResponse(request, "user_detail.html", {
        "user": user
    })

@app.get("/random", response_class=HTMLResponse)
async def random_user(request: Request, db: AsyncSession = Depends(get_db)):
    user = await get_random_user(db)
    if not user:
        return templates.TemplateResponse(request, "404.html", {
            "message": "No users in database"
        }, status_code=404)
    
    return templates.TemplateResponse(request, "user_detail.html", {
        "user": user
    })
