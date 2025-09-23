from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, Boolean, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()

# Association table (many-to-many User <-> Group)
UserGroup = Table(
    'user_group',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.user_id'), primary_key=True),
    Column('group_id', Integer, ForeignKey('groups.group_id'), primary_key=True),
    Column('joined_at', TIMESTAMP, server_default=func.current_timestamp())
)


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    telegram_id = Column(String(50), nullable=False, unique=True)

    whitelisted = Column(Boolean, default=False)
    banned = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)

    boob_size = Column(Integer, default=0)  # current size in cm
    last_growth = Column(TIMESTAMP, server_default=func.current_timestamp())  # last /grow
    streak = Column(Integer, default=0)  # daily growth streak

    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relationships
    settings = relationship("Settings", uselist=False, back_populates="user", cascade="all, delete-orphan")
    history = relationship("GrowthHistory", back_populates="user", cascade="all, delete-orphan")
    groups = relationship("Group", secondary=UserGroup, back_populates="users")


class Group(Base):
    __tablename__ = 'groups'

    group_id = Column(Integer, primary_key=True)
    telegram_id = Column(String(50), nullable=False, unique=True)
    whitelisted = Column(Boolean, default=False)

    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    # Relationships
    users = relationship("User", secondary=UserGroup, back_populates="groups")


class Settings(Base):
    __tablename__ = 'settings'

    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)

    notifications_enabled = Column(Boolean, default=True)  # toggle game notifications
    auto_reset_negative = Column(Boolean, default=False)  # auto reset if stuck below 0

    user = relationship("User", back_populates="settings")


class GrowthHistory(Base):
    __tablename__ = 'growth_history'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)

    growth_amount = Column(Integer, nullable=False)  # change in size for that day (-2 to +10)
    total_size = Column(Integer, nullable=False)  # size after applying growth
    grown_at = Column(TIMESTAMP, server_default=func.current_timestamp())  # timestamp of growth

    user = relationship("User", back_populates="history")
