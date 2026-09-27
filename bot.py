import os
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.types import Chat, Channel

api_id = 38275473
api_hash = '1d2dbdc7a786c4c1bc6b3547c7ec3e63'
string_session = os.environ.get('SESSION')

if not string_session:
    raise ValueError("ERROR: Variabel lingkungan SESSION tidak ditemukan! Pastikan secret GitHub sudah diset.")

client = TelegramClient(StringSession(string_session), api_id, api_hash)

pesan_kirim = "Halo, ini pesan broadcast otomatis."
jeda_waktu = 1200  

async def main():
    print("Userbot broadcast aktif...")
    while True:
        try:
            print("Memindai semua grup yang di-join...")
            count = 0
            
            async for dialog in client.iter_dialogs():
                if dialog.is_group or dialog.is_channel:
                    entity = dialog.entity
                    if isinstance(entity, Chat) or (isinstance(entity, Channel) and entity.megagroup):
                        try:
                            await client.send_message(dialog.id, pesan_kirim)
                            count += 1
                            print(f"Berhasil kirim ke: {dialog.name}")
                            await asyncio.sleep(3)
                        except Exception as e:
                            print(f"Gagal kirim ke {dialog.name}: {e}")
                            
            print(f"Selesai! Pesan terkirim ke {count} grup.")
            
        except Exception as e:
            print(f"Error utama: {e}")
        
        print(f"Menunggu {jeda_waktu // 60} menit untuk siklus berikutnya...")
        await asyncio.sleep(jeda_waktu)

with client:
    client.loop.run_until_complete(main())
