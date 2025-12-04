from datetime import datetime
import sys

# ======== Variabel Global ========
riwayat_tidur = []


# ======== Fungsi yang digunakan ========

def hitung_durasi(waktu_tidur, waktu_bangun):
    format_waktu = "%H:%M"
    start = datetime.strptime(waktu_tidur, format_waktu)
    end = datetime.strptime(waktu_bangun, format_waktu)

    if end < start:
        end = end.replace(day=end.day + 1)

    durasi = end - start
    return round(durasi.total_seconds() / 3600, 2)


def kategori_tidur(usia):
    if usia <= 12:
        return "Anak-anak", 9
    elif usia <= 17:
        return "Remaja", 8
    return "Dewasa", 7


def hitung_sleep_debt(durasi, kebutuhan):
    return max(kebutuhan - durasi, 0)


def hitung_sleep_score(durasi, debt):
    skor = durasi * 10 - debt * 5
    return max(min(round(skor, 2), 100), 0)


def input_waktu(pesan):
    while True:
        waktu = input(pesan)
        try:
            datetime.strptime(waktu, "%H:%M")
            return waktu
        except:
            print("❌ Format salah! Contoh yang benar: 22:45\n")


def tampilkan_panduan():
    print("""
📘 PANDUAN MENGUKUR TIDUR

1. Durasi Tidur
   Ukur dari jam tidur sampai jam bangun. Jika melewati tengah malam, cukup input normal (contoh: 23:00 → 06:30).

2. Sleep Debt (Utang Tidur)
   Jika durasi < kebutuhan usia, selisihnya dihitung utang tidur.

3. Sleep Score
   Rumus: (durasi × 10) - (sleep debt × 5)
   Rentang hasil: 0 - 100

4. Interpretasi Sleep Score:
   ⭐ 85 - 100 → Sangat baik: tubuh pulih optimal
   🙂 70 - 84  → Cukup baik: masih dalam zona sehat
   😐 50 - 69 → Kurang: mulai menumpuk utang tidur
   🔴 < 50   → Buruk: risiko gangguan fokus, metabolisme, dan mood meningkat

5. Hal yang mempengaruhi kualitas tidur:
   - Konsistensi jam tidur
   - Tidak sering terbangun
   - Bangun dengan perasaan segar

Semakin rutin dan konsisten waktunya, semakin baik hasil tidurmu.
""")


# ======== PROGRAM UTAMA ========

print("👋 Selamat datang di Sleep Tracker!\n")

# Input usia
while True:
    usia = input("➡️ Masukkan usiamu: ")
    if usia.isdigit() and int(usia) > 0:
        usia = int(usia)
        break
    print("❌ Input harus angka dan lebih dari 0.\n")

kategori, kebutuhan_tidur = kategori_tidur(usia)

print(f"\n📍 Kamu termasuk kategori **{kategori}**.")
print(f"💤 Rekomendasi tidur: {kebutuhan_tidur} jam/hari\n")


# ======== LOOP MENU ========

while True:
    print("\n======= MENU UTAMA =======")
    print("1. Catat Tidur")
    print("2. Lihat Riwayat")
    print("3. Analisis Mingguan")
    print("4. Panduan Pengukuran")
    print("5. Keluar\n")

    pilihan = input("Pilih menu: ")

    # ---------------------------------
    # 1. PENCATATAN TIDUR
    # ---------------------------------
    if pilihan == "1":
        print("\n📌 Pilih Metode Pencatatan:")
        print("1. Catat hari ini")
        print("2. Catat beberapa hari sekaligus\n")

        mode = input("Pilih: ")

        # --- Mode satu hari ---
        if mode == "1":
            tidur = input_waktu("\n⏰ Jam tidur (HH:MM): ")
            bangun = input_waktu("⏰ Jam bangun (HH:MM): ")

            durasi = hitung_durasi(tidur, bangun)
            debt = hitung_sleep_debt(durasi, kebutuhan_tidur)
            skor = hitung_sleep_score(durasi, debt)

            riwayat_tidur.append({"durasi": durasi, "debt": debt, "skor": skor})

            print(f"\n😴 Durasi: {durasi} jam")
            print(f"⚠️ Sleep Debt: {debt} jam")
            print(f"⭐ Sleep Score: {skor}/100\n")

        # --- Mode banyak hari ---
        elif mode == "2":
            print("\n📆 MODE MULTI-DAY INPUT (ketik 'stop' untuk berhenti)")

            while True:
                tidur = input_waktu("\n⏰ Jam tidur (HH:MM): ")
                bangun = input_waktu("⏰ Jam bangun (HH:MM): ")

                durasi = hitung_durasi(tidur, bangun)
                debt = hitung_sleep_debt(durasi, kebutuhan_tidur)
                skor = hitung_sleep_score(durasi, debt)

                riwayat_tidur.append({"durasi": durasi, "debt": debt, "skor": skor})

                lanjut = input("➡️ Input hari berikutnya? (y/n): ").lower()
                if lanjut != "y":
                    print("\n📌 Input selesai.\n")
                    break

        else:
            print("\n❌ Pilihan tidak valid.\n")

    # ---------------------------------
    # 2. Riwayat
    # ---------------------------------
    elif pilihan == "2":
        if not riwayat_tidur:
            print("\n📄 Belum ada data tersimpan.")
        else:
            print("\n📄 Riwayat Tidur:\n")
            for i, r in enumerate(riwayat_tidur, 1):
                print(f"{i}. Durasi: {r['durasi']} jam | Debt: {r['debt']} jam | Skor: {r['skor']}/100")

    # ---------------------------------
    # 3. Analisis Mingguan
    # ---------------------------------
    elif pilihan == "3":
        if not riwayat_tidur:
            print("\n⚠️ Tidak ada data untuk dianalisis.")
        else:
            hari = len(riwayat_tidur)
            rata_durasi = sum(r["durasi"] for r in riwayat_tidur) / hari
            rata_debt = sum(r["debt"] for r in riwayat_tidur) / hari
            rata_skor = sum(r["skor"] for r in riwayat_tidur) / hari

            print("\n📊 ANALISIS MINGGUAN:")
            print(f"🗓 Data: {hari} hari")
            print(f"😴 Rata-rata durasi: {round(rata_durasi, 2)} jam")
            print(f"⚠️ Rata-rata sleep debt: {round(rata_debt, 2)} jam")
            print(f"⭐ Rata-rata sleep score: {round(rata_skor, 2)}/100\n")

    # ---------------------------------
    # 4. Panduan
    # ---------------------------------
    elif pilihan == "4":
        tampilkan_panduan()

    # ---------------------------------
    # 5. EXIT
    # ---------------------------------
    elif pilihan == "5":
        print("\n👋 Terima kasih sudah menggunakan Sleep Tracker!")
        sys.exit()

    else:
        print("\n❌ Menu tidak ditemukan.\n")
