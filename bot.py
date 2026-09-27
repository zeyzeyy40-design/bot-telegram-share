import asyncio
from telethon import TelegramClient
from telethon.tl.types import Channel, Chat

# --- ISI DATA AKUN TELEGRAM LU DISINI ---
api_id = 38275473       # Ganti pakai API ID lu (ambil di my.telegram.org)
api_hash = '1d2dbdc7a786c4c1bc6b3547c7ec3e63' # Ganti pakai API Hash lu
pesan_kirim = 'Halo gan, mau promoin layanan / panel sosial media di sini ya!' 
jeda_waktu = 1200     # 1200 detik = 20 menit

client = TelegramClient('sesi_userbot', api_id, api_hash)

async def main():
    print("Userbot broadcast aktif...")
    while True:
        try:
            print("Memindai semua grup yang di-join...")
            count = 0
            
            # Loop untuk mendeteksi semua dialog/chat yang ada di akun
            async for dialog in client.iter_dialogs():
                # Cek apakah itu grup atau supergrup (channel biasa diskip biar gak error)
                if dialog.is_group or dialog.is_channel:
                    entity = dialog.entity
                    # Pastikan kita punya izin kirim pesan (bukan channel broadcast satu arah)
                    if isinstance(entity, Chat) or (isinstance(entity, Channel) and entity.megagroup):
                        try:
                            await client.send_message(dialog.id, pesan_kirim)
                            count += 1
                            print(f"Berhasil kirim ke: {dialog.name}")
                            # Jeda 3 detik antar grup supaya gak kena banned (FloodWait)
                            await asyncio.sleep(3)
                        except Exception as e:
                            print(f"Gagal kirim ke {dialog.name}: {e}")
                            
            print(f"Selesai! Pesan terkirim ke {count} grup.")
            
        except Exception as e:
            print(f"Error utama: {e}")
        
        # Tunggu selama 20 menit sebelum siklus kirim berikutnya
        print(f"Menunggu {jeda_waktu // 60} menit untuk siklus berikutnya...")
        await asyncio.sleep(jeda_waktu)

with client:
    client.loop.run_until_complete(main())
