
from telethon import events,Button
import json,logging,aiohttp,asyncio,os
from functions.utils import get_best_video
from functions.utils import download_image,escape
from functions.igscraper import fetch_instagram_info
def register(client):

    @client.on(events.NewMessage(pattern = r"^(?:https?:\/\/)?(?:www\.)?instagram\.com\/reels?\/([a-zA-Z0-9_-]+)"))
    async def video_handler(event):
        reel_id = event.pattern_match.group(1)
        tasks=await client.get_tasks(event.sender_id)
        btns=[]
        if(len(tasks)>0):
            for taskid in tasks:
                task=tasks[taskid]
                btns.append([
                    Button.inline(escape(f"⏳ {task['type']} {task['url']}"), data=f"view_task {taskid}"),
                    Button.inline(escape(f"❌ Cancel all {task['type']}"), data=f"cancel_{task['type']}"),
                    Button.inline("❌ Cancel", data=f"cancel_task {taskid}")
                ])
            return await event.reply("you're already processing a task ,please wait or cancel it first",buttons=[
                [*btns],
                [Button.inline("❌ Cancel all tasks", data=f"cancel_all")]
            ])
        
        print('triggered',reel_id)
        url = f"https://www.instagram.com/reels/{reel_id}/"
        
        print("📸 Instagram Reel triggered:", url)

        info = fetch_instagram_info(url)

        uploader = info.get("uploader") or "N/A"
        title = info.get("title") or "N/A"
        duration = info.get("duration") or "N/A"
        thumbnail = info.get("thumbnail")
        view_count = info.get("view_count", "N/A")
        like_count = info.get("like_count", "N/A")
        uploader_url = info.get("uploader_url", url)

        logging.info(thumbnail)
        #logging.info(info)
        message = (
            f"📸 **Instagram Reel Info** 🎶\n"
            f"🆔 **Reel ID:** `{reel_id}`\n"
            f"👤 **Uploader:** {uploader}\n"
            f"📺 **Title:** {title}\n"
            f"⏱️ **Duration:** {duration}\n"
            f"👍 **Likes:** {like_count}\n"
            f"👥 **Uploader URL:** [link]({uploader_url})\n"
            f"▶️ **Watch Reel:** [link]({url})"
        )
        best_video = get_best_video(info)
        await client.add_task(event.sender_id, "igreel", url,best_video=best_video,id=event.id,info=info)
        logging.info("Best video format: %s", best_video)
        
        img = await download_image(thumbnail)
        btns = []
        row1 = [
            #Button.inline("🎵 Download Audio", data=f"download_ig {reel_id}"),
            Button.inline("🎥 Download reel", data=f"download_ig_reel {event.id}")
        ]
        row2 = [
            Button.url("👤 Uploader", url=uploader_url),
            Button.url("▶️ Watch on Instagram", url=url)
        ]
        row3 = [
            Button.inline("ℹ️ More Info", data=f"info_insta_{reel_id}")
        ]
        btns.extend([row1, row2, row3])

        if img:
            await event.respond(
                file=img,
                message=message,
                buttons=btns
            )
            #os.remove(img)
        else:
            message += "\n\n(Note: Thumbnail not available)"
            await event.respond(
                message=message,
                buttons=btns
            )
            pass