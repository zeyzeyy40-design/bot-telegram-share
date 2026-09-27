import os
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.types import Chat, Channel

api_id = 38275473
api_hash = "1d2dbdc7a786c4c1bc6b3547c7cc3e63"
string_session = os.environ.get('SESSION')

if not string_session:
    raise ValueError("ERROR: Variabel lingkungan SESSION tidak ditemukan! Pastikan secret GitHub sudah diset.")

client = TelegramClient(StringSession(string_session), api_id, api_hash)

pesan_kirim = "DOWNLOAD MILKYPEDIA, APK PPOB & QRIS TANPA KTP GRATISS🥳"
jeda_antar_grup = 15     # Jeda 15 detik antar grup biar aman dari FloodWait JB
jeda_siklus = 900        # Jeda 15 menit (900 detik) setelah selesai satu putaran penuh

async def main():
    print("Userbot broadcast aktif...")
    while True:
        try:
            print("Memindai semua grup yang di-join...")
            count = 0

            async for dialog in client.iter_dialogs():
                if dialog.is_group or dialog.is_channel:
                    entity = dialog.entity
                    
                    # Cek apakah grup tertutup atau read-only (tidak bisa kirim pesan)
                    is_closed = False
                    try:
                        if isinstance(entity, Channel):
                            if entity.banned_rights and entity.banned_rights.send_messages:
                                is_closed = True
                        elif isinstance(entity, Chat):
                            if entity.admin_rights and not entity.admin_rights.post_messages:
                                is_closed = True
                    except Exception:
                        pass

                    if is_closed:
                        print(f"Skipped (Grup Ditutup): {dialog.name}")
                        continue

                    # Coba kirim pesan ke grup yang terbuka
                    try:
                        await client.send_message(dialog.id, pesan_kirim)
                        count += 1
                        print(f"Berhasil kirim ke: {dialog.name}")
                        
                        # Jeda aman antar grup
                        await asyncio.sleep(jeda_antar_grup)
                        
                    except Exception as e:
                        print(f"Gagal kirim ke {dialog.name}: {e}")

            print(f"Selesai satu putaran! Pesan terkirim ke {count} grup.")

        except Exception as e:
            print(f"Error utama: {e}")

        print(f"Menunggu {jeda_siklus // 60} menit sebelum mulai siklus berikutnya...")
        await asyncio.sleep(jeda_siklus)

with client:
    client.loop.run_until_complete(main())
