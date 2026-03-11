#!/usr/bin/env python3
"""
YouTube to MP3 Downloader — Web UI
Run: python app.py
Open: http://localhost:5000
"""

from flask import Flask, render_template, request, jsonify, send_file
import subprocess
import os
import glob
import threading
import uuid
import time

app = Flask(__name__)
DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Track download status
downloads = {}


def run_download(job_id, url, quality):
    """Run yt-dlp in background."""
    downloads[job_id] = {"status": "downloading", "progress": 0, "filename": None, "error": None}

    job_dir = os.path.join(DOWNLOAD_DIR, job_id)
    os.makedirs(job_dir, exist_ok=True)
    output_template = os.path.join(job_dir, "%(title)s.%(ext)s")

    cmd = [
        "yt-dlp", "-x",
        "--audio-format", "mp3",
        "--audio-quality", quality,
        "--embed-thumbnail",
        "--embed-metadata",
        "--no-playlist",
        "-o", output_template,
        "--newline",
        url
    ]

    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            if "[download]" in line and "%" in line:
                try:
                    pct = float(line.split("%")[0].split()[-1])
                    downloads[job_id]["progress"] = pct
                except:
                    pass
        process.wait()

        if process.returncode == 0:
            mp3_files = glob.glob(os.path.join(job_dir, "*.mp3"))
            if mp3_files:
                downloads[job_id]["status"] = "done"
                downloads[job_id]["filename"] = os.path.basename(mp3_files[0])
                downloads[job_id]["filepath"] = mp3_files[0]
                downloads[job_id]["progress"] = 100
            else:
                downloads[job_id]["status"] = "error"
                downloads[job_id]["error"] = "No MP3 file was created"
        else:
            downloads[job_id]["status"] = "error"
            downloads[job_id]["error"] = "Download failed"
    except Exception as e:
        downloads[job_id]["status"] = "error"
        downloads[job_id]["error"] = str(e)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/download", methods=["POST"])
def start_download():
    url = request.json.get("url", "").strip()
    quality = request.json.get("quality", "192")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    job_id = str(uuid.uuid4())[:8]
    thread = threading.Thread(target=run_download, args=(job_id, url, quality))
    thread.start()

    return jsonify({"job_id": job_id})


@app.route("/status/<job_id>")
def check_status(job_id):
    if job_id not in downloads:
        return jsonify({"error": "Job not found"}), 404
    return jsonify(downloads[job_id])


@app.route("/file/<job_id>")
def get_file(job_id):
    if job_id not in downloads or downloads[job_id]["status"] != "done":
        return jsonify({"error": "File not ready"}), 404
    return send_file(downloads[job_id]["filepath"], as_attachment=True)


if __name__ == "__main__":
    print("\n  YouTube to MP3 Downloader")
    print("  Open http://localhost:5000 in your browser\n")
    app.run(debug=False, port=5000)
