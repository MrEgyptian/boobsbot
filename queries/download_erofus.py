import os
import asyncio,time

from functions.utils import escape,download_image
from functions.erofus import download_erofus_page
from telethon import Button
async def execute(event, args):
    taskid=int(args)
    await event.answer("⏳ Downloading EroFus comic...", alert=False)

    task=event.client.tasks.get(event.sender_id, {}).get(taskid)
    if not task:
        return await event.edit("ℹ️ You have no ongoing EroFus download tasks to procceed.")
    pages=task['info'].get('pages',[])
    downloaded_pages=[]
    async with event.client.action(event.chat_id, "photo"):
     for i in range(len(pages)):
        page=pages[i]
        if event.client.tasks.get(event.sender_id, {}).get(taskid,{}).get("cancelled"):
            return await event.edit("❌ Your EroFus download task has been cancelled.")
        #downloaded_pages.append(await download_erofus_page(page)
        p=await download_erofus_page(page)
        if p:
            downloaded_pages.append(p)
        #if len(downloaded_pages)//10==0
        await asyncio.sleep(0.2)  # to avoid hitting rate limits
        
     await event.client.send_file(event.sender_id, downloaded_pages, caption="✅ Here is your downloaded EroFus comic")
    if event.client.tasks.get(event.sender_id, {}).get(taskid):
        del event.client.tasks[event.sender_id][taskid]
