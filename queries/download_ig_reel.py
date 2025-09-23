import os, asyncio
from functions.igscraper import download_instagram_reel

async def execute(event, args):
        reel_id = args
        if not str(reel_id).isdigit():
            await event.answer("⏳ Downloading reel...", alert=False)
            try:
                file_path = download_instagram_reel(reel_id)
                print(reel_id)
                print(file_path)
                async with event.client.action(event.chat_id, 'video'):
                    await event.client.send_file(
                    file=file_path,
                    message=f"🎵 **Reel Downloaded:** {reel_id}"
                    )
                os.remove(file_path)
            except Exception as e:
                await event.answer(f"❌ Error: {str(e)}", alert=True)
        else:
            reel_id = int(reel_id)
            await event.answer("⏳ Downloading reel...", alert=False)
            async with event.client.action(event.chat_id, 'video'):
              vid=await event.client.get_tasks(event.sender_id)
              info=vid[reel_id]['info']
              vid=vid[reel_id]['best_video']['url']
              print(vid)
              #await event.respond(str(vid))
              await event.client.send_file(event.chat_id,file=vid,message=f"🎥 **Reel Downloaded:** `{info['title']}`")
              del event.client.tasks[event.sender_id][reel_id]
              
            