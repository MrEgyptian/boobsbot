import os, yt_dlp
def fetch_instagram_info(url: str):
    """Fetch Instagram Reel info using yt-dlp."""
    ydl_opts = {"quiet": True, "skip_download": True, "cookiefile":"cookies.txt"}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
    return info


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

def download_instagram_reel(url: str, output_dir: str = "downloads", cookies: str = "cookies.txt"):
    url = url if url.startswith("http") else f"https://www.instagram.com/reels/{url}/"
    # ydl_opts = {"format": "best","quiet": True, "skip_download": False}
    ydl_opts = {
        "cookiefile": cookies,
        "format": "bv+ba/b",  # best video+audio
        "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
        "n_threads": 8,    # speed up downloads
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
         info = ydl.extract_info(url, download=True)
         fname=ydl.prepare_filename(info)
         return fname
    return
    #os.makedirs(output_dir, exist_ok=True)
    #print("Downloading Instagram Reel from:", url)
    

#    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#        ydl.download([url])
    