import os
import asyncio,time,re

from functions.utils import escape,download_image
from functions.erofus import download_erofus_page
from telethon import Button
from functions.erofus import get_comic_info

async def execute(event, args):
    comic,chapter=args.split(" ")
    print('hi',comic,chapter)
    event.answer('wait...')
    chapter=int(chapter)
    url=event.client.erofus[comic]['chapters'][chapter]
    info=await get_comic_info(url)
    event.pattern_match=re.match(r"^https?:\/\/(?:www\.)?erofus\.com/comics/(?P<series>[^/]+)(?:/(?P<subdir>[^/]+))?(?:/(?P<slug>[^/]+))?(?:/(?P<issue>[^/?#]+))?/?$",url)
    slug= comic = event.pattern_match.group("slug")
    series=event.pattern_match.group("series")
    subdir=event.pattern_match.group("subdir")
    issue=event.pattern_match.group("issue")
    comic_author = subdir or series
    tags=info['tags']
    message = (
                        f"📸 **EroFus Comic Info** 🎶\n"
                        f"👤 **Author:** {comic_author}\n"
                        f"📺 **Comic:** {comic}\n"
                        f"▶️ **Read Comic:** [link]({url})\n"
                        f" 📄 Pages count {info['page_count']}\n"
                        f"🗂️ **Tags:** {', '.join(tags)}"
                    )
    thumbnail = info.get("thumbnail")
    #url=info['webpage_url']
    await event.client.add_task(event.sender_id, "erofus", url, id=event.id, info=info)
    if thumbnail:
        img = await download_image(thumbnail)
        btns = []
        row1 = [
                    Button.inline("⬇️ Download Comic", data=f"download_erofus {event.id}"),
                    Button.url("📖 Read Comic", url),
                    Button.url("👤 Author", f"https://www.erofus.com/{comic_author}"),
                ]
        btns.append(row1)
        print(message,chapter)
        await event.reply(message, buttons=btns, file=img)
    else:
        await event.reply(message, buttons=Button.url("📖 Read Comic", url))