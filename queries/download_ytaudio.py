import os, asyncio,logging
from functions.ytscraper import download_audio

async def execute(event, args):
        video_id = args
        await event.answer("⏳ Downloading audio...", alert=False)

        try:
            file_path = download_audio(video_id)
            logging.info(f"downloaded to {file_path}.")

            await event.respond(
                file=file_path,
                message=f"🎵 **Audio Downloaded:** {video_id}",
                #part_size_kb=512,     # bigger chunks
                #upload_threads=8      # parallel upload
                #workers=8,
            )
            logging.info(f"done ")
            os.remove(file_path)
        except Exception as e:
            await event.answer(f"❌ Error: {str(e)}", alert=True)
