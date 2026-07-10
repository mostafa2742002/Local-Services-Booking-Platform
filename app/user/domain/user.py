from dataclasses import dataclass
from uuid import UUID
from app.user.domain.role import Role

@dataclass
class User:
    id: UUID
    name: str
    email: str
    password_hash: str
    role: Role
    created_at: str
    updated_at: str
