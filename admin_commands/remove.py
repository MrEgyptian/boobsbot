import re
async def wrong_usage_msg(event):
    msg="""❌ Incorrect command usage!  
To remove a user, use:  

✅ `/remove @username`  
✅ `/remove user_id`  

📌 **Examples:**  
🔹 `/remove @example_user`  
🔹 `/remove 123456789`  

🔍 Check existing users with `/users`.  
🔄 Use `/refresh` to update the list.  
➕ Add a user with `/add @username` if needed.

"""
    await event.reply(msg)
async def invalid_user(event,userid):
    msg=f"""⚠️ Cannot remove user `{userid}` because they are already deleted or invalid!  

🔄 Use `/refresh` to clean up the database.  
📋 Check active users with `/users`.
➕ Add a user with `/add @username` if needed.
"""
    await event.reply(msg)

async def removed_user(event,userid):
    msg=f"""🗑️ User `{userid}` has been successfully removed from the database! ✅
 
🔄 Use `/refresh` to update the list.  
📋 Check all users with `/users`.  
➕ Add a user with `/add @username` if needed.
"""
    await event.reply(msg)
async def execute(event,client, strings):
    if len(event.args)==0: await wrong_usage_msg(event)
    else:
        try:
            try:
                userid=int(event.args)
            except:
                userid=await client.get_entity(event.args)
                userid=userid.id
            event.db.rm_user(userid)
            await removed_user(event,userid)
        except Exception as e:
            print(e)
            await invalid_user(event,event.args)
