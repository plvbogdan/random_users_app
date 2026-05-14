from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class UserBase(BaseModel):
    external_id: Optional[str] = None
    gender: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    street: Optional[str] = None
    building: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class UserFromAPI(BaseModel):
    FirstName: Optional[str] = None
    LastName: Optional[str] = None
    Gender: Optional[str] = None
    Phone: Optional[str] = None
    Email: Optional[str] = None
    City: Optional[str] = None
    Street: Optional[str] = None
    House: Optional[str] = None

class PaginatedUsersResponse(BaseModel):
    users: List[UserResponse]
    total: int
    offset: int
    limit: int

class LoadRequest(BaseModel):
    count: int