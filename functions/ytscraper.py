import os
from yt_dlp import YoutubeDL

def fetch_playlist_info_by_id(playlist_id: str) -> dict:
    url = f"https://www.youtube.com/playlist?list={playlist_id}"
    ydl_opts = {
        "quiet": True,
        "extract_flat": True,   # only metadata, no downloads
        "skip_download": True,
        'n_threads': 8,
        "cookiefile":"cookies.txt",
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
    return info

def fetch_video_info_by_id(video_id: str) -> dict:
    url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts = {
        "quiet": True,
        "extract_flat": False,  # full info for single video
        "skip_download": True,
        'n_threads': 8,
        "cookiefile":"cookies.txt",
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        print(info)
    return info


def download_audio(video_id: str, DOWNLOADS_DIR="downloads/") -> str:
    """Download YouTube video as MP3 and return file path."""
    url = f"https://www.youtube.com/watch?v={video_id}"

    ydl_opts = {
    "format": "bestaudio[ext=m4a]/bestaudio/best",   # pick m4a first (no conversion needed)
    "outtmpl": os.path.join(DOWNLOADS_DIR, f"{video_id}.%(ext)s"),
    "quiet": False,
    "cookiefile": "cookies.txt",
    "n_threads": 8,
    'fixup': 'never',
    "postprocessors": [],   # 🚀 no re-encoding, just download as-is
    }
#    ydl_opts = {
#        "format": "bestaudio/best",
#        "outtmpl": os.path.join(DOWNLOADS_DIR, f"{video_id}.%(ext)s"),
#        "quiet": False,
#        "cookiefile":"cookies.txt",
#        'n_threads': 8,
#        "postprocessors": [{
#            "key": "FFmpegExtractAudio",
#            "preferredcodec": "mp3",
#            "preferredquality": "192"
#        }],
#    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info)
        file_path = os.path.splitext(file_path)[0] + ".mp3"
    return file_path


def download_video(video_id: str, DOWNLOADS_DIR="downloads/") -> str:
    """Download YouTube video as MP4 and return file path."""
    url = f"https://www.youtube.com/watch?v={video_id}"

    ydl_opts = {
        "format": "best[ext=mp4]/best",
        "outtmpl": os.path.join(DOWNLOADS_DIR, f"{video_id}.%(ext)s"),
        "cookiefile":"cookies.txt",
        'fixup': 'never',
        'n_threads': 8,
        "quiet": False,
    }

    with YoutubeDL(ydl_opts) as ydl:
        print('getting info')
        info = ydl.extract_info(url, download=True)
        print(info)
        file_path = ydl.prepare_filename(info)
    return file_path,info
