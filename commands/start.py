async def execute(event,client, strings):
    msg = ("""
    👋 Hello, !

Do you want to have the **biggest boobs in the world**? I’m sure you do!  
Just use **/grow** once a day in every chat you’re in, and watch your chest expand!  
Get to the top of the leaderboard and show everyone your curves! 💖  

📏 The growth range for the command is between **-5 cm and +7 cm**.  
Use **/top** to see who has the biggest bust in your chat.  

✨ Every day there’s also a daily election of the **Boobs of the Day** in every chat.  
This crown gives its owner **bonus centimeters**.  
Only active players who have grown at least once in the past week participate.  

🔥 Want to take risks for faster growth?  
Challenge your friends with **/pvp**! Place a bet — the winner gets the centimeters, the loser loses them. Simple.  

---

🤔 *Wait, I already know similar bots…*  
Don’t worry! This bot was made as a replacement for spammy competitors.  
I **promise never to flood chats with ads**.  

---

🔗 **Import from other bots**  
Using **/import** (as a reply to another bot’s leaderboard), admins can import already existing stats.  

✔️ To import successfully:  
- The player must already have boobs in this bot.  
- Both lengths are summed (no progress lost).  
- The bot needs temporary admin rights *only* to read the import message (privacy mode stays on).  

---

🙅 *But my group admin doesn’t allow adding bots…*  
No problem! You can still play with **inline queries**:  
Just type `@boobsgrowingbot` + space in any chat to use commands without adding me. """
    )
    await event.reply(msg)
