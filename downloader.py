#!/usr/bin/env python3
"""
YouTube to MP3 Downloader
Usage: python downloader.py <URL> [--output-dir ./downloads]
Supports: YouTube, SoundCloud, Vimeo, and 1000+ other sites via yt-dlp
"""

import argparse
import os
import sys
import subprocess


def check_dependencies():
    for tool in ["yt-dlp", "ffmpeg"]:
        try:
            subprocess.run([tool, "--version"], capture_output=True, check=True)
        except (FileNotFoundError, subprocess.CalledProcessError):
            print(f"[ERROR] {tool} is not installed.")
            if tool == "yt-dlp":
                print("   Install: pip install yt-dlp")
            else:
                print("   Install: brew install ffmpeg (Mac) or sudo apt install ffmpeg (Linux)")
            sys.exit(1)


def download_mp3(url, output_dir="./downloads", quality="192"):
    os.makedirs(output_dir, exist_ok=True)
    output_template = os.path.join(output_dir, "%(title)s.%(ext)s")
    cmd = [
        "yt-dlp", "-x",
        "--audio-format", "mp3",
        "--audio-quality", quality,
        "--embed-thumbnail",
        "--embed-metadata",
        "--no-playlist",
        "-o", output_template,
        "--progress",
        url
    ]
    print(f"Downloading: {url}")
    print(f"Saving to: {output_dir}")
    print(f"Quality: {quality}kbps MP3")
    try:
        subprocess.run(cmd, check=True)
        print(f"Done! Check {output_dir}/")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Download failed: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Download audio from YouTube (and 1000+ other sites) as MP3",
        epilog="Examples:\n"
               "  python downloader.py https://youtube.com/watch?v=VIDEO_ID\n"
               "  python downloader.py URL --quality 320\n"
               "  python downloader.py URL --output-dir ~/Music",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("url", help="URL of the video/audio to download")
    parser.add_argument("--output-dir", "-o", default="./downloads", help="Output directory (default: ./downloads)")
    parser.add_argument("--quality", "-q", default="192", choices=["128", "192", "256", "320"], help="MP3 bitrate in kbps (default: 192)")
    args = parser.parse_args()
    check_dependencies()
    download_mp3(args.url, args.output_dir, args.quality)


if __name__ == "__main__":
    main()
