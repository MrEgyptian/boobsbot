import yt_dlp,os

def fetch_video_info(url: str) -> dict:
    """
    Fetch metadata from any site (Vimeo, YouTube, Instagram, TikTok, etc.)
    using yt-dlp.
    """
    ydl_opts = {"quiet": True,
                "cookiefile": "cookies.txt",
                }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info

def download_video(url: str, output_dir: str = "downloads") -> str:
    """
    Download a video from any supported site (Instagram, Vimeo, YouTube, TikTok, etc.)
    using yt-dlp and return the saved file path.
    """
    output = os.path.join(output_dir, "./%(title)s.%(ext)s")
    ydl_opts = {
        "outtmpl": output,
        "cookiefile": "cookies.txt",
        "format": "bv+ba/b"  # best video + audio
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)
