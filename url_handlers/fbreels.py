from telethon import events, Button
import json, logging, aiohttp, asyncio, os,re
from functions.utils import download_image, escape ,resolve_share_url
from functions.fbscraper import fetch_facebook_info   
def register(client):

    @client.on(events.NewMessage(pattern=\
                                 #r"^(https?:\/\/(?:www\.)?facebook\.com\/"
                                 #r"(?:watch\/\?v=(?P<id1>\d+)"
                                 #r"|[^\/]+\/videos\/(?P<id2>\d+)"
                                 #r"|share\/v\/(?P<shareid>[\w-]+)\/?))"
                                 #r"|reels?\/(?P<reelid>\d+))\/?)"
                                 #r"|reel?\/(?P<reelid>\d+))\/?)"
                                 r"^(https?:\/\/(?:www\.|m\.)?facebook\.com\/"
                                 r"(?:watch\/\?v=(?P<id1>\d+)"
                                 r"|watch\?v=(?P<id3>\d+)"
                                 r"|[^\/]+\/videos\/(?P<id2>\d+)"
                                 r"|share\/.\/(?P<shareid>[\w-]+)"
                                 r"|reels?\/(?P<reelid>\d+))\/?)"
                                 
                                 ))
    async def video_handler(event):
        url = event.pattern_match.group(1)
        pattern_match=None
        sid=event.pattern_match.group("shareid")
        if sid:
            resolved_url = await resolve_share_url(url)
            print("🔗 Resolved Share URL:", resolved_url)
            url = resolved_url
            pattern_match = re.match(
            r"^(https?:\/\/(?:www\.|m\.)?facebook\.com\/"
            r"(?:watch\/\?v=(?P<id1>\d+)"
            r"|[^\/]+\/videos\/(?P<id2>\d+)"
            r"|watch\?v=(?P<id3>\d+)"
            r"|share\/v\/(?P<shareid>[\w-]+)"
            r"|reel?\/(?P<reelid>\d+)"
            r")\/?)"
           , url)
        if pattern_match:
                video_id = pattern_match.group("id1") or \
                           pattern_match.group("id2") or \
                           pattern_match.group("id3") or \
                           pattern_match.group("reelid")
        else:
            video_id = event.pattern_match.group("id1") or \
                   event.pattern_match.group("id2") or \
                   event.pattern_match.group("id3") or \
                   event.pattern_match.group("reelid")
        if not video_id:
            return await event.respond("❌ Could not find video in the URL.")
        #print('triggered', video_id)
        
        #print("📘 Facebook Video triggered:", video_id)

        # Fetch info from your Facebook scraper
        info = fetch_facebook_info(f"https://facebook.com/watch/?v={video_id}")
        #"facebook.com/watch/?v=24440056172287357"
        uploader = info.get("uploader") or "N/A"
        title = info.get("title") or "N/A"
        duration = info.get("duration") or "N/A"
        thumbnail = info.get("thumbnail")
        view_count = info.get("view_count", "N/A")
        like_count = info.get("like_count", "N/A")
        uploader_url = info.get("uploader_url", url)

        logging.info(thumbnail)
        logging.info(info)
        #title=title[:500]
        message = (
            f"📘 **Facebook Video Info** 🎥\n"
            f"🆔 **Video ID:** `{video_id}`\n"
            f"📺 **Title:** {title}\n"
            f"⏱️ **Duration:** {duration}\n"
            f"👍 **Likes:** {like_count}\n"
        )

        img = await download_image(thumbnail)
        btns = []
        row1 = [
            Button.inline("🎥 Download Video", data=f"download_fb_video {video_id}")
        ]
        row2 = [
            Button.url("👤 Uploader", url=uploader_url),
            Button.url("▶️ Watch on Facebook", url=url)
        ]
        row3 = [
            Button.inline("ℹ️ More Info", data=f"info_fb_{video_id}")
        ]
        btns.extend([row1, row2, row3])

        if img:
            await event.respond(
                file=img,
                message=message[:1000],
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
