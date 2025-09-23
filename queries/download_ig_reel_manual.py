import os, asyncio
from functions.igscraper import download_instagram_reel

async def execute(event, args):
        reel_url = args
        await event.answer("⏳ Downloading reel...", alert=False)

        try:
            file_path = download_instagram_reel(reel_url)
            print("Downloaded file path:", file_path)
            async with event.client.action(event.chat_id, 'upload_video'):
             await event.respond(
                file=file_path,
                message=f"🎵 **Reel Downloaded:** {reel_url}"
             )
            os.remove(file_path)
        except Exception as e:
            await event.answer(f"❌ Error: {str(e)}", alert=True)
