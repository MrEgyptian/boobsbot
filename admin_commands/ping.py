import subprocess
import platform
import re,time

def ping_server(server: str):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', server]
    try:
        output = subprocess.run(command, stdout=subprocess.PIPE, text=True)
        result = output.stdout
        if platform.system().lower() == 'windows':
            time_ms = re.search(r'time=(\d+)ms', result)
        else:
            time_ms = re.search(r'time=(\d+\.\d+) ms', result)
        if time_ms:
            return f"{time_ms.group(1)}"
        else:
            return f"Ping to {server} failed or no response."
    except Exception as e:
        return f"An error occurred: {e}"

async def execute(event,client,strings):
     msg_id=event.message.id
     p=ping_server("8.8.8.8")
     try:
      p=float(p)
      if(p<200):
         await event.respond(f"""🏓 Pong!  
✅ Bot is online and running smoothly.  
⏳ Response time: {p}ms  
""")
      else:
         await event.respond(f"""⚠️ Pong... but slow!  
⏳ Response time: {p}ms  

🔄 The bot might be experiencing delays. Please check the server status!  
""")
     except Exception as e:
      event.error=p