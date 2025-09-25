#!/bin/env python3
from telethon import events
from functions.TelegramClient import TelegramClient
from telethon.errors import rpcbaseerrors # type: ignore
import tracemalloc
from configparser import ConfigParser as cp
import yaml
from urllib.parse import quote_plus

import json,colorama
import asyncio
from datetime import datetime
import os,uuid,random,sys
import logging
from functions.custom_md import BotMD as md
from functions.formatter import *
from functions.database import Database
import re,random,time,threading,asyncio,uuid,random,os
#from datetime import datetime
from datetime import datetime, timedelta
import logging
colorama.init(True)
os.makedirs('logs/',exist_ok=True)
os.makedirs('sessions/',exist_ok=True)
term_handler= logging.StreamHandler()
term_handler.setLevel(logging.INFO)
term_handler.setFormatter(Formatter())
handlers = [logging.FileHandler("logs/log.txt"), term_handler]
#format='%(asctime)s - %(levelname)s - %(message)s'
fmt='[%(levelname)s] %(message)s'
logging.basicConfig(level=logging.DEBUG,handlers=handlers,format=fmt)
sys.stdout.reconfigure(encoding='utf-8')  # ensures console uses UTF-8

#################
config = cp()
logging.info('Reading config')
config.read('config.ini')

db_username = config.get("database", "DB_USERNAME").strip()
db_password = quote_plus(config.get("database", "DB_PASSWORD").strip())
db_host = config.get("database", "DB_HOST").strip()
db_port = config.get("database", "DB_PORT").strip()
db_name = config.get("database", "DB_NAME").strip()

# Build DATABASE_URL
DATABASE_URL = f"postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"

#DATABASE_URL = f"postgresql://{config.get('database', 'DB_USERNAME')}:{config.get('database', 'DB_PASSWORD')}@{config.get('database', 'DB_HOST')}:{config.get('database', 'DB_PORT')}/{config.get('database', 'DB_NAME')}"
db=Database(DATABASE_URL)
bot_token = config.get('bot', 'token')

api_id = config.get('bot', 'api_id')
api_hash = config.get('bot', 'api_hash')
session_name = config.get('bot', 'session_name')

db.logs_channel=config.getint('logs', 'channel')


logging.info(f"Found \x1b[1;93m[{db.get_bot_users_count()}]\x1b[0;96m users who can use the bot.")
owner_ids = config.get('bot', 'owner_ids').split(',')
prefix=config.get('bot', 'prefix')
db.prefix=prefix

client = TelegramClient(session_name, api_id=api_id, api_hash=api_hash)
client.lang='en'
client.owner_ids = owner_ids
client.tasks = {}
command_pattern=rf"\{prefix}(\w+)(.*)"
#########################################################################
logging.info('Loading commands & aliases')
with open('alias.yaml', 'r',encoding="utf-8") as file:
    strings = yaml.safe_load(file)

handlers={}
for filename in os.listdir('inline_handlers'):
    if filename.endswith('.py'):
        handler_name = filename.split('.')[0]
        handler_module = __import__(f'inline_handlers.{handler_name}', fromlist=[''])
        if hasattr(handler_module, "register"):
            
            handler_module.register(client)
commands = {}
commands_folder = 'commands'
for filename in os.listdir(commands_folder):
    if filename.endswith('.py'):
        command_name = filename.split('.')[0]
        command_module = __import__(f'{commands_folder}.{command_name}', fromlist=[''])
        commands[command_name] = getattr(command_module, 'execute')


admin_commands = {}
admin_commands_folder = 'admin_commands'
for filename in os.listdir(admin_commands_folder):
    if filename.endswith('.py'):
        admin_command_name = filename.split('.')[0]
        admin_command_module = __import__(f'{admin_commands_folder}.{admin_command_name}', fromlist=[''])
        admin_commands[admin_command_name] = getattr(admin_command_module, 'execute')

# Create a reverse mapping from aliases to main commands
aliases_map = {}
if strings:
 aliases=strings.get('commands')
 if aliases:
  for command, data in aliases.items():
    main_command = command
    aliases = data.get('aliases', [])
    for alias in aliases:
        aliases_map[alias] = main_command
queries = {}
queries_folder = 'queries'
for filename in os.listdir(queries_folder):
    if filename.endswith('.py'):
        query_name = filename.split('.')[0]
        query_module = __import__(f'{queries_folder}.{query_name}', fromlist=[''])
        queries[query_name] = getattr(query_module, 'execute')
@client.on(events.CallbackQuery)
async def handle_callback(event):
    #print(event.query)
    if event.query:
        #command = event.pattern_match.group(1)
        client.commands=commands
        event.db=db
        event.client.db=db
        data = event.query.data.decode('utf-8')
        EV=data.split('\x20')
        args="\x20".join(EV[1:])
        if EV[0] in queries:
         await queries[EV[0]](event,args)
@client.on(events.NewMessage(pattern=command_pattern))
async def handle_command(event):
    command = event.pattern_match.group(1)
    db.command=command
    args = event.pattern_match.group(2).lstrip()
    event.args=args
    event.userid=user_id=event.sender_id
    event.db=db
    event.userid=user_id
    db.user_id=int(user_id)
    event.db=db
    #print(f"User {user_id} used command {command} with args {args}")
    if event.is_private:
      try:
        db.add_user(user_id)
      except Exception as e:
        pass
    else:
      try:
       db.add_bot_group(event.chat_id)
      except Exception as e:
        pass
    db.allowed_users=db.get_users()
    if(str(user_id) in owner_ids) or (int(user_id) in db.allowed_users):
      asyncio.create_task(exec_command(event,command))
      client.db=event.db
      pass
    else:
     await event.respond("You're not allowed to use the bot contact @MrAhmed to get whitelisted.")


async def exec_command(event,command):
 try:
  if command in admin_commands:
   if str(event.userid) in owner_ids:
    #print('lol')
    await admin_commands[command](event,client,strings)
    pass
   else:
    return
  if command in commands:
   await commands[command](event,client, strings)
  elif command in aliases_map:
   main_command = aliases_map[command]
   await commands[main_command](event,client,strings)
 except ValueError as e:
  logging.error(f"Error {e}")
  #await event.delete()
  pass

async def main():
    await client.start(bot_token=bot_token)
    print(client.bot_token)
    
    tracemalloc.start()

    # Run both clients concurrently
    await asyncio.gather(
        client.run_until_disconnected(),
    )
if __name__ == '__main__':
 asyncio.run(main())
