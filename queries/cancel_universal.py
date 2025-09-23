async def execute(event, args):
    await event.answer("❌ Cancelling your ongoing task...", alert=False)
    user_tasks = event.client.tasks.get(event.sender_id, {})
    if "url" in user_tasks and user_tasks["type"] == "universal":
        del event.client.tasks[event.sender_id]
        await event.edit("✅ Your ongoing task has been cancelled.")
    else:
        await event.edit("ℹ️ You have no ongoing universal download tasks to cancel.")