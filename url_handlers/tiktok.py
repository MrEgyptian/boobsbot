from telethon import events, Button
from functions.universal import fetch_video_info
from functions.utils import download_image

def register(client):

    @client.on(events.NewMessage(pattern=\
    r"^(https?:\/\/(?:www\.)?tiktok\.com\/"
    r"@[\w\.]+\/video\/(?P<id>\d+))"
    ))
    async def universal_handler(event):
        url = event.pattern_match.group(1)
        processing_tasks = event.client.tasks.get(event.sender_id, {}).get('url')
        print("Processing tasks:", processing_tasks)
        if processing_tasks:
            return await event.reply("you're already processing a task ,please wait or cancel it first",buttons=[
                [Button.inline("❌ Cancel", data=f"cancel_universal")]
            ])

        try:
            info = fetch_video_info(url)
        except Exception as e:
            
            return

        site = info.get("extractor_key", "Unknown")
        title = info.get("title") or "N/A"
        uploader = info.get("uploader") or "N/A"
        duration = info.get("duration") or "N/A"
        view_count = info.get("view_count", "N/A")
        like_count = info.get("like_count", "N/A")
        thumbnail = info.get("thumbnail")
        video_id = info.get("id")

        message = (
            f"🎬 **{site} Video Info**\n"
            f"🆔 **ID:** `{video_id}`\n"
            f"👤 **Uploader:** {uploader}\n"
            f"📺 **Title:** {title}\n"
            f"⏱️ **Duration:** {duration}\n"
            f"👀 **Views:** {view_count}\n"
            f"👍 **Likes:** {like_count}\n"
            f"▶️ **Watch:** [link]({url})"
        )

        img = await download_image(thumbnail)
        event.client.tasks[event.sender_id] = {"url": url, "type": "universal"}
        btns = [
            [Button.inline("🎥 Download Video", data=f"download_video")],
            [Button.url("▶️ Watch Online", url=url)]
        ]

        if img:
            await event.respond(file=img, message=message, buttons=btns)
        else:
            await event.respond(message=message, buttons=btns)
