from telethon import Button
from io import BytesIO
import aiohttp
def escape(text):
            # Escape characters for Telegram MarkdownV2
            escape_chars = r"_*`["
            return ''.join(['\\' + c if c in escape_chars else c for c in str(text)])
async def resolve_share_url(url: str) -> str:
    """
    Resolve tt/fb links without share in them to direct links.
    Returns the resolved URL.
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, allow_redirects=True) as resp:
                return str(resp.url)  # final URL after redirects
    except Exception as e:
        print(f"[resolve_share_url] Error: {e}")
        return url  # fallback to original

async def download_image(url):
    """
    Downloads an image from the given URL and returns it as a BytesIO object.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                img_bytes = await resp.read()
                img=BytesIO(img_bytes)
                img.name = 'thumbnail.jpg'
                return img
            else:
                raise Exception(f"Failed to download image: {resp.status}")

async def send_paginated_message(client, chat_id, data_dict, page=0, page_size=5, message_id=None):
    """
    Sends a paginated message using Telethon.
    data_dict: list of dicts with keys 'id', 'thumbnail_url', 'text'
    page: current page number (0-indexed)
    page_size: number of items per page
    message_id: if set, edits the message instead of sending a new one
    """
    total_items = len(data_dict)
    total_pages = (total_items + page_size - 1) // page_size
    start = page * page_size
    end = start + page_size
    items = data_dict[start:end]

    text = ""
    buttons = []
    for item in items:
        text += f"**{item['text']}**\n"
        text += f"[Thumbnail]({item['thumbnail_url']})\n"
        text += f"ID: `{item['id']}`\n\n"
        buttons.append([Button.inline(f"Select {item['id']}", data=f"select_{item['id']}")])

    nav_buttons = []
    if page > 0:
        nav_buttons.append(Button.inline("⬅️ Prev", data=f"page_{page-1}"))
    if page < total_pages - 1:
        nav_buttons.append(Button.inline("Next ➡️", data=f"page_{page+1}"))
    if nav_buttons:
        buttons.append(nav_buttons)

    if message_id:
        await client.edit_message(chat_id, message_id, text, buttons=buttons, link_preview=False)
    else:
        await client.send_message(chat_id, text, buttons=buttons, link_preview=False)
def get_best_video(data: dict):
    best = None
    print(data['formats'])
    for fmt in data.get("formats", []):
        if fmt.get("vcodec") == "none":
            continue  # Skip audio-only formats
        if fmt.get("acodec") == "none":
            continue  # Skip video-only formats
        if fmt.get("protocol") in ["m3u8", "f4m", "rtmp"]:
            continue  # Skip streaming formats
        if not fmt.get("height") and not fmt.get("width") and not fmt.get("fps"):
            continue  # Skip formats without resolution info
        if fmt.get("ext") in ["webm", "flv"]:
            continue  # Skip less common formats
        if fmt.get("height") == 0 and fmt.get("width") == 0 and fmt.get("fps") == 0:
            continue  # Skip formats with zero resolution
        if fmt.get("ext") == "m3u8":
            continue  # Skip HLS formats
        if fmt.get("ext") == "f4m":
            continue  # Skip HDS formats
        if str(fmt.get("format_id")) in ["301","91"]:
            continue  # Skip 301 format which is DASH audio
        if fmt.get("protocol") == "m3u8" or fmt.get("ext") == "m3u8":
                    continue  # Skip HLS formats
        if fmt.get("url").endswith(".m3u8"):
            continue  # Skip HLS URLs
            #continue  # Skip formats without URL
        if not fmt.get("ext")=='mp4':
            continue  # Skip formats without URL
        print(fmt)
        # Prefer ones with resolution info
        height = fmt.get("height") or 0
        width = fmt.get("width") or 0
        fps = fmt.get("fps") or 0

        # Candidate tuple for comparison
        score = (height, width, fps)

        if best is None or score > (
            best.get("height") or 0,
            best.get("width") or 0,
            best.get("fps") or 0,
        ):
            best = fmt
            print("New best format found:", best)

    return best
