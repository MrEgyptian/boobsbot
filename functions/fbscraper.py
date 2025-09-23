import os, yt_dlp


def fetch_facebook_info(url: str) -> dict:
    """
    Extracts metadata for a Facebook video using yt-dlp.
    Returns a dictionary with uploader, title, duration, etc.
    """
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,  # don't download the video, only extract info
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            uploader_url = (
            info.get("uploader_url")
            or info.get("channel_url")  # fb sometimes uses this
            or (f"https://www.facebook.com/{info['uploader_id']}" if info.get("uploader_id") else None)
        )

        return {
            "uploader": info.get("uploader"),
            "title": info.get("title"),
            "duration": info.get("duration"),
            "thumbnail": info.get("thumbnail"),
            "view_count": info.get("view_count"),
            "like_count": info.get("like_count"),
            "uploader_url": uploader_url,
            "webpage_url": info.get("webpage_url"),
        }

    except Exception as e:
        print(f"[fetch_facebook_info] Error: {e}")
        return {}


async def download_image(url: str, filename="thumb.jpg"):
    """Download thumbnail image."""
    import aiohttp
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                with open(filename, "wb") as f:
                    f.write(await resp.read())
                return filename
    return None

def download_facebook_video(vid_id: str, output_dir: str = "downloads", cookies: str = "cookies.txt"):
    """
    Downloads a Facebook video and returns the local file path.

    Args:
        vid_id (str): Facebook video ID.
        output_dir (str): Directory where the video will be saved.
        cookies (str): Path to cookies.txt file (needed for private videos).

    Returns:
        str: Path to the downloaded video file.
        None: If download failed.
    """
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "%(id)s.%(ext)s")

    ydl_opts = {
        "outtmpl": output_path,
        "quiet": True,
        "no_warnings": True,
        "format": "mp4/best",
    }

    # add cookies if file exists
    if cookies and os.path.exists(cookies):
        ydl_opts["cookiefile"] = cookies

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"https://facebook.com/watch/?v={vid_id}", download=True)
        return ydl.prepare_filename(info)
