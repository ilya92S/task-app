from dataclasses import dataclass

from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from models import UserProfile

@dataclass
class AuthRepository:
    db_session: Session

    pass