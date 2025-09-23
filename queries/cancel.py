async def execute(event, args):
    taskid=int(args)
    await event.answer("❌ Cancelling your ongoing task...", alert=False)
    user_tasks = event.client.tasks.get(event.sender_id, {})
    if taskid in user_tasks:
        del event.client.tasks[event.sender_id][taskid]
        await event.edit("✅ Your ongoing task has been cancelled.")
    else:
        await event.edit("ℹ️ You have no ongoing universal download tasks to cancel.")