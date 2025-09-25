async def execute(event, args):
    #event.sender_id=sender = await event.get_sender()
    #await event.edit('hh')
    print(event)
    event.reply=event.edit
    await event.client.commands['grow'](event,event.client,'')
    pass