from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey,Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()
class User(Base):
    __tablename__ = 'Users'
    
    user_id = Column(Integer, primary_key=True)
    whitelisted = Column(Boolean, default=False)
    banned = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    telegram_id = Column(String(50), nullable=False, unique=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    downloads = relationship("Download", back_populates="user") 
    favorites = relationship("Favorites", back_populates="user")
    settings = relationship("Settings", uselist=False, back_populates="user")
class File(Base):
    __tablename__ = 'Files'
    
    file_id = Column(Integer, primary_key=True)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(255), nullable=False)
    file_size = Column(Integer, nullable=False)
    file_type = Column(String(50), nullable=False)
    file_tg_id = Column(String(50), nullable=False)
    uploaded_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    downloads = relationship("Download", back_populates="file")
    favorites = relationship("Favorites", back_populates="file")
    favorited_by = relationship("Favorites", back_populates="file")

class Group(Base):
    __tablename__ = 'Groups'
    group_id = Column(Integer, primary_key=True)
    telegram_id = Column(String(50), nullable=False, unique=True)
    whitelisted = Column(Boolean, default=False)
    
class Download(Base):
    __tablename__ = 'Downloads'
    download_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.user_id'), nullable=False)
    file_id = Column(Integer, ForeignKey('Files.file_id'), nullable=False)
    downloaded_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    status = Column(String(20), nullable=False)
    user = relationship("User", back_populates="downloads")
    file = relationship("File", back_populates="downloads")
class Favorites(Base):
    __tablename__ = 'Favorites'
    favorite_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.user_id'), nullable=False)
    file_id = Column(Integer, ForeignKey('Files.file_id'), nullable=False)
    added_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    user = relationship("User", back_populates="favorites")
    file = relationship("File", back_populates="favorited_by")
class Settings(Base):
    __tablename__ = 'Settings'
    video_download_quality = Column(String(50), nullable=False, default="720p")
    video_download_format = Column(String(50), nullable=False, default="mp4")
    audio_download_quality = Column(String(50), nullable=False, default="128kbps")
    audio_download_format = Column(String(50), nullable=False, default="mp3")
    auto_delete_history = Column(Boolean, default=False)
    auto_delete_history_after= Column(Integer, default=30)  # days
    user_id = Column(Integer, ForeignKey('Users.user_id'), nullable=False, primary_key=True)
    user = relationship("User", back_populates="settings")