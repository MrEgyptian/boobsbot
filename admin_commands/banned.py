async def execute(event, client, strings):
    banned_users = event.db.get_banned_users()  # Use your method to get banned users
    invalid_users = []
    if len(banned_users) > 0:
        msg = "\n🚫 Banned Users:\n\n"
        for user_id in banned_users:
            try:
                entity = await client.get_entity(user_id)
                username = entity.usernames[0].username if hasattr(entity, 'usernames') and entity.usernames else getattr(entity, 'username', '')
                user_id_str = user_id
                username_str = f"@{username} |" if username else ''
                msg += f"👤 {username_str} 🆔{user_id_str}\n"
            except Exception as e:
                print(e)
                invalid_users.append(user_id)
        if len(invalid_users) > 0:
            msg += """
🚨 Warning: Some users in the list are deleted or invalid!  

🗑️ **Invalid Banned Users:**  \n"""
            msg += "\n"
            for user_id in invalid_users:
                msg += f"❌ `{user_id}`\n"
            msg += """
🔄 Use `/refresh` to update the list and remove inactive users.  

"""
        await event.reply(msg)
    else:
        await event.reply('''✅ No banned users found in the database!  
It looks like no users have been banned yet. 🤔

➕ You can ban users with `/ban @username`
🔄 Refresh the database with `/refresh` to update the list!  
''')
