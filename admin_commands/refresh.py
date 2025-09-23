async def execute(event,client, strings):
   new_users=event.db.get_users()
   if(event.db.allowed_users==new_users):
      updated="""
⚠️ The database is already up to date!  
No new users were added or removed.  


   ➕ You can add users with /add @username  
   📌 Use `/users` to check the current list.  
"""
      await event.reply(updated)
   else:
      success="""🔄 Database refreshed successfully! ✅  
   📋 All users and data are now up to date.  

   🔍 Check the latest users with `/users`. 
   ➕ You can add users with /add @username  
   🔄 Refresh the database with /refresh to update the list! 
   """
      await event.reply(success)
