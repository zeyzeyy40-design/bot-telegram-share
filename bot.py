import os
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

api_id = 38275473
api_hash = '1d2dbdc7a786c4c1bc6b3547c7ec3e63'
string_session = os.environ.get('SESSION')

# Inisialisasi client menggunakan StringSession dari environment variable GitHub Secrets
client = TelegramClient(StringSession(string_session), api_id, api_hash)

pesan_kirim = "Halo, ini pesan otomatis userbot!"
jeda_waktu = 10 # dalam menit

async def main():
    print("Userbot broadcast aktif...")
    while True:
        try:
            print("Memindai semua grup yang di-join...")
            count = 0
            async for dialog in client.iter_dialogs():
                if dialog.is_group or dialog.is_channel:
                    entity = dialog.entity
                    if getattr(entity, 'megagroup', False) or dialog.is_channel:
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
        
        print(f"Menunggu {jeda_waktu} menit untuk siklus berikutnya...")
        await asyncio.sleep(jeda_waktu * 60)

with client:
    client.loop.run_until_complete(main())
