from telethon import events,Button
from functions.ytscraper import fetch_playlist_info_by_id,fetch_video_info_by_id
import json,logging,aiohttp,asyncio
from functions.utils import download_image,escape, get_best_video
def register(client):
    @client.on(events.NewMessage(pattern=r"^(?:https?:\/\/)?(?:www\.)?youtube\.com\/(?:playlist\?list=|watch\?.*?[&?]list=)([a-zA-Z0-9_-]+)"))
    async def start_handler(event):
        playlist_id = event.pattern_match.group(1)
        print('triggered')
        info = fetch_playlist_info_by_id(playlist_id)
        uploader = info.get("uploader")
        title = info.get("title")
        vids=info.get("entries", [])
        videos_count = len(vids)
        ch_id=info.get("channel_id", "")
        channel=info.get("channel", "")
        thumbs=info.get("thumbnails", [])
        best_thumb = max(thumbs, key=lambda x: x["width"] * x["height"])
        thumbnail=best_thumb.get("url","")
        print(thumbnail)
        channel_url=info.get("channel_url", "")
        uploader_url=info.get("uploader_url", "")
        json_info = json.dumps(info, indent=2)
        #logging.info(f"Fetched info for playlist {playlist_id}: {json_info}")
        logging.info(thumbnail)
        
        message = (
            f"🎬 **Playlist Info** 🎶\n"
            f"🆔 **Playlist ID:** `{playlist_id}`\n"
            f"👤 **Uploader:** {uploader if uploader else 'N/A'}\n"
            f"📺 **Title:** {title if title else 'N/A'}\n"
            f"🎞️ **Videos Count:** **{videos_count}**\n"
            f"🔗 **Channel ID:** `{ch_id if ch_id else 'N/A'}`\n"
            f"🌐 **Channel URL:** [link]({channel_url})\n"
            f"👥 **Uploader URL:** [link]({uploader_url})"
        )
        img = await download_image(thumbnail)
        btns = []
        row1 = [
            Button.inline("🎵 Download Audios", data=f"download_ytaudio_playlist {playlist_id}"),
            Button.inline("🎥 Download Videos", data=f"download_ytvideo_playlist {playlist_id}")
        ]
        row2 = [
            Button.url("📺 Channel", url=channel_url),
            Button.url("👤 Uploader", url=uploader_url),
            Button.url("📃 View Playlist", url=f"https://www.youtube.com/playlist?list={playlist_id}")
        ]
        row3 = [
            Button.inline("ℹ️ More Info", data=f"info_{playlist_id}")
        ]
        btns.extend([row1, row2, row3])
        if img:
            await event.respond(
            file=img,
            message=message,
            buttons=btns
            )
        else:
            message=message+"\n\n(Note: Thumbnail not available)"
            await event.respond(
            message=message,
            buttons=btns
            )
    #@client.on(events.NewMessage(pattern = r"^(?:https?:\/\/)?(?:www\.)?youtube\.com\/(?:watch\?v=|shorts\/)([a-zA-Z0-9_-]+)"))
    @client.on(events.NewMessage(pattern = r"^(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:watch\?v=|shorts\/)|youtu\.be\/)([a-zA-Z0-9_-]+)"))
    async def video_handler(event):
        video_id = event.pattern_match.group(1)
        print('video triggered')

        info = fetch_video_info_by_id(video_id)
        uploader = info.get("uploader")
        title = info.get("title")
        duration = info.get("duration")
        ch_id = info.get("channel_id", "")
        channel = info.get("channel", "")
        print(info.get("thumbnail"))
        #thumbs = info.get("thumbnails", [])
        #best_thumb = max(thumbs, key=lambda x: x["width"] * x["height"]) if thumbs else {}
        thumbnail = info.get("thumbnail")
        channel_url = info.get("channel_url", "")
        uploader_url = info.get("uploader_url", "")
        view_count = info.get("view_count", "N/A")
        like_count = info.get("like_count", "N/A")

        logging.info(thumbnail)

        message = (
            f"🎬 **Video Info** 🎶\n"
            f"🆔 **Video ID:** `{video_id}`\n"
            f"👤 **Uploader:** {uploader if uploader else 'N/A'}\n"
            f"📺 **Title:** {title if title else 'N/A'}\n"
            f"⏱️ **Duration:** {duration if duration else 'N/A'}\n"
            f"👁️ **Views:** {view_count}\n"
            f"👍 **Likes:** {like_count}\n"
            f"🔗 **Channel ID:** `{ch_id if ch_id else 'N/A'}`\n"
            f"🌐 **Channel URL:** [link]({channel_url})\n"
            f"👥 **Uploader URL:** [link]({uploader_url})"
        )

        img = await download_image(thumbnail)
        btns = []
        row1 = [
            Button.inline("🎵 Download Audio", data=f"download_ytaudio {video_id}"),
            Button.inline("🎥 Download Video", data=f"download_ytvideo {event.id}")
        ]
        row2 = [
            Button.url("📺 Channel", url=channel_url),
            Button.url("👤 Uploader", url=uploader_url),
            Button.url("▶️ Watch on YouTube", url=f"https://www.youtube.com/watch?v={video_id}")
        ]
        row3 = [
            Button.inline("ℹ️ More Info", data=f"info_{video_id}")
        ]
        btns.extend([row1, row2, row3])

        if img:
            await event.client.add_task(event.sender_id, "ytvid", url=None,best_video=get_best_video(info),id=event.id,info=info)
            await event.respond(
                file=img,
                message=message,
                buttons=btns
            )
        else:
            
            message += "\n\n(Note: Thumbnail not available)"
            await event.client.add_task(event.sender_id, "ytvid", url=None,best_video=get_best_video(info),id=event.id,info=info)
            await event.respond(
                message=message,
                buttons=btns
            )
