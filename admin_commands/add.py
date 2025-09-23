import re
async def wrong_usage_msg(event):
    msg="""    ❌ Incorrect usage!  
To add a user, use:  
`/add @username` or `/add user_id`  

🔍 Example:  
`/add @example_user`  
`/add 123456789`  
"""
    await event.reply(msg)
async def invalid_user_msg(event):
    msg="""⚠️ User not found on Telegram!  
Make sure the username or user ID is correct.  

🔍 Try checking manually:  
🔗 [t.me/username_or_id](https://t.me/username_or_id)  

💡 **Possible reasons:**  
- The username doesn't exist.  
- The user ID is invalid.  
- The account is private or deleted.  
- A typo in the username or ID.  

✅ Try again with a valid username or ID!  

"""
    await event.reply(msg)
async def valid_user_msg(event,userid):
    msg=f"""✅ User `{userid}` has been successfully added to the database!  

🔄 Use `/refresh` to update the list.  
📋 Check all users with `/users`.  

"""
    await event.reply(msg)
async def exists_user_msg(event,userid):
    msg=f"""⚠️ This user `{userid}` is already in the database!  

🔍 Use `/users` to check the existing users.  
🔄 If needed, refresh with `/refresh`.  
"""
    await event.reply(msg)
async def execute(event,client, strings):
    user_entity=event.args if len(event.args)>0 else None
    if re.match(r'[0-9]+', event.args):
        user_entity=int(event.args)
    if not user_entity: await wrong_usage_msg(event)
    else:
        try:
            ent=await client.get_entity(user_entity)
            try:
                event.db.add_user(ent.id)
                await valid_user_msg(event,ent.id)
            except Exception as e:
                await exists_user_msg(event,ent.id)
        except Exception as e:
            print(e)
            await invalid_user_msg(event)
