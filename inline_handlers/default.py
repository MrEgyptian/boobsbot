
from telethon import events,Button
import json,logging,aiohttp,asyncio,os
from functions.utils import get_best_video
from functions.utils import download_image,escape

def register(client):

    @client.on(events.InlineQuery)
    async def handler(event):
           builder = event.builder
           print(dir())
           results = [
               builder.article(
                title="Grow your boobs!",
                description="Increase your 🍒 size",
                text="🍒 Click button below to grow your boobiees ^_^",
                buttons=[Button.inline("Grow now!", "grow")]

            ),
            builder.article(
                title="Get the biggest boobs of the chat",
                description="Show the leaderboard",
                text="🏆 Biggest boobs leaderboard coming soon...",
                #query='xx',
                buttons=[Button.switch_inline("Grow now!", query="grow")]

            ),
            builder.article(
                title="Elect the Boobs of the Day",
                description="Vote for today’s champion",
                text="👑 Today’s Boobs of the Day: TBD!",
                buttons=[Button.switch_inline("Grow now!", query="grow")]

            ),
            builder.article(
                title="Flat? Take a loan!",
                description="Get a boob loan",
                text="💳 You got a +5 cm loan!",
                buttons=[Button.switch_inline("Grow now!", query="grow")]

            ),
            builder.article(
                title="Win statistics",
                description="See your stats",
                text="📊 Your current size: 12 cm.",
                buttons=[Button.switch_inline("Grow now!", query="grow")]

            ),
            builder.article(
                title="Challenge others with a bet of 5 cm!",
                description="Fight another player",
                text="⚔️ You challenged someone with a 5 cm bet!",
                buttons=[Button.switch_inline("Grow now!", query="grow")]

            ),
        ]
           await event.answer(results)
           pass