from functions.db_models import User, Group, GrowthHistory

async def execute(event, client, strings):

    client.db.clear_db()

    await event.reply("🗑️ Database cleared successfully!")
