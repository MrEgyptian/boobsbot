import os
import asyncio,time
from functions.fbscraper import download_facebook_video
from telethon import Button
async def execute(event, args):
    video_url = args
    url=f"https://facebook.com/watch/?v={video_url}"
    await event.answer("⏳ Downloading Facebook video...", alert=False)
    progress_msg = await event.respond("📤 Starting download...")
    event.client.tasks[event.sender_id] = {"url": url, "type": "fbvid","last_percent":-1}
    event.client.tasks[event.sender_id]['last_time'] = int(time.time())
    print(event.client.tasks[event.sender_id]['last_time'])
    async def progress(current, total):
        last_percent=event.client.tasks.get(event.sender_id, {}).get("last_percent", -1)
        cancelled=event.client.tasks.get(event.sender_id, {}).get("cancelled", False)
        last_time=event.client.tasks[event.sender_id]['last_time']
        if cancelled:
            raise Exception("Upload cancelled by user.")
        percent = int(current * 100 / total)
        if int(time.time())-last_time<5:
            #print('wait',int(time.time()),last_time)
            return

        if percent == last_percent:
            return
        last_percent = percent
        event.client.tasks[event.sender_id]["last_percent"]=percent
        event.client.tasks[event.sender_id]["last_time"]=int(time.time())
        print(f"Upload progress: {percent}%")
        bar_length = 20  # adjust length of bar
        bar = "█" * (percent * bar_length // 100) + "░" * (bar_length - (percent * bar_length // 100))
        await progress_msg.edit(f"📤 Uploading...\n[{bar}] {percent}%", buttons=[
            [Button.inline("Cancel", data="cancel_upload")]
        ])

    try:
        #event.client.tasks[event.sender_id] = {"url": video_url, "type": "Facebook"}
        file_path = download_facebook_video(video_url)
        print("Downloaded file path:", file_path)
        try:
           async with event.client.action(event.chat_id, 'video'):
            await event.client.send_file(event.chat_id,
                file=file_path,
                progress_callback=progress,
                supports_streaming=True,
                )
        except Exception as e:
            await event.reply(f"❌ {str(e)}")
            return
        # await event.respond(
        #     file=file_path,
        #     message=f"🎥 **Facebook Video Downloaded:** {video_url}"
        # )

        #os.remove(file_path)

    except Exception as e:
        await event.answer(f"❌ Error: {str(e)}", alert=True)
