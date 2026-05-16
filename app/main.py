from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func
import os

from .database import engine, get_db, init_db
from . import models
from .fetch_songs import fetch_eurovision_2026_songs

# Initialize database
init_db()

# Create FastAPI app
app = FastAPI(title="Eurovision Voting App")

# Setup templates
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=templates_dir)

# Serve static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

def seed_songs(db: Session):
    """Seed the database with Eurovision songs"""
    if db.query(models.Song).first():
        return  # Already seeded
    
    songs_data = fetch_eurovision_2026_songs()
    for song_data in songs_data:
        song = models.Song(**song_data)
        db.add(song)
    db.commit()

# Routes

@app.get("/", response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)):
    """Landing page - user registration/selection"""
    seed_songs(db)
    users = db.query(models.User).all()
    return templates.TemplateResponse("index.html", {"request": request, "users": users})

@app.post("/register")
def register_user(request: Request, db: Session = Depends(get_db)):
    """Register a new user"""
    # This will be called via AJAX from the frontend
    return {"status": "pending"}

@app.get("/mgp/{username}", response_class=HTMLResponse)
def song_list(username: str, request: Request, db: Session = Depends(get_db)):
    """Main song list page"""
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return RedirectResponse(url="/")
    
    songs = db.query(models.Song).order_by(models.Song.order).all()
    
    # Get all ratings for all songs
    all_ratings = db.query(models.Rating).all()
    
    # Group ratings by song
    ratings_by_song = {}
    for rating in all_ratings:
        if rating.song_id not in ratings_by_song:
            ratings_by_song[rating.song_id] = {}
        ratings_by_song[rating.song_id][rating.user.username] = rating
    
    return templates.TemplateResponse(
        "song_list.html",
        {
            "request": request,
            "username": username,
            "songs": songs,
            "ratings_by_song": ratings_by_song
        }
    )

@app.get("/mgp/{username}/rate/{song_id}", response_class=HTMLResponse)
def rating_page(username: str, song_id: int, request: Request, db: Session = Depends(get_db)):
    """Rating page for a specific song"""
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return RedirectResponse(url="/")
    
    song = db.query(models.Song).filter(models.Song.id == song_id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    
    # Get existing rating if any
    existing_rating = db.query(models.Rating).filter(
        models.Rating.user_id == user.id,
        models.Rating.song_id == song_id
    ).first()
    
    return templates.TemplateResponse(
        "rating.html",
        {
            "request": request,
            "username": username,
            "song": song,
            "rating": existing_rating
        }
    )

@app.post("/api/users")
def create_user(username: str, db: Session = Depends(get_db)):
    """Create a new user via API"""
    existing_user = db.query(models.User).filter(models.User.username == username).first()
    if existing_user:
        return {"id": existing_user.id, "username": existing_user.username}
    
    user = models.User(username=username)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "username": user.username}

@app.post("/api/ratings")
def save_rating(user_id: int, song_id: int, stage_show: int, musical_performance: int, 
                sex_appeal: int, wtf_factor: int, db: Session = Depends(get_db)):
    """Save or update a rating"""
    rating = db.query(models.Rating).filter(
        models.Rating.user_id == user_id,
        models.Rating.song_id == song_id
    ).first()
    
    if not rating:
        rating = models.Rating(
            user_id=user_id,
            song_id=song_id,
            stage_show=stage_show,
            musical_performance=musical_performance,
            sex_appeal=sex_appeal,
            wtf_factor=wtf_factor
        )
        db.add(rating)
    else:
        rating.stage_show = stage_show
        rating.musical_performance = musical_performance
        rating.sex_appeal = sex_appeal
        rating.wtf_factor = wtf_factor
    
    db.commit()
    db.refresh(rating)
    return {"final_rating": rating.final_rating}

@app.get("/mgp/{username}/results", response_class=HTMLResponse)
def results_page(username: str, sort_by: str = "average", sort_dir: str = "desc", request: Request = None, db: Session = Depends(get_db)):
    """Results page showing all votes with optional sorting"""
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return RedirectResponse(url="/")
    
    users = db.query(models.User).all()
    songs = db.query(models.Song).order_by(models.Song.order).all()
    
    # Build results matrix
    results = []
    for song in songs:
        song_result = {
            "song": song,
            "ratings": {}
        }
        for user_item in users:
            rating = db.query(models.Rating).filter(
                models.Rating.user_id == user_item.id,
                models.Rating.song_id == song.id
            ).first()
            song_result["ratings"][user_item.username] = rating.final_rating if rating else None
        
        # Calculate average
        ratings_list = [r for r in song_result["ratings"].values() if r is not None]
        song_result["average"] = round(sum(ratings_list) / len(ratings_list), 1) if ratings_list else None
        results.append(song_result)
    
    # Sort based on parameters
    reverse = sort_dir == "desc"
    
    if sort_by == "average":
        results.sort(key=lambda x: x["average"] if x["average"] else 0, reverse=reverse)
    elif sort_by in [u.username for u in users]:
        results.sort(key=lambda x: x["ratings"][sort_by] if x["ratings"][sort_by] else 0, reverse=reverse)
    else:
        # Default to song order
        results.sort(key=lambda x: x["song"].order, reverse=False)
    
    return templates.TemplateResponse(
        "results.html",
        {
            "request": request,
            "username": username,
            "users": users,
            "results": results,
            "sort_by": sort_by,
            "sort_dir": sort_dir
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
