async def execute(event, client, strings):
    FAQ_MESSAGE = """
❓ **Frequently Asked Questions (FAQ)** ❓

**Q: How do I start playing?**  
A: Just type **/start** and then use **/grow** once a day in any chat to begin growing!  

**Q: How much can I grow per day?**  
A: Each /grow gives you between **-2 cm and +10 cm**. Growth is random, so keep at it daily!  

**Q: What is /top?**  
A: The **/top** command shows the players with the biggest boobs in your current chat.  

**Q: What is "Boobs of the Day"?**  
A: Every day, one active player is randomly crowned **Boobs of the Day**, earning bonus growth. To qualify, you must have grown at least once in the past week.  

**Q: Can I fight other players?**  
A: Yes! Use **/pvp** to challenge friends and bet centimeters. Winner grows bigger, loser shrinks.  

**Q: I’m stuck in the negatives! What now?**  
A: You have two options:  
1️⃣ Every growth will get a **+0.1% boost** until you recover.  
2️⃣ Use **/loan** to reset your size to zero instantly, and pay it back with each growth.  

**Q: Can I bring my stats from another bot?**  
A: Yes! Use **/import** (as a reply to another bot’s leaderboard message). Your progress will be added on top of your current stats.  

**Q: Do I need the bot in group chats?**  
A: Not necessarily! You can also play with **inline mode**. Just type `@boobsgrowingbot` in any chat and access commands without adding the bot.  

**Q: Will you spam chats with ads?**  
A: No 🚫 This bot will never flood your chats with ads like others do.  

**Q: Who do I contact if I have issues?**  
A: Reach out at **@YourSupportUsername** for support or feedback.  
"""

    await event.reply(FAQ_MESSAGE)
