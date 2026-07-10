import json
from pathlib import Path
from uuid import UUID

from app.user.domain.user import User
from app.user.domain.role import Role

DATA_FILE = Path("data/users.json")

def user_to_dict(user: User) -> dict:
    return {
        "id": str(user.id),
        "name": user.name,
        "email": user.email,
        "password_hash": user.password_hash,
        "role": user.role.value,
        "created_at": user.created_at,
        "updated_at": user.updated_at
    }
    

def dict_to_user(data: dict) -> User:
    return User(
        id=UUID(data["id"]),
        name=data["name"],
        email=data["email"],
        password_hash=data["password_hash"],
        role=Role(data["role"]),
        created_at=data["created_at"],
        updated_at=data["updated_at"]
    )
    
def load_users() -> list[User]:
    if not DATA_FILE.exists():
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        DATA_FILE.write_text("[]")
    
    content = DATA_FILE.read_text().strip()
    
    if content == "":
        return []
    
    user_data = json.loads(content)
    
    return [dict_to_user(data) for data in user_data]


def save_users(users: list[User]) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    users_data = [user_to_dict(user) for user in users]

    DATA_FILE.write_text(json.dumps(users_data, indent=4))


def find_all() -> list[User]:
    return load_users()


def find_by_email(email: str) -> User | None:
    users = load_users()

    for user in users:
        if user.email == email:
            return user

    return None

def find_by_id(user_id: UUID) -> User | None:
    users = load_users()

    for user in users:
        if user.id == user_id:
            return user

    return None


def save(user: User) -> User:
    users = load_users()
    users.append(user)
    save_users(users)

    return user