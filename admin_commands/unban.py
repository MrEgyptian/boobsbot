import re

async def wrong_usage_msg(event):
    msg = """❌ Incorrect command usage!  
To unban a user, use:  

✅ `/unban @username`  
✅ `/unban user_id`  

📌 **Examples:**  
🔹 `/unban @example_user`  
🔹 `/unban 123456789`  

🔍 Check banned users with `/banned`.  
🔄 Use `/refresh` to update the list.  
➕ Ban a user with `/ban @username` if needed.

"""
    await event.reply(msg)

async def invalid_user(event, userid):
    msg = f"""⚠️ Cannot unban user `{userid}` because they are not banned or invalid!  

🔄 Use `/refresh` to clean up the database.  
📋 Check banned users with `/banned`.
➕ Ban a user with `/ban @username` if needed.
"""
    await event.reply(msg)

async def unbanned_user(event, userid):
    msg = f"""✅ User `{userid}` has been successfully unbanned and can use the bot again!
 
🔄 Use `/refresh` to update the list.  
📋 Check all banned users with `/banned`.  
➕ Ban a user with `/ban @username` if needed.
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
            event.db.unban_user(userid)
            await unbanned_user(event, userid)
        except Exception as e:
            print(e)
            await invalid_user(event, event.args)
