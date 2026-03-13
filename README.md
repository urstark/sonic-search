# YouTube Data Extraction with py-yt-search


## Features
- Search YouTube for videos, channels, and playlists
- Retrieve video and playlist details
- Extract comments from videos
- Fetch search suggestions from YouTube

## Installation
Make sure you have Python installed (>=3.8). Install `py-yt-search` using:

```bash
pip install git+https://github.com/urstark/sonic-search@main
```

```bash
pip install py-yt-search
```

## Usage
The script uses `asyncio` to execute YouTube queries asynchronously. Below is an overview of the main functions:

### Search YouTube
```python
_search = Search('NoCopyrightSounds', limit=1, language='en', region='US')
result = await _search.next()
print(result)
```

### Search for Videos Only
```python
videosSearch = VideosSearch('NoCopyrightSounds', limit=10, language='en', region='US')
videosResult = await videosSearch.next()
print(videosResult)
```

### Search for Channels Only
```python
channelsSearch = ChannelsSearch('NoCopyrightSounds', limit=1, language='en', region='US')
channelsResult = await channelsSearch.next()
print(channelsResult)
```

### Search for Playlists Only
```python
playlistsSearch = PlaylistsSearch('NoCopyrightSounds', limit=1, language='en', region='US')
playlistsResult = await playlistsSearch.next()
print(playlistsResult)
```

### Get Video Details
```python
video = await Video.get('z0GKGpObgPY')
print(video)
```

### Get Playlist Details
```python
playlist = await Playlist.get('https://www.youtube.com/playlist?list=PLRBp0Fe2GpgmsW46rJyudVFlY6IYjFBIK')
print(playlist)
```

### Fetch Comments from a Video
```python
comments = Comments('_ZdsmLgCVdU')
await comments.getNextComments()
print(len(comments.comments['result']))
```

### Retrieve Video Transcript
```python
transcript = await Transcript.get('https://www.youtube.com/watch?v=L7kF4MXXCoA')
print(transcript)
```

### Get YouTube Search Suggestions
```python
suggestions = await Suggestions.get('NoCopyrightSounds', language='en', region='US')
print(suggestions)
```

## Running the Script
To run the script, execute:
```bash
python script.py
```

Ensure `asyncio.run(main())` is at the end of the script to handle async execution.

## Notes
- The script uses `asyncio` for efficient asynchronous operations.
- Some operations may require multiple calls to retrieve all available data (e.g., pagination for comments and playlists).
- `py-yt-search` provides various search filters to refine results, such as sorting by upload date or filtering by duration.

## Deployment

### Deploying to a Free Tier Service (e.g., Render)

Free-tier hosting services like Render are a great way to run this API 24/7 without cost. These services, however, typically put your application to "sleep" after a period of inactivity (e.g., 15 minutes) to save resources. To keep the service running, you can use an external monitoring service to send it a request every few minutes.

Here’s a step-by-step guide to deploy on Render:

1.  **Fork the Repository:**
    First, fork this repository to your own GitHub account.

2.  **Add `requirements.txt`:**
    In the root of your project, ensure a file named `requirements.txt` exists. This file tells Render which Python packages to install. It should contain:
    ```
    fastapi
    uvicorn[standard]
    python-dotenv
    .
    ```
    The `.` at the end is important; it tells `pip` to also install the local `py-yt` package from your repository. Commit this file to your repository.

3.  **Set up on Render:**
    *   Go to the Render Dashboard and create a new **Web Service**.
    *   Connect the GitHub repository you just forked.
    *   Render will auto-detect that it's a Python project. You'll need to configure the following settings:
        *   **Build Command**: `pip install -r requirements.txt`
        *   **Start Command**: `uvicorn api:app --host 0.0.0.0 --port $PORT`
    *   Under "Advanced", you can add **Environment Variables**. For example, if you use the recommendations feature, add your `LASTFM_API_KEY` here.

4.  **Keep the Service Alive:**
    *   Once your service is deployed, Render will give you a public URL (e.g., `https://your-app-name.onrender.com`).
    *   To prevent it from sleeping, use a free uptime monitoring service like UptimeRobot or cron-job.org.
    *   Create a new monitor in the service of your choice. Set it to make an HTTP GET request to your API's health check endpoint every 5-15 minutes.
    *   **URL to Ping**: `https://your-app-name.onrender.com/health`

This setup ensures your API is always online and responsive, running on a free tier.

---

### Deploying to any VPS (Docker)

To deploy this API to any VPS (DigitalOcean, Linode, AWS, etc.), the easiest way is using Docker.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/urstark/sonic-search.git
    cd sonic-search
    ```

2.  **Using Docker Compose (Recommended):**
    ```bash
    docker-compose up -d
    ```
    This will start the API on port `8000`.

3.  **Using Docker Build:**
    ```bash
    docker build -t sonic-search .
    docker run -d -p 8000:8000 sonic-search
    ```

### Manual Deployment on VPS

If you prefer not to use Docker:

1.  **Install dependencies:**
    ```bash
    pip install .
    ```

2.  **Run with Uvicorn:**
    ```bash
    uvicorn api:app --host 0.0.0.0 --port 8000
    ```

## License
This project is licensed under the MIT License. See the [LICENSE](/LICENSE) file for details.

## Credits
This project is based on [youtube-search-python](https://github.com/alexmercerind/youtube-search-python) by Alex Mercer.
