from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    ratings = relationship("Rating", back_populates="user", cascade="all, delete-orphan")

class Song(Base):
    __tablename__ = "songs"
    
    id = Column(Integer, primary_key=True, index=True)
    order = Column(Integer, nullable=False)
    country = Column(String, nullable=False, index=True)
    artist = Column(String, nullable=False)
    song_name = Column(String, nullable=False)
    youtube_url = Column(String, nullable=True)
    
    ratings = relationship("Rating", back_populates="song", cascade="all, delete-orphan")

class Rating(Base):
    __tablename__ = "ratings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    song_id = Column(Integer, ForeignKey("songs.id"), nullable=False)
    stage_show = Column(Integer, nullable=True)  # 1-12
    musical_performance = Column(Integer, nullable=True)  # 1-12
    sex_appeal = Column(Integer, nullable=True)  # 1-12
    wtf_factor = Column(Integer, nullable=True)  # 1-12
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="ratings")
    song = relationship("Song", back_populates="ratings")
    
    @property
    def final_rating(self):
        """Calculate weighted final rating: stage_show=30%, musical_performance=40%, sex_appeal=15%, wtf_factor=15%"""
        if all(x is not None for x in [self.stage_show, self.musical_performance, self.sex_appeal, self.wtf_factor]):
            weighted = (
                self.stage_show * 0.30 +
                self.musical_performance * 0.40 +
                self.sex_appeal * 0.15 +
                self.wtf_factor * 0.15
            )
            return round(weighted, 1)
        return None
