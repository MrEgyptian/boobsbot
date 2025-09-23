async def execute(event, args):
    event.client.tasks.get(event.sender_id, {})["cancelled"] = True
    await event.answer("❌ Cancelling your upload...", alert=False)
    
