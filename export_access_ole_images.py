# Project mostly AI-generated, but tested and actively used.

import mysql.connector
from pathlib import Path
import os
from PIL import Image
import io

# === Funktion: BMP-Header an DIB anhängen ===
def extract_bmp_from_dib(blob: bytes) -> bytes:
    dib_signature = b'\x28\x00\x00\x00'
    dib_offset = blob.find(dib_signature)
    if dib_offset == -1:
        raise ValueError("Kein DIB-Header (0x28 00 00 00) gefunden.")

    dib = blob[dib_offset:]
    filesize = len(dib) + 14

    bmp_header = b'BM'
    bmp_header += filesize.to_bytes(4, 'little')
    bmp_header += (0).to_bytes(4, 'little')
    bmp_header += (14).to_bytes(4, 'little')

    return bmp_header + dib

# === Setup ===
output_dir = Path(os.path.abspath(os.path.dirname(__file__)))

# === DB-Verbindung (anpassen!) ===
conn = mysql.connector.connect(
    host='your_host',
    user='your_user',
    password='your_password',
    database='your_database'
)
cursor = conn.cursor()

cursor.execute("SELECT Art_Nr, Art_Bild FROM your_schema.your_table WHERE Art_Bild IS NOT NULL")
rows = cursor.fetchall()
print(f"📦 {len(rows)} Bilder gefunden.\n")

# === Verarbeiten ===
for i, (art_pk, blob) in enumerate(rows, start=1):
    try:
        bmp_bytes = extract_bmp_from_dib(blob)
        img = Image.open(io.BytesIO(bmp_bytes))

        # Ziel-Dateiname
        jpg_path = output_dir / f"{art_pk}.jpg"

        # Speichern mit Standardqualität
        img.convert("RGB").save(jpg_path, format='JPEG', quality=85)

        # Prüfen ob über 300 KB → neu speichern mit 70% Qualität
        if jpg_path.stat().st_size > 300_000:
            img.convert("RGB").save(jpg_path, format='JPEG', quality=70)
            print(f"📉 [{i}/{len(rows)}] {art_pk}.jpg komprimiert (<300KB)")
        else:
            print(f"✅ [{i}/{len(rows)}] {art_pk}.jpg gespeichert")

    except Exception as e:
        print(f"❌ [{i}/{len(rows)}] Fehler bei {art_pk}: {e}")

cursor.close()
conn.close()
