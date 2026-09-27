import os
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.types import Chat, Channel
from telethon.errors import FloodWaitError

api_id = 38275473
api_hash = "1d2dbdc7a786c4c1bc6b3547c7cc3e63"
string_session = os.environ.get('SESSION')

if not string_session:
    raise ValueError("ERROR: Variabel lingkungan SESSION tidak ditemukan! Pastikan secret GitHub sudah diset.")

client = TelegramClient(StringSession(string_session), api_id, api_hash)

pesan_kirim = "apk ppob & qris tanpa ktp gratis tinggal login, baca namaku"
jeda_antar_grup = 25     # Jeda agak panjang (25 detik) supaya lebih aman dari pancingan spam

async def main():
    print("Userbot broadcast anti-gagal aktif...")
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

                    # Sistem Kirim dengan Proteksi Anti-FloodWait (Otomatis Nunggu & Coba Lagi)
                    berhasil = False
                    while not berhasil:
                        try:
                            await client.send_message(dialog.id, pesan_kirim)
                            count += 1
                            print(f"Berhasil kirim ke: {dialog.name}")
                            berhasil = True
                            
                            # Jeda antar grup yang terbuka
                            await asyncio.sleep(jeda_antar_grup)
                            
                        except FloodWaitError as e:
                            # Jika kena batasan Telegram, bot otomatis diam menunggu sampai waktu hukuman selesai, lalu lanjut lagi!
                            menunggu = e.seconds + 5
                            print(f"Kena FloodWait di {dialog.name}. Menunggu otomatis selama {menunggu} detik...")
                            await asyncio.sleep(menunggu)
                        except Exception as e:
                            print(f"Gagal kirim ke {dialog.name} karena kendala lain: {e}")
                            break # Lewati grup ini jika error-nya bukan karena FloodWait (misal akun di-kick/dibanned dari grup)

            print(f"Selesai satu putaran penuh! Pesan berhasil disebar ke {count} grup.")

        except Exception as e:
            print(f"Error utama siklus: {e}")

        # Jeda antar siklus besar (misal 15 menit sebelum mutar ulang dari grup pertama)
        print("Menunggu 15 menit sebelum mulai siklus berikutnya...")
        await asyncio.sleep(900)

with client:
    client.loop.run_until_complete(main())
