import os
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.types import Chat, Channel
from telethon.errors import FloodWaitError

api_id = 38275473
api_hash = "1d2dbdc7a786c41bc6b3547c7cc3e63"
string_session = os.environ.get('SESSION_STRING')

if not string_session:
    raise ValueError("ERROR: Variabel lingkungan SESSION_STRING tidak ditemukan!")

client = TelegramClient(StringSession(string_session), api_id, api_hash)
pesan_kirim = "apk ppob & qris tanpa ktp gratis tinggal login, baca namaku"
jeda_antar_grup = 25

async def main():
    print("Memulai putaran broadcast...")
    count = 0

    async for dialog in client.iter_dialogs():
        if dialog.is_group or dialog.is_channel:
            entity = dialog.entity
            
            # Cek grup tertutup/read-only
            is_closed = False
            try:
                if isinstance(entity, Channel) and entity.banned_rights and entity.banned_rights.send_messages:
                    is_closed = True
                elif isinstance(entity, Chat) and entity.admin_rights and not entity.admin_rights.post_messages:
                    is_closed = True
            except Exception:
                pass

            if is_closed:
                continue

            # Kirim pesan dengan proteksi FloodWait
            berhasil = False
            while not berhasil:
                try:
                    await client.send_message(dialog.id, pesan_kirim)
                    count += 1
                    print(f"Berhasil kirim ke: {dialog.name}")
                    berhasil = True
                    await asyncio.sleep(jeda_antar_grup)
                except FloodWaitError as e:
                    menunggu = e.seconds + 5
                    print(f"Kena FloodWait, menunggu {menunggu} detik...")
                    await asyncio.sleep(menunggu)
                except Exception:
                    break

    print(f"Selesai! Pesan disebar ke {count} grup. Bot dimatikan dengan aman.")

with client:
    client.loop.run_until_complete(main())
