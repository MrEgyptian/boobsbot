async def execute(event,client, strings):

 users=event.db.get_users()
 invalid_users=[]
 if len(users)>0:
    msg="\n📜 Whitelisted bot Users are:\n\n"
    for user in users:
        try:
            username=await client.get_entity(user)
            username=username.usernames[0].username if username.usernames else username.username
            userid=user
            if(userid):
                username=f"@{username} |" if username else ''
                msg+=f"👤 {username} 🆔{userid}\n"
        except Exception as e:
           print(e)
           invalid_users.append(user)
    if(len(invalid_users)>0):
       msg+="""
🚨 Warning: Some users in the list are deleted or invalid!  

🗑️ **Trashy Users:**  \n"""
       msg+="\n"
       for user in invalid_users:
          msg+=f"❌ `{user}`\n"
       msg+="""
🔄 Use `/refresh` to update the list and remove inactive users.  

"""
    await event.reply(msg)
 else:
    await event.reply('''⚠️ No users found in the database!  
It looks like no users have been added yet. 🤔

➕ You can add users with `/add @username`
🔄 Refresh the database with `/refresh` to update the list!  
''')