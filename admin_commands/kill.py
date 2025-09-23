import sys
async def execute(event,client, strings):
    await event.reply("🛑 Shutting down... Bye! 👋")
    await client.disconnect()
    sys.exit(0)