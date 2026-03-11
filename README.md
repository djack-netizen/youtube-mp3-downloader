# YouTube to MP3 Downloader

A simple command-line tool to download audio from YouTube, SoundCloud, Vimeo, and 1000+ other sites as MP3 files.

## Setup

### 1. Install dependencies

```bash
# Install yt-dlp (the downloader)
pip install yt-dlp

# Install ffmpeg (for audio conversion)
# Mac:
brew install ffmpeg
# Linux:
sudo apt install ffmpeg
```

### 2. Clone this repo

```bash
git clone https://github.com/djack-netizen/youtube-mp3-downloader.git
cd youtube-mp3-downloader
```

## Usage

```bash
# Basic download
python downloader.py https://www.youtube.com/watch?v=VIDEO_ID

# Choose quality (128, 192, 256, 320 kbps)
python downloader.py URL --quality 320

# Custom output folder
python downloader.py URL --output-dir ~/Music
```

## Features
- Downloads as MP3 (configurable bitrate)
- Embeds album art from video thumbnail
- Embeds metadata (title, artist, etc.)
- Single video only (won't accidentally download full playlists)
- Supports YouTube, SoundCloud, Vimeo, Bandcamp, and 1000+ more sites
