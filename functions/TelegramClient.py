from telethon import TelegramClient as _TelegramClient
from telethon.tl.types import KeyboardButtonUrl, KeyboardButtonCallback
from telethon.tl.types import InputPeerChannel,InputPeerChat,InputPeerUser
from aiohttp import ClientSession,FormData
import asyncio,json,re,sys
class TelegramClient(_TelegramClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tasks={}
        self.erofus={}
    async def add_task(self, user_id, task_type, url,id=None,best_video=None,info=None):
        if not id:
            id=len(self.tasks.get(user_id, {}))+1
        self.tasks[user_id] = {id:{"url": url, "type": task_type,"best_video":best_video,"info":info}}
    async def get_tasks(self, user_id):
        return self.tasks.get(user_id, {})
    async def clear_tasks(self, user_id):
        if user_id in self.tasks:
            del self.tasks[user_id]
    def start(self, *args, **kwargs):
        result = super().start(*args, **kwargs)
        self.bot_token = kwargs.get('bot_token', None)
        return result
    def entity_to_id(self, entity):
        if isinstance(entity,  InputPeerUser):
            #print(entity.user_id)
            return int(entity.user_id)
        elif isinstance(entity, (InputPeerChannel, InputPeerChat)):
            return int(entity.channel_id)
        elif isinstance(entity, str) or isinstance(entity, int):
            return int(entity)
        else:
            #print(entity,entity.__class__)
            return int(entity.id)
    def telethon_buttons_to_botapi(self,buttons):
        """
        Convert Telethon button objects into Bot API inline_keyboard format.
        """
        inline_keyboard = []

        for row in buttons:
            row_buttons = []
            for btn in row:
                if isinstance(btn, KeyboardButtonUrl):
                    row_buttons.append({
                        "text": btn.text,
                        "url": btn.url
                    })
                elif isinstance(btn, KeyboardButtonCallback):
                    # Bot API callback_data must be str or bytes ≤ 64 bytes
                    row_buttons.append({
                        "text": btn.text,
                        "callback_data": btn.data.decode() if isinstance(btn.data, (bytes, bytearray)) else str(btn.data)
                    })
                else:
                    # Fallback: just show text
                    row_buttons.append({"text": getattr(btn, "text", "Unknown")})
            inline_keyboard.append(row_buttons)

        return {"inline_keyboard": inline_keyboard}
    def telethon_parse_to_botapi(self, parse_mode: str | None) -> str | None:
        """
        Convert Telethon parse_mode to Telegram Bot API parse_mode.
        Returns None if no parse_mode should be used.
        """

        if parse_mode is None or parse_mode == () or parse_mode is ...:
            print("parse_mode",parse_mode)

            return "MarkdownV2"

        parse_mode = parse_mode.lower()

        mapping = {
            "md": "Markdown",
            "markdown": "Markdown",
            "markdown2": "MarkdownV2",
            "html": "HTML"
        }

        return mapping.get(parse_mode, None)
    def escape_markdown_v2(self, text: str) -> str:
        """
        Escape special characters for Telegram Bot API MarkdownV2.
        """
        escape_chars = r':~>#+-=|{}.!'
        return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text).replace('**','*')
    async def send_file(self, entity, file, *, caption = None,message=None, force_document = False, mime_type = None, file_size = None, clear_draft = False, progress_callback = None, reply_to = None, attributes = None, thumb = None, allow_cache = True, parse_mode = ..., formatting_entities = None, voice_note = False, video_note = False, buttons = None, silent = None, background = None, supports_streaming = False, schedule = None, comment_to = None, ttl = None, nosound_video = None, send_as = None, message_effect_id = None, **kwargs):
        #return super().send_file(entity, file, caption=caption, force_document=force_document, mime_type=mime_type, file_size=file_size, clear_draft=clear_draft, progress_callback=progress_callback, reply_to=reply_to, attributes=attributes, thumb=thumb, allow_cache=allow_cache, parse_mode=parse_mode, formatting_entities=formatting_entities, voice_note=voice_note, video_note=video_note, buttons=buttons, silent=silent, background=background, supports_streaming=supports_streaming, schedule=schedule, comment_to=comment_to, ttl=ttl, nosound_video=nosound_video, send_as=send_as, message_effect_id=message_effect_id, **kwargs)
        if parse_mode is None or parse_mode == () or parse_mode is ...:
            parse_mode = "md"
        async with ClientSession() as session:
            url = f"https://api.telegram.org/bot{self.bot_token}/"

            self.aiosession = session
            form = FormData()

            form.add_field("chat_id", str(self.entity_to_id(entity)))

            # file
            if file is not None:
               if hasattr(file, "read") and callable(file.read):
                   return await super().send_file(entity, file, caption=caption, force_document=force_document, mime_type=mime_type, file_size=file_size, clear_draft=clear_draft, progress_callback=progress_callback, reply_to=reply_to, attributes=attributes, thumb=thumb, allow_cache=allow_cache, parse_mode=parse_mode, formatting_entities=formatting_entities, voice_note=voice_note, video_note=video_note, buttons=buttons, silent=silent, background=background, supports_streaming=supports_streaming, schedule=schedule, comment_to=comment_to, ttl=ttl, nosound_video=nosound_video, send_as=send_as, message_effect_id=message_effect_id, **kwargs)
                    # if force_document:
                    #     form.add_field("force_document", "true" if force_document else "false")
                    #     url += "sendDocument"
                    # else:
                    #     if not hasattr(file, "name"):
                    #             file.name = "file.bin"
                    #             form.add_field("document", file, filename=file.name, content_type="application/octet-stream")
                    #             url += "sendDocument"
                    #     elif file.name.lower().endswith(('.mp4', '.mkv', '.mov', '.avi', '.wmv', '.flv', '.webm')):
                    #             form.add_field("video", file, filename=file.name, content_type="application/octet-stream")
                    #             url += "sendVideo"
                    #     elif file.name.lower().endswith(('.mp3', '.wav', '.ogg', '.flac', '.m4a')):
                    #             form.add_field("audio", file, filename=file.name, content_type="application/octet-stream")
                    #             url += "sendAudio"
                    #     elif file.name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')):
                    #             form.add_field("photo", file, filename=file.name, content_type="application/octet-stream")
                    #             url += "sendPhoto"
                    #     else:
                    #                 form.add_field("document", file, filename=file.name, content_type="application/octet-stream")
                    #                 url += "sendDocument"
               elif isinstance(file,list):
                   return await super().send_file(entity, file, caption=caption, force_document=force_document, mime_type=mime_type, file_size=file_size, clear_draft=clear_draft, progress_callback=progress_callback, reply_to=reply_to, attributes=attributes, thumb=thumb, allow_cache=allow_cache, parse_mode=parse_mode, formatting_entities=formatting_entities, voice_note=voice_note, video_note=video_note, buttons=buttons, silent=silent, background=background, supports_streaming=supports_streaming, schedule=schedule, comment_to=comment_to, ttl=ttl, nosound_video=nosound_video, send_as=send_as, message_effect_id=message_effect_id, **kwargs)
               elif isinstance(file, str) and (file.startswith("http") or file.startswith("https")):
                   file=file.replace("requiressl=yes","requiressl=no")
                   if file.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')):
                        form.add_field("photo", file)
                        url += "sendPhoto"
                   elif file.endswith(('.mp4', '.mkv', '.mov', '.avi', '.wmv', '.flv', '.webm')):
                        form.add_field("video", file)
                        url += "sendVideo"
                   elif file.endswith(('.mp3', '.wav', '.ogg', '.flac', '.m4a')):
                        form.add_field("audio", file)
                        url += "sendAudio"
                   elif force_document:
                        form.add_field("force_document", "true" if force_document else "false")
                        form.add_field("document", file)
                        url += "sendDocument"
                   elif file.endswith(('.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.zip', '.rar', '.7z')):
                        form.add_field("document", file)
                        url += "sendDocument"
                   else:

                       form.add_field("video", file,content_type="video/mp4",content_transfer_encoding="binary")
                       form.add_field("disable_content_type_detection", "true")
                       print(file)
                       form.add_field("mime_type", "video/mp4")
                       url += "sendVideo"

            # caption
            caption= caption or message
            if caption is not None:
                print("caption",caption)
                form.add_field("caption", self.escape_markdown_v2(caption))


            # mime_type
            if mime_type is not None:
                form.add_field("mime_type", str(mime_type))

            # file_size
            if file_size is not None:
                form.add_field("file_size", str(file_size))

            # clear_draft
            if clear_draft is not None:
                form.add_field("clear_draft", "true" if clear_draft else "false")
            print("url",url.encode('utf-8'))

            # progress_callback (functions can’t be sent, skip or serialize differently)
            # if progress_callback is not None:
            #     form.add_field("progress_callback", str(progress_callback))

            # reply_to
            if reply_to is not None:
                form.add_field("reply_to", str(reply_to))

            # attributes
            if attributes is not None:
                form.add_field("attributes", str(attributes))

            # thumb
            if thumb is not None:
                if not hasattr(thumb, "name"):
                    thumb.name = "thumb.bin"
                form.add_field("thumb", thumb, filename=thumb.name, content_type="application/octet-stream")

            # allow_cache
            if allow_cache is not None:
                form.add_field("allow_cache", "true" if allow_cache else "false")

            # parse_mode
            parse_mode = self.telethon_parse_to_botapi(parse_mode)
            if parse_mode is not None:
                #print("parse_mode",parse_mode)
                form.add_field("parse_mode", parse_mode)

            # formatting_entities
            if formatting_entities is not None:
                form.add_field("formatting_entities", str(formatting_entities))

            # voice_note
            if voice_note is not None:
                form.add_field("voice_note", "true" if voice_note else "false")

            # video_note
            if video_note is not None:
                form.add_field("video_note", "true" if video_note else "false")

            # buttons
            if buttons is not None:
                buttons = self.telethon_buttons_to_botapi(buttons)
                #print("buttons",buttons)
                form.add_field("reply_markup", json.dumps(buttons))

            # silent
            if silent is not None:
                form.add_field("silent", "true" if silent else "false")

            # background
            if background is not None:
                form.add_field("background", "true" if background else "false")

            # supports_streaming
            if supports_streaming is not None:
                form.add_field("supports_streaming", "true" if supports_streaming else "false")

            # schedule
            if schedule is not None:
                form.add_field("schedule", str(schedule))

            # comment_to
            if comment_to is not None:
                form.add_field("comment_to", str(comment_to))

            # ttl
            if ttl is not None:
                form.add_field("ttl", str(ttl))

            # nosound_video
            if nosound_video is not None:
                form.add_field("nosound_video", "true" if nosound_video else "false")

            # send_as
            if send_as is not None:
                form.add_field("send_as", str(send_as))

            # message_effect_id
            if message_effect_id is not None:
                form.add_field("message_effect_id", str(message_effect_id))

            async with self.aiosession.post(url, data=form) as resp:
                #print(resp.status)
                #print(await resp.text())
                print(resp.status,await resp.json())
                return resp.status, await resp.json()
    def reload_bot(self):
        import os
        os.execv(sys.executable, ['python'] + sys.argv)
    def reload_session(self):
        self.session = self.session
        self.session.save()
        self.disconnect()
        self.connect()
    def disconnect(self):
        super().disconnect()
        if hasattr(self, 'aiosession'):
            asyncio.get_event_loop().run_until_complete(self.aiosession.close())
    def close(self):
        self.disconnect()
    def connect(self):
        return super().connect()
