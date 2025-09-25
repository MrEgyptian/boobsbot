
from telethon import events,Button
import json,logging,aiohttp,asyncio,os
from functions.utils import get_best_video
from functions.utils import download_image,escape
from telethon.tl.types import UpdateBotInlineQuery,UpdateBotInlineSend

def register(client):
    print(dir(events))
    @client.on(events.Raw)
    async def chosen_handler(event):
        print(event.__class__)
        if isinstance(event,UpdateBotInlineQuery):
            print(event)
        #if event.result_id:  # each inline result has an id
            #print(event.result_id)
