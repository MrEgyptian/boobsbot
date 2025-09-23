async def execute(event, client, strings):

    contact_text = (
        "📩 **Contact Support**\n\n"
        "Please describe your issue or feedback after this command.\n\n"
        "_Example:_\n"
        "`/contact The video link is not working on site XYZ.`\n\n"
        "Your message will be forwarded to the developer."
    )

    # Check if user added a message
    msg_parts = event.raw_text.split(" ", 1)
    if len(msg_parts) > 1:
        user_message = msg_parts[1]
        # Forward the message to you (bot owner)
        for owner_id in client.owner_ids:
            try:
                await client.send_message(int(owner_id), f"📬 **New Contact Message**\n\nFrom: [{event.sender.first_name}](tg://user?id={event.sender_id})\nMessage: {user_message}")
            except Exception as e:
                pass
        await event.reply("✅ Your message has been sent to support. We'll get back to you soon!")
    else:
        await event.reply(contact_text)