import os
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.types import Chat, Channel
from telethon.errors import FloodWaitError

api_id = 38275473
api_hash = '1d2debu7a786c41bub3547c7cc3ee63'
string_session = os.getenv('SESSION_STRING')

if not string_session:
    raise ValueError("ERROR: Variabel lingkungan SESSION_STRING tidak diatur.")

client = TelegramClient(StringSession(string_session), api_id, api_hash)
pesan_irim = "download apk ppob & qris tanpa ktp ku dong, baca namaku aja ya.."
jeda_antar_grup = 35 # Disesuaikan sedikit jadi 35 detik biar gak gampang flood

async def main():
    while True:
        print("Memulai putaran broadcast...")
        count = 0
        
        async for dialog in client.iter_dialogs():
            if dialog.is_group or dialog.is_channel:
                entity = dialog.entity
                
                # Cek grup tertutup/read only
                is_closed = False
                try:
                    if isinstance(entity, Channel) and entity.banned_rights:
                        is_closed = True
                    elif isinstance(entity, Chat) and entity.admin_rights:
                        is_closed = True
                except Exception:
                    pass
                
                if is_closed:
                    continue
                
                # Kirim pesan dengan proteksi FloodWait & Auto-Reconnect
                berhasil = False
                while not berhasil:
                    try:
                        # Pastikan koneksi aktif sebelum kirim
                        if not client.is_connected():
                            print("Koneksi terputus, mencoba menyambungkan ulang...")
                            await client.connect()
                        
                        await client.send_message(dialog.id, pesan_irim)
                        count += 1
                        print(f"Berhasil kirim ke: {dialog.name}")
                        berhasil = True
                        await asyncio.sleep(jeda_antar_grup)
                        
                    except FloodWaitError as e:
                        menunggu = e.seconds + 5
                        print(f"Kena FloodWait, menunggu {menunggu} detik...")
                        await asyncio.sleep(menunggu)
                        
                    except Exception as ex:
                        print(f"Gagal kirim ke {dialog.name}: {ex}")
                        if "disconnected" in str(ex).lower():
                            print("Koneksi terputus di tengah jalan, mencoba menyambungkan ulang...")
                            await asyncio.sleep(10)
                            try:
                                await client.connect()
                            except:
                                pass
                        else:
                            break
                            
        print(f"Selesai: Pesan disebar ke {count} grup. Menunggu 15 menit untuk putaran berikutnya...")
        
        # Jeda 15 menit (900 detik) sebelum bot mengulang broadcast dari awal secara otomatis
        await asyncio.sleep(900)

with client:
    client.loop.run_until_complete(main())
