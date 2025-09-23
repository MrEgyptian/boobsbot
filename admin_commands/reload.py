import asyncio
async def execute(event,client, strings):
    msg="""
🔄 Reloading...  
"""
    await event.reply(msg)
    asyncio.sleep(5)
    msg="""
✅ Bot restarted successfully!  
📌 All services are back online."""
    await event.reply(msg)
    client.reload_bot()