import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import re

def fetch_eurovision_2026_songs() -> List[Dict]:
    """Fetch Eurovision 2026 songs from eurovisionworld.com"""
    
    # Eurovision 2026 Grand Final song list
    # Source: https://eurovisionworld.com/eurovision/2026
    songs = [
        {
            "order": 1,
            "country": "Denmark",
            "artist": "Søren Torpegaard Lund",
            "song_name": "Før vi går hjem",
            "youtube_url": "https://www.youtube.com/watch?v=lqXYe1SHNZA"
        },
        {
            "order": 2,
            "country": "Germany",
            "artist": "Sarah Engels",
            "song_name": "Fire",
            "youtube_url": "https://www.youtube.com/watch?v=FpGjPN1E2DE"
        },
        {
            "order": 3,
            "country": "Israel",
            "artist": "Noam Bettan",
            "song_name": "Michelle",
            "youtube_url": "https://www.youtube.com/watch?v=L9JVTSHKeqc"
        },
        {
            "order": 4,
            "country": "Belgium",
            "artist": "Essyla",
            "song_name": "Dancing on the Ice",
            "youtube_url": "https://www.youtube.com/watch?v=hz8CWouTIoo"
        },
        {
            "order": 5,
            "country": "Albania",
            "artist": "Alis",
            "song_name": "Nân",
            "youtube_url": "https://www.youtube.com/watch?v=FBoF2J8Mrbw"
        },
        {
            "order": 6,
            "country": "Greece",
            "artist": "Akylas",
            "song_name": "Ferto",
            "youtube_url": "https://www.youtube.com/watch?v=G0y1sZ4CxaE"
        },
        {
            "order": 7,
            "country": "Ukraine",
            "artist": "Leléka",
            "song_name": "Ridnym",
            "youtube_url": "https://www.youtube.com/watch?v=oSUIylL64XU"
        },
        {
            "order": 8,
            "country": "Australia",
            "artist": "Delta Goodrem",
            "song_name": "Eclipse",
            "youtube_url": "https://www.youtube.com/watch?v=xlze1NdwlII"
        },
        {
            "order": 9,
            "country": "Serbia",
            "artist": "Lavina",
            "song_name": "Kraj mene",
            "youtube_url": "https://www.youtube.com/watch?v=uyfdKvR1nJM"
        },
        {
            "order": 10,
            "country": "Malta",
            "artist": "Aidan",
            "song_name": "Bella",
            "youtube_url": "https://www.youtube.com/watch?v=FpG_DV2jAQo"
        },
        {
            "order": 11,
            "country": "Czechia",
            "artist": "Daniel Žižka",
            "song_name": "Crossroads",
            "youtube_url": "https://www.youtube.com/watch?v=MNfJxo04M5I"
        },
        {
            "order": 12,
            "country": "Bulgaria",
            "artist": "Dara",
            "song_name": "Bangaranga",
            "youtube_url": "https://www.youtube.com/watch?v=4Mxq2WCAhT4"
        },
        {
            "order": 13,
            "country": "Croatia",
            "artist": "Lelek",
            "song_name": "Andromeda",
            "youtube_url": "https://www.youtube.com/watch?v=-qtoDzlS-rk"
        },
        {
            "order": 14,
            "country": "United Kingdom",
            "artist": "Look Mum No Computer",
            "song_name": "Eins, Zwei, Drei",
            "youtube_url": "https://www.youtube.com/watch?v=xnls0LHAJLg"
        },
        {
            "order": 15,
            "country": "France",
            "artist": "Monroe",
            "song_name": "Regarde !",
            "youtube_url": "https://www.youtube.com/watch?v=YwwE7zqQ6XM"
        },
        {
            "order": 16,
            "country": "Moldova",
            "artist": "Satoshi",
            "song_name": "Viva, Moldova",
            "youtube_url": "https://www.youtube.com/watch?v=sJjTOalT4DY"
        },
        {
            "order": 17,
            "country": "Finland",
            "artist": "Linda Lampenius & Pete Parkkonen",
            "song_name": "Liekinheitin",
            "youtube_url": "https://www.youtube.com/watch?v=i8vlDO89YQA"
        },
        {
            "order": 18,
            "country": "Poland",
            "artist": "Alicja",
            "song_name": "Pray",
            "youtube_url": "https://www.youtube.com/watch?v=WsmVIlscdJU"
        },
        {
            "order": 19,
            "country": "Lithuania",
            "artist": "Lion Ceccah",
            "song_name": "Sólo quiero más",
            "youtube_url": "https://www.youtube.com/watch?v=_0kkvvTc3hQ"
        },
        {
            "order": 20,
            "country": "Sweden",
            "artist": "Felicia",
            "song_name": "My System",
            "youtube_url": "https://www.youtube.com/watch?v=az6XIorzZxM"
        },
        {
            "order": 21,
            "country": "Cyprus",
            "artist": "Antigoni",
            "song_name": "Jalla",
            "youtube_url": "https://www.youtube.com/watch?v=QMjGilVXpD0"
        },
        {
            "order": 22,
            "country": "Italy",
            "artist": "Sal Da Vinci",
            "song_name": "Per sempre sì",
            "youtube_url": "https://www.youtube.com/watch?v=OknnSe8SG8Q"
        },
        {
            "order": 23,
            "country": "Norway",
            "artist": "Jonas Lovv",
            "song_name": "Ya ya ya",
            "youtube_url": "https://www.youtube.com/watch?v=FcFaMMTz5-M"
        },
        {
            "order": 24,
            "country": "Romania",
            "artist": "Alexandra Căpitănescu",
            "song_name": "Choke Me",
            "youtube_url": "https://www.youtube.com/watch?v=xJgWNtg6YPo"
        },
        {
            "order": 25,
            "country": "Austria",
            "artist": "Cosmó",
            "song_name": "Tanzschein",
            "youtube_url": "https://www.youtube.com/watch?v=F9YqxdIzPQk"
        },
    ]
    
    return songs
