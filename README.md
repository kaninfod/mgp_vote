# Eurovision Voting App 2026 🎵

A festive web application for voting on Eurovision songs in real-time with multiple users.

## Features

- 🎭 Multi-user voting system with username-based sessions
- ⭐ 4-parameter rating system (Stage Show, Musical Performance, Sex Appeal, WTF Factor)
- 🎯 Weighted rating calculation (30%, 40%, 15%, 15%)
- 📊 Real-time results display with rankings
- 🎨 Festive Eurovision-themed UI with Bootstrap 5
- 🎬 YouTube video integration for each song
- 💾 Persistent SQLite database

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: Bootstrap 5, Stimulus JS
- **Database**: SQLite with SQLAlchemy ORM
- **Templates**: Jinja2

## Installation

### 1. Create a virtual environment

```bash
cd /Users/martinhinge/projects/mgp
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

## Running the App

```bash
cd /Users/martinhinge/projects/mgp
source venv/bin/activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Then open [http://localhost:8000](http://localhost:8000) in your browser.

## Pages

### 1. Registration Page (`/`)
- Register new voters or select existing ones
- Redirects to the voting interface

### 2. Song List (`/mgp/[username]`)
- Browse all Eurovision songs for tonight
- View current ratings from all voters
- Click "Rate This Song" to vote

### 3. Rating Page (`/mgp/[username]/rate/[song_id]`)
- Rate 4 categories (1-12 scale)
- Interactive sliders with real-time rating calculation
- YouTube video preview
- Save and return to song list

### 4. Results Page (`/mgp/[username]/results`)
- View all votes in a comprehensive table
- Rankings sorted by average rating
- Per-user ratings visible in columns

## Rating Calculation

The final rating is calculated as a weighted average:
- **Stage Show**: 30%
- **Musical Performance**: 40%
- **Sex Appeal**: 15%
- **WTF Factor**: 15%

Formula: `(stage_show × 0.30) + (musical × 0.40) + (sex × 0.15) + (wtf × 0.15)`

## Database Schema

### Users
- `id`: Primary key
- `username`: Unique voter name
- `created_at`: Registration timestamp

### Songs
- `id`: Primary key
- `order`: Song order in the contest
- `country`: Country name
- `artist`: Artist name
- `song_name`: Song title
- `youtube_url`: Link to YouTube video

### Ratings
- `id`: Primary key
- `user_id`: Foreign key to Users
- `song_id`: Foreign key to Songs
- `stage_show`: 1-12 rating
- `musical_performance`: 1-12 rating
- `sex_appeal`: 1-12 rating
- `wtf_factor`: 1-12 rating
- `created_at` / `updated_at`: Timestamps

## Project Structure

```
/Users/martinhinge/projects/mgp/
├── app/
│   ├── templates/
│   │   ├── base.html          # Base template with Bootstrap
│   │   ├── index.html         # Registration page
│   │   ├── song_list.html     # Main song voting page
│   │   ├── rating.html        # Individual song rating page
│   │   ├── results.html       # Results/rankings page
│   │   └── partials/
│   │       └── song_card.html # Song card component
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css      # Festive Eurovision theming
│   │   └── js/
│   │       └── application.js # Stimulus JS setup
│   ├── main.py                # FastAPI application
│   ├── models.py              # SQLAlchemy models
│   ├── database.py            # Database configuration
│   └── fetch_songs.py         # Eurovision songs data
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Notes

- The app supports 2-4 concurrent voters
- All data is stored locally in `mgp.db`
- The Eurovision 2026 song list is hardcoded for reliability
- YouTube links in the song list are prepared for embedding

## Future Enhancements

- Fetch live Eurovision data from API
- Export results as PDF/CSV
- Admin panel for results management
- User authentication (simple passwords)
- Real-time WebSocket updates
- Mobile app version
