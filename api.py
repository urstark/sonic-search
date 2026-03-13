from typing import Optional
import logging

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from py_yt import (
    Search,
    VideosSearch,
    PlaylistsSearch,
    Playlist,
    Suggestions,
    Recommendations,
)
from py_yt.extras import Lyrics

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Sonic Search API",
    description="An unofficial YouTube API to search and retrieve YouTube data.",
    version="2.1.0",
)

@app.get("/", tags=["Root"])
async def read_root():
    """Lists all available endpoints."""
    endpoints = {
        route.name: route.path
        for route in app.routes
        if hasattr(route, "path") and route.name != "read_root"
    }
    return {
        "message": "Welcome to the Sonic Search API! Here are the available endpoints:",
        "endpoints": endpoints,
        "docs_url": "/docs",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Checks the health of the API.
    """
    return {"status": "running"}

@app.get("/search", tags=["Search"])
async def search_youtube(
    query: str,
    limit: int = 20,
    language: str = "en",
    region: str = "US",
):
    """Search for videos, channels, and playlists on YouTube."""
    try:
        _search = Search(query, limit=limit, language=language, region=region)
        return await _search.next()
    except Exception as e:
        logging.error(f"Error in /search: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/search/videos", tags=["Search"])
async def search_videos(
    query: str,
    limit: int = 20,
    language: str = "en",
    region: str = "US",
):
    """Search for videos on YouTube."""
    try:
        videos_search = VideosSearch(query, limit=limit, language=language, region=region)
        return await videos_search.next()
    except Exception as e:
        logging.error(f"Error in /search/videos: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/search/playlists", tags=["Search"])
async def search_playlists(
    query: str,
    limit: int = 20,
    language: str = "en",
    region: str = "US",
):
    """Search for playlists on YouTube."""
    try:
        playlists_search = PlaylistsSearch(
            query, limit=limit, language=language, region=region
        )
        return await playlists_search.next()
    except Exception as e:
        logging.error(f"Error in /search/playlists: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/playlist", tags=["Playlist"])
async def get_playlist_details(url: str):
    """Get details for a specific playlist by its URL."""
    try:
        return await Playlist.get(url)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logging.error(f"Error in /playlist: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/suggestions", tags=["Suggestions"])
async def get_search_suggestions(query: str, language: str = "en", region: str = "US"):
    """Get YouTube search suggestions for a query."""
    try:
        return await Suggestions.get(query, language=language, region=region)
    except Exception as e:
        logging.error(f"Error in /suggestions: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/lyrics", tags=["Lyrics"])
async def get_lyrics(query: str):
    """Get lyrics for a song query."""
    try:
        return await Lyrics.get(query)
    except Exception as e:
        logging.error(f"Error in /lyrics: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/recommendations/genre", tags=["Recommendations"])
async def get_genre_recommendations(genre: str, limit: int = 10):
    """Get song recommendations based on a genre (tag)."""
    try:
        return await Recommendations.get_by_genre(genre, limit)
    except Exception as e:
        logging.error(f"Error in /recommendations/genre: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/recommendations/song", tags=["Recommendations"])
async def get_song_recommendations(song: str, limit: int = 10):
    """Get similar songs based on a song name."""
    try:
        return await Recommendations.get_similar_tracks(song, limit)
    except Exception as e:
        logging.error(f"Error in /recommendations/song: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
