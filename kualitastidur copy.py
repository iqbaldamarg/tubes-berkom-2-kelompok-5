from datetime import datetime
import sys

# ======================
# KAMUS (Daftar Variabel)
# ======================

# -------- Variabel Global --------
# riwayat_tidur        : array of dictionary   # menyimpan data tidur per hari (durasi, debt, skor)

# -------- Fungsi hitung_durasi --------
# waktu_tidur          : string                # input jam tidur dalam format "HH:MM"
# waktu_bangun         : string                # input jam bangun dalam format "HH:MM"
# format_waktu         : string                # format parsing waktu "%H:%M"
# start                : datetime              # waktu tidur setelah parsing
# end                  : datetime              # waktu bangun setelah parsing
# durasi               : float                 # lama tidur dalam jam

# -------- Fungsi kategori_tidur --------
# usia                 : integer               # umur pengguna
# kategori             : string                # kategori usia (Anak-anak / Remaja / Dewasa)
# kebutuhan            : integer               # kebutuhan tidur per hari (jam)

# -------- Fungsi hitung_sleep_debt --------
# durasi               : float                 # durasi tidur aktual
# kebutuhan            : integer               # kebutuhan tidur sesuai usia
# sleep_debt           : float                 # jumlah utang tidur jika durasi < kebutuhan

# -------- Fungsi hitung_sleep_score --------
# durasi               : float                 # durasi tidur
# debt                 : float                 # sleep debt
# skor                 : float                 # sleep score sebelum dibatasi 0–100

# -------- Fungsi input_waktu --------
# pesan                : string                # teks untuk prompt input
# waktu                : string                # input waktu pengguna (HH:MM)

# -------- Program Utama --------
# usia                 : integer               # usia pengguna
# kategori             : string                # kategori usia pengguna
# kebutuhan_tidur      : integer               # durasi tidur ideal sesuai kategori

# -------- Menu Utama --------
# pilihan              : string                # input pilihan menu utama (1–5)

# -------- Menu Catat Tidur --------
# mode                 : string                # metode pencatatan (1 = satu hari, 2 = multi-day)
# tidur                : string                # jam mulai tidur (HH:MM)
# bangun               : string                # jam bangun (HH:MM)
# durasi               : float                 # lama tidur hasil perhitungan
# debt                 : float                 # sleep debt per hari
# skor                 : float                 # sleep score per hari
# lanjut               : string                # pilihan lanjut input multi-day (y/n)

# -------- Menu Riwayat --------
# i                    : integer               # nomor urut data riwayat
# r                    : dictionary            # elemen riwayat tidur (durasi, debt, skor)

# -------- Menu Analisis Mingguan --------
# hari                 : integer               # jumlah hari data yang tersedia
# rata_durasi          : float                 # rata-rata durasi tidur
# rata_debt            : float                 # rata-rata sleep debt
# rata_skor            : float                 # rata-rata sleep score mingguan


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
          
6. Saran:
    - Sangat baik: Pertahankan kebiasaan ini!
    - Cukup baik: Sudah cukup baik, tapi bisa ditingkatkan.
    - Kurang: Usahakan tidur lebih awal dan hindari begadang.
    - Buruk: Waspada terhadap risiko kesehatan, coba perbaiki pola tidur.

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
           
            # Saran berdasarkan rata-rata sleep score
            if rata_skor >= 85:
                print("💡 Saran: Sangat baik - Pertahankan kebiasaan ini!")
            elif rata_skor >= 70:
                print("💡 Saran: Cukup baik - Sudah cukup baik, tapi bisa ditingkatkan.")
            elif rata_skor >= 50:
                print("💡 Saran: Kurang - Usahakan tidur lebih awal dan hindari begadang.")
            else:
                print("💡 Saran: Buruk - Waspada terhadap risiko kesehatan, coba perbaiki pola tidur.")

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
