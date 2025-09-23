from telethon import Button
import math

# Number of chats per page
CHATS_PER_PAGE = 2
MAX_PAGE_BUTTONS = 3

async def execute(event, client, strings):
    # Fetch all chats the bot is a part of
    chats = event.db.get_bot_groups()  
    total_chats = len(chats)
    total_pages = math.ceil(total_chats / CHATS_PER_PAGE)
    
    # Get the current page number from the event (if any)
    page_number = 1
    # Calculate the start and end indices for the current page
    start_index = (page_number - 1) * CHATS_PER_PAGE
    end_index = min(start_index + CHATS_PER_PAGE, total_chats)
    
    # Prepare the message
    chat_list = "📋 **Here are the chats the bot is in:**\n"
    buttons = []
    
    # Add the chats for the current page
    for chat in chats[start_index:end_index]:
        try:
            chat_info = await client.get_entity(chat)
            
            # Prepare the chat details
            chat_name = chat_info.title if hasattr(chat_info, 'title') else "Unknown"
            chat_username = f"@{chat_info.username}" if chat_info.username else "No username"
            
            # Add buttons for each chat
            chat_button = Button.inline(f" 💬{chat_name} {chat_username}", data=f"chat_{chat}")
            leave_button = Button.inline(f"❌ Leave ", data=f"leave_{chat}")
            invite_button = Button.inline(f"🔗 Link", data=f"invite_{chat}")
            
            buttons.append([chat_button, leave_button, invite_button])  # Add buttons in a row
            
        except Exception as e:
            # In case there's an error fetching the chat info
            print(f"Error fetching chat {chat}: {e}")
    
    # Add pagination buttons (Page numbers and Last)
    navigation_buttons = []

    if page_number > 1:
        navigation_buttons.append(Button.inline("⬅️ ", data=f"page_{page_number - 1}"))

    # Add page number buttons
    page_buttons = [Button.inline(str(i), data=f"page_{i}") for i in range(1, total_pages + 1)]
    
    if len(page_buttons) > MAX_PAGE_BUTTONS:  # Limit the number of page buttons to 5 for display purposes
        page_buttons = page_buttons[:MAX_PAGE_BUTTONS] + [Button.inline("...")] + page_buttons[-1:]

    navigation_buttons.extend(page_buttons)

    if page_number < total_pages:
        navigation_buttons.append(Button.inline(" ➡️", data=f"page_{page_number + 1}"))
    
    if buttons:
        await event.respond(
            chat_list, 
            buttons=[*buttons, navigation_buttons] if navigation_buttons else buttons
        )
    else:
        await event.respond("❌ No chats found.")
