from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models import User
from app.api_client import fetch_users_total
from typing import List, Optional, Tuple

async def convert_api_user_to_db(api_user: dict) -> User:
    """
    Преобразует данные из API в модель User
    """
    return User(
        external_id=f"{api_user.get('LastName', '')}_{api_user.get('FirstName', '')}",
        gender=api_user.get("Gender"),
        first_name=api_user.get("FirstName"),
        last_name=api_user.get("LastName"),
        email=api_user.get("Email"),
        phone=api_user.get("Phone"),
        city=api_user.get("City"),
        street=api_user.get("Street"),
        building=str(api_user.get("House", "")) if api_user.get("House") else None,
    )

async def load_users_to_db(db: AsyncSession, target_count: int) -> int:
    """
    Загружает пользователей из API и сохраняет в БД.
    Пропускает дубликаты по email.
    Возвращает количество реально добавленных пользователей.
    """
    if target_count <= 0:
        return 0
    
    api_users = await fetch_users_total(target_count)
    
    added_count = 0
    for api_user in api_users:
        email = api_user.get("Email")
        
        if email:
            existing = await db.execute(
                select(User).where(User.email == email)
            )
            if existing.scalar_one_or_none():
                continue
        
        user = await convert_api_user_to_db(api_user)
        db.add(user)
        added_count += 1
    
    await db.commit()
    return added_count

async def get_paginated_users(
    db: AsyncSession, 
    offset: int = 0, 
    limit: int = 50
) -> Tuple[List[User], int]:
    """
    Возвращает пагинированный список пользователей и общее количество
    """
    total_result = await db.execute(select(func.count()).select_from(User))
    total = total_result.scalar_one()
    
    result = await db.execute(
        select(User)
        .order_by(User.id)
        .offset(offset)
        .limit(limit)
    )
    users = result.scalars().all()
    
    return users, total

async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    """
    Получает пользователя по ID
    """
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

async def get_random_user(db: AsyncSession) -> Optional[User]:
    """
    Получает случайного пользователя
    """
    result = await db.execute(select(User).order_by(func.random()).limit(1))
    return result.scalar_one_or_none()

async def count_users(db: AsyncSession) -> int:
    """
    Общее количество пользователей в БД
    """
    result = await db.execute(select(func.count()).select_from(User))
    return result.scalar_one()

async def is_db_empty(db: AsyncSession) -> bool:
    """
    Проверяет, пустая ли база данных
    """
    return await count_users(db) == 0