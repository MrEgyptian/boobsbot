async def execute(event, client, strings):
    admins = event.db.get_admins()  # Use your method to get admins
    invalid_admins = []
    if len(admins) > 0:
        msg = "\n👑 Whitelisted Bot Admins are:\n\n"
        for admin in admins:
            try:
                entity = await client.get_entity(admin)
                username = entity.usernames[0].username if hasattr(entity, 'usernames') and entity.usernames else getattr(entity, 'username', '')
                admin_id = admin
                username_str = f"@{username} |" if username else ''
                msg += f"👤 {username_str} 🆔{admin_id}\n"
            except Exception as e:
                print(e)
                invalid_admins.append(admin)
        if len(invalid_admins) > 0:
            msg += """
🚨 Warning: Some admins in the list are deleted or invalid!  

🗑️ **Trashy Admins:**  \n"""
            msg += "\n"
            for admin in invalid_admins:
                msg += f"❌ `{admin}`\n"
            msg += """
🔄 Use `/refresh` to update the list and remove inactive admins.  

"""
        await event.reply(msg)
    else:
        await event.reply('''⚠️ No admins found in the database!  
It looks like no admins have been added yet. 🤔

➕ You can add admins with `/addadmin @username`
🔄 Refresh the database with `/refresh` to update the list!  
''')
