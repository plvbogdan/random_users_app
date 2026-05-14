import asyncio
import httpx
from typing import List, Dict, Any

API_BASE_URL = "https://api.randomdatatools.ru"

async def fetch_users_batch(count: int) -> List[Dict[str, Any]]:
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(f"{API_BASE_URL}/?count={count}")
        response.raise_for_status()
        data = response.json()
        
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            return [data]
        return []

async def fetch_users_total(target_count: int) -> List[Dict[str, Any]]:
    if target_count <= 0:
        return []
    
    all_users = []
    remaining = target_count
    
    while remaining > 0:
        batch_size = min(remaining, 100)  
        batch = await fetch_users_batch(batch_size)
        all_users.extend(batch)
        remaining -= batch_size
        
        if remaining > 0:
            await asyncio.sleep(1.1)
    
    return all_users