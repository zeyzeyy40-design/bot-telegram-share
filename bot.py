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

pesan_kirim = "DOWNLOAD APLIKASI QRIS TANPA KTP & GRATIS FEE CUMA 101P LOH 🥳"
jeda_waktu = 300  # Jeda 5 menit untuk siklus berikutnya

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
                        
                        # Cek apakah grup tertutup atau tidak mengizinkan mengirim pesan
                        # (Membaca atribut admin_rights atau default_banned_rights dari entity)
                        try:
                            # Jika grup adalah channel/megagroup, cek hak kirim pesannya
                            if isinstance(entity, Channel):
                                if entity.banned_rights and entity.banned_rights.send_messages:
                                    print(f"Skipped (Grup Ditutup/Read-only): {dialog.name}")
                                    continue
                            elif isinstance(entity, Chat):
                                if entity.admin_rights and not entity.admin_rights.post_messages:
                                    # Untuk grup biasa, pastikan tidak dibatasi
                                    pass
                        except Exception:
                            pass

                        try:
                            await client.send_message(dialog.id, pesan_kirim)
                            count += 1
                            print(f"Berhasil kirim ke: {dialog.name}")
                            
                            # Jeda 6 detik antar pesan agar aman dari batasan FloodWait Telegram
                            await asyncio.sleep(6)
                            
                        except Exception as e:
                            # Kalau tetap kena error karena grup tiba-tiba read-only/restricted
                            print(f"Gagal kirim ke {dialog.name}: {e}")

            print(f"Selesai! Pesan terkirim ke {count} grup.")

        except Exception as e:
            print(f"Error utama: {e}")

        print(f"Menunggu {jeda_waktu // 60} menit untuk siklus berikutnya...")
        await asyncio.sleep(jeda_waktu)

with client:
    client.loop.run_until_complete(main())
