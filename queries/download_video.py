import os, asyncio
from io import BytesIO as ByteIO
from functions.universal import download_video
from telethon import Button

async def execute(event, args):
    await event.answer("⏳ Downloading video...", alert=False)
    
    video_url = event.client.tasks.get(event.sender_id, {}).get("url")
    if not video_url:
        return await event.reply("❌ No video URL found to download.")

    progress_msg = await event.respond("📤 Starting Download...")

    cancelled = False
    async def progress(current, total):
        last_percent=event.client.tasks.get(event.sender_id, {}).get("last_percent", -1)
        cancelled=event.client.tasks.get(event.sender_id, {}).get("cancelled", False)
        if cancelled:
            raise Exception("Upload cancelled by user.")
        percent = int(current * 100 / total)
        if percent == last_percent:
            return
        last_percent = percent
        event.client.tasks[event.sender_id]["last_percent"]=percent
        print(f"Upload progress: {percent}%")
        bar_length = 20  # adjust length of bar
        bar = "█" * (percent * bar_length // 100) + "░" * (bar_length - (percent * bar_length // 100))
        await progress_msg.edit(f"📤 Uploading...\n[{bar}] {percent}%", buttons=[
            [Button.inline("Cancel", data="cancel_upload")]
        ])

    #event.client.tasks[event.sender_id] = {"url": video_url, "type": "universal"}
    if 1:
        file_path = download_video(video_url)
        #print("Downloaded file path:", file_path)
        f=open(file_path,'rb')
        f2send=ByteIO(f.read())
        f.close()
        f2send.name=os.path.basename(file_path)
        print("Prepared file for sending:", f2send.name)
        #fid=await fast_upload(event.client, f2send, progress_bar_function=progress)
        try:
            await event.client.send_file(event.chat_id,
                 file=f2send,
                progress_callback=progress,
                supports_streaming=True,
                caption=f"🎬 **Video Downloaded:** {video_url}"
            )
        except Exception as e:
            await event.reply(f"❌ {str(e)}")
            print("Error during sending file:", str(e))
            return
        #fid=await fast_upload(event.client, file_path, progress_bar_function=progress)
        #print("Uploaded file id:", fid)
        #await event.respond(f"🎬 **Video Downloaded:** {video_url}")
        #await event.client.send_message(fid)
        #os.remove(file_path)  # cleanup after sending
 