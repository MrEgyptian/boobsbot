import os, asyncio,time
from telethon import events, Button
from functions.ytscraper import download_video
from io import BytesIO as ByteIO
async def execute(event, args):
        video_id = args
        url = f"https://www.youtube.com/watch?v={video_id}"
        event.client.tasks[event.sender_id] = {"url": url, "type": "ytvid","last_percent":-1}
        event.client.tasks[event.sender_id] = {"url": url, "type": "ytvid","last_time":int(time.time())}

        await event.answer("⏳ Downloading video...", alert=False)

        cancelled = False
        #event.client.tasks.get(event.sender_id, {})={}
        async def progress(current, total):
         print(current)
         last_percent=event.client.tasks.get(event.sender_id, {}).get("last_percent", -1)
         last_time=event.client.tasks.get(event.sender_id, {}).get("last_time", int(time.time()))
         cancelled=event.client.tasks.get(event.sender_id, {}).get("cancelled", False)
         if cancelled:
            raise Exception("Upload cancelled by user.")
         percent = int(current * 100 / total)
         if int(time.time())-last_time<5:
           return
         if percent == last_percent:
            return
         last_percent = percent
         last_time=event.client.tasks.get(event.sender_id, {}).get("last_time", int(time.time()))
         event.client.tasks[event.sender_id]["last_percent"]=percent
         print(f"Upload progress: {percent}%")
         bar_length = 20  # adjust length of bar
         bar = "█" * (percent * bar_length // 100) + "░" * (bar_length - (percent * bar_length // 100))
         await progress_msg.edit(f"📤 Uploading...\n[{bar}] {percent}%", buttons=[
            [Button.inline("Cancel", data="cancel_upload")]
          ])
        #
        if 1:
            file_path,vid_info = download_video(video_id)
            progress_msg = await event.respond("📤 Starting Download...")
            
            print(file_path,vid_info)
            f=open(file_path,'rb')
            f2send=ByteIO(f.read())
            f.close()
            f2send.name=os.path.basename(file_path)
            print("Prepared file for sending:", f2send.name)

            #await event.respond(
            #    file=file_path,
            #    message=f"🎥 **Video Downloaded:** {vid_info['title']}",
#        part_size_kb=512,     # bigger chunks
#        upload_threads=8      # parallel upload
            #)
            
            #os.remove(file_path)
            print(event.chat_id)
            try:
             async with event.client.action(event.chat_id, 'video'):
               await event.client.send_file(event.chat_id,
                 file=f2send,
                 progress_callback=progress,
                 supports_streaming=True,
                 caption=f"🎬 **Video Downloaded:** {vid_info['title']}"
                 )
            except Exception as e:
               await event.reply(f"❌ {str(e)}")
               print("Error during sending file:", str(e))
               return

         #except Exception as e:
         #   await event.answer(f"❌ Error: {str(e)}", alert=True)
         #   print(e)
