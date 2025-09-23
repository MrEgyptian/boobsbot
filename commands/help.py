async def execute(event, client, strings):
    help_text = (
"""
👋 **Welcome to BoobsGrowingBot!**

Do you want to grow the **biggest boobs** in the world?  
I’m sure you do! Just use **/grow** once a day in every chat you’re in to start your journey.  
Climb the leaderboard and show off your curves! 💖

✨ **How it works:**  
- Each /grow gives you between **-2 cm and +10 cm** of growth.  
- Use **/top** to check who has the biggest boobs in your chat.  
- Every day, one lucky player is crowned **Boobs of the Day** with bonus growth!  

🔥 **Extra Features:**  
- **/pvp** → Challenge your friends and bet centimeters. Winner grows, loser shrinks.  
- **/import** → Bring progress from other bots.  
- **/loan** → Reset your size to 0 if you’re too deep in negatives.  
- Play even without adding the bot to groups using **inline mode**: type `@boobsgrowingbot` + space.  

💬 Use **/faq** for more detailed info.  
💖 Use **/support** if you’d like to help keep this bot alive.  

Now go out there and grow! 🌱
"""
    )
    await event.reply(help_text)
