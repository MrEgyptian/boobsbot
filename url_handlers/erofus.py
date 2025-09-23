
from telethon import events,Button
import json,logging,aiohttp,asyncio,os
from functions.utils import get_best_video
from functions.erofus import get_comic_info
from functions.utils import download_image,escape
def register(client):

    @client.on(events.NewMessage(pattern = r"^https?:\/\/(?:www\.)?erofus\.com/comics/(?P<series>[^/]+)(?:/(?P<subdir>[^/]+))?(?:/(?P<slug>[^/]+))?(?:/(?P<issue>[^/?#]+))?/?$"))
    async def comic_handler(event):
        slug= comic = event.pattern_match.group("slug")
        series=event.pattern_match.group("series")
        subdir=event.pattern_match.group("subdir")
        issue=event.pattern_match.group("issue")
        comic_author = subdir or series
       
        tasks=await client.get_tasks(event.sender_id)
        btns=[]
        if(len(tasks)>0):
            for taskid in tasks:
                task=tasks[taskid]
                btns+=[
                    Button.inline(escape(f"⏳ {task['type']} {task['url']}"), data=f"view_task {taskid}"),
                    Button.inline(escape(f"❌ Cancel all {task['type']}"), data=f"cancel_{task['type']}"),
                    Button.inline("❌ Cancel", data=f"cancel_task {taskid}")
                ]
            return await event.reply("you're already processing a task ,please wait or cancel it first",buttons=[
                [*btns],
                [Button.inline("❌ Cancel all tasks", data=f"cancel_all")]
            ])
        
        print('triggered',series,subdir,slug,issue)
        if issue:
            url=f"https://www.erofus.com/comics/{series}/{subdir}/{slug}/{issue}"
        elif slug:
            url=f"https://www.erofus.com/comics/{series}/{subdir}/{slug}"
        else:
            comic=subdir
            comic_author=series
            url = f"https://www.erofus.com/comics/{series}/{subdir}"
        
        print(url)

        info = await get_comic_info(url)
        print("📸 EroFus Comic triggered:", url)
        
        thumbnail = info.get("thumbnail")
        logging.info(thumbnail)
        tags=[f"#{t}" for t in info.get("tags", [])]
        if info['page_count']==0:
            message = (
                        f"📸 **EroFus Comic Info** 🎶\n"
                        f"👤 **Author:** {comic_author}\n"
                        f"📺 **Comic:** {comic}\n"
                        f"▶️ **Read Comic:** [link]({url})\n"
                        f"🗂️ **Tags:** {', '.join(tags)}"
                    )
            chapters=info['chapters']
            #print(chapters)
            
            client.erofus[comic]={'url':url,'chapters':chapters}
            btns=[]
            for i in range(len(chapters)):
             btns.append([Button.inline(f'Download Chapter {i}',f'erofus_ch {comic} {i}'),
                          Button.url(f"Read chapter {i}",chapters[i])
                          ])
            try:
             img = await download_image(thumbnail)

             await event.reply(message,file=img,buttons=btns)
            except Exception as e:
                await event.reply(message)
        else:
            message = (
                        f"📸 **EroFus Comic Info** 🎶\n"
                        f"👤 **Author:** {comic_author}\n"
                        f"📺 **Comic:** {comic}\n"
                        f"▶️ **Read Comic:** [link]({url})\n"
                        f" 📄 Pages count {info['page_count']}\n"
                        f"🗂️ **Tags:** {', '.join(tags)}"
                    )
            await client.add_task(event.sender_id, "erofus", url, id=event.id, info=info)
            if thumbnail:
                img = await download_image(thumbnail)
                btns = []
                row1 = [
                                Button.inline("⬇️ Download Comic", data=f"download_erofus {event.id}"),
                                Button.url("📖 Read Comic", url),
                                Button.url("👤 Author", f"https://www.erofus.com/{comic_author}"),
                            ]
                btns.append(row1)
                await event.reply(message, buttons=btns, file=img)
            else:
                await event.reply(message, buttons=Button.url("📖 Read Comic", url))