import os, asyncio,time,aiohttp
from telethon import events, Button
from functions.ytscraper import download_video
from io import BytesIO

async def execute(event, args):
  video_id = int(args)
  tasks=await event.client.get_tasks(event.sender_id)
  task=tasks.get(video_id)
  print(task)
  best_video=task.get("best_video")
  best_video_url=best_video.get("url")
  async def progress(current, total):
         print(current)
         last_percent=event.client.tasks.get(event.sender_id, {})[video_id].get("last_percent", -1)
         last_time=event.client.tasks.get(event.sender_id, {})[video_id].get("last_time", int(time.time()))
         cancelled=event.client.tasks.get(event.sender_id, {})[video_id].get("cancelled", False)
         if cancelled:
            raise Exception("Upload cancelled by user.")
         percent = int(current * 100 / total)
         if int(time.time())-last_time<5:
           print("Skipping update to avoid spamming", int(time.time())-last_time)
           return
         #event.client.tasks[event.sender_id][video_id]["last_percent"]=last_percent
         if percent == last_percent:
            return
         last_percent = percent
         event.client.tasks[event.sender_id][video_id]["last_percent"]=percent
         last_time=event.client.tasks.get(event.sender_id, {})[video_id].get("last_time", int(time.time()))
         event.client.tasks[event.sender_id][video_id]["last_time"]=last_time
         print(f"Upload progress: {percent}%")
         bar_length = 20
         bar = "█" * (percent * bar_length // 100) + "░" * (bar_length - (percent * bar_length // 100))
         await progress_msg.edit(f"📤 Uploading...\n[{bar}] {percent}%", buttons=[
            [Button.inline("Cancel", data="cancel_upload")]
          ])

  async with event.client.action(event.chat_id, 'video'):
    progress_msg = await event.respond("📤 Starting Download...")
    event.client.tasks[event.sender_id][video_id]["last_time"]=int(time.time())
    connector = aiohttp.TCPConnector(limit_per_host=20, ttl_dns_cache=300,use_dns_cache=True,ssl=False)

    async with aiohttp.ClientSession(connector=connector) as session:
      async with session.get(best_video_url) as response:
        bio = BytesIO()
        bio.name = "video.mp4"
        async for chunk in response.content.iter_chunked(1024 * 1024 * 5):  # 5MB chunks
          bio.write(chunk)
        bio.seek(0)  # rewind before sending
        progress_msg = await progress_msg.edit("📤 Sending the video...")
        await event.client.send_file(event.chat_id, bio, filename="video.mp4", progress_callback=progress, parse_mode='md',part_size_kb=1024,
          caption=f"🎥 **Video Downloaded:** `{task['info']['title']}`"
        )
