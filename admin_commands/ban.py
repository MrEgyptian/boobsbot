import re

async def wrong_usage_msg(event):
    msg = """❌ Incorrect command usage!  
To ban a user, use:  

✅ `/ban @username`  
✅ `/ban user_id`  

📌 **Examples:**  
🔹 `/ban @example_user`  
🔹 `/ban 123456789`  

🔍 Check banned users with `/banned`.  
🔄 Use `/refresh` to update the list.  
➕ Unban a user with `/unban @username` if needed.

"""
    await event.reply(msg)

async def invalid_user(event, userid):
    msg = f"""⚠️ Cannot ban user `{userid}` because they are already banned or invalid!  

🔄 Use `/refresh` to clean up the database.  
📋 Check banned users with `/banned`.
➕ Unban a user with `/unban @username` if needed.
"""
    await event.reply(msg)

async def banned_user(event, userid):
    msg = f"""🚫 User `{userid}` has been successfully banned from using the bot! ✅
 
🔄 Use `/refresh` to update the list.  
📋 Check all banned users with `/banned`.  
➕ Unban a user with `/unban @username` if needed.
"""
    await event.reply(msg)

async def execute(event, client, strings):
    if len(event.args) == 0:
        await wrong_usage_msg(event)
    else:
        try:
            try:
                userid = int(event.args)
            except:
                userid = await client.get_entity(event.args)
                userid = userid.id
            event.db.ban_user(userid)
            await banned_user(event, userid)
        except Exception as e:
            print(e)
            await invalid_user(event, event.args)
