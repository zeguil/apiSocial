from config.database import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from sqlalchemy import (Column, Integer, String, 
                        ForeignKey, Boolean, DateTime, Index)


class User(Base):
    """
    Modelo User representando um usuário no sistema.
    Cada usuário possui um relacionamento um-para-um com um Profile.
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String)
    email = Column(String, unique=True)
    is_admin = Column(Boolean, default=False)
    token = Column(String, nullable=True)
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    profile = relationship("Profile", uselist=False, back_populates="user")

    __table_args__ = (
        Index('idx_users_username_email', 'username', 'email', unique=True),
    )


class Profile(Base):
    """
    Modelo Profile representando o perfil do usuário.
    Cada perfil possui um relacionamento um-para-um com um User.
    """
    __tablename__ = 'profiles'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    full_name = Column(String(100), nullable=True)
    bio = Column(String(500), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    user = relationship("User", back_populates="profile")
