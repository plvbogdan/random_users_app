import pytest
from app.services import get_paginated_users, count_users
from app.models import User


@pytest.mark.asyncio
async def test_save_user_to_db(db_session):
    user = User(
        first_name="Test",
        last_name="User",
        email="test@test.local"
    )
    db_session.add(user)
    await db_session.commit()
    
    total = await count_users(db_session)
    assert total == 1


@pytest.mark.asyncio
async def test_pagination_works(db_session):
    for i in range(30):
        db_session.add(User(email=f"pagination_{i}@test.local"))
    await db_session.commit()
    
    users_page1, total = await get_paginated_users(db_session, 0, 10)
    assert len(users_page1) == 10
    assert total == 30
    
    users_page2, _ = await get_paginated_users(db_session, 10, 10)
    assert len(users_page2) == 10
    assert users_page1[0].id != users_page2[0].id