"""
print_kc_stats.py — Cetak statistik data sintetis per KC untuk Tabel 4.X skripsi
Jalankan: python print_kc_stats.py
"""

import csv, os, sys
from collections import defaultdict

os.chdir(os.path.dirname(os.path.abspath(__file__)))

TRAIN = "data/matematika_grade1_train.csv"
TEST  = "data/matematika_grade1_test.csv"

rows = []
for f in [TRAIN, TEST]:
    rows += list(csv.DictReader(open(f)))

KC_NAMES = {
    "KC-B01": "Mengenal bilangan 1–10",
    "KC-B02": "Membilang 1–10",
    "KC-B03": "Mengenal bilangan 11–20",
    "KC-B04": "Membilang 11–20",
    "KC-B05": "Membandingkan dua bilangan",
    "KC-B06": "Urutan bilangan",
    "KC-B07": "Nilai tempat: satuan",
    "KC-B08": "Nilai tempat: puluhan",
    "KC-O01": "Konsep penjumlahan",
    "KC-O02": "Penjumlahan hasil sampai 10",
    "KC-O03": "Penjumlahan hasil sampai 20",
    "KC-O04": "Konsep pengurangan",
    "KC-O05": "Pengurangan dari bilangan sampai 10",
    "KC-O06": "Pengurangan dari bilangan sampai 20",
    "KC-O07": "Hubungan penjumlahan dan pengurangan",
    "KC-G01": "Mengenal bangun datar",
    "KC-G02": "Sifat bangun datar",
    "KC-G03": "Mengelompokkan bangun datar",
    "KC-P01": "Perbandingan panjang",
    "KC-P02": "Perbandingan berat",
    "KC-P03": "Urutan kejadian dan waktu",
    "KC-A01": "Mengenal pola berulang",
    "KC-A02": "Melanjutkan pola",
}

kc_stats = defaultdict(lambda: {"n": 0, "correct": 0})
for r in rows:
    kc_stats[r["kc_id"]]["n"]       += 1
    kc_stats[r["kc_id"]]["correct"] += int(r["correct"])

print("=" * 60)
print("Tabel 4.X  Statistik Data Sintetis per Knowledge Component")
print("=" * 60)
print(f"{'KC ID':<8}  {'Nama KC':<38}  {'Interaksi':>10}  {'Akurasi':>8}")
print("-" * 60)

total_n = total_c = 0
for kc_id in sorted(kc_stats):
    s    = kc_stats[kc_id]
    acc  = round(s["correct"] / s["n"] * 100, 1)
    name = KC_NAMES.get(kc_id, "-")
    print(f"{kc_id:<8}  {name:<38}  {s['n']:>10}  {acc:>7.1f}%")
    total_n += s["n"]
    total_c += s["correct"]

print("-" * 60)
print(f"{'Total':<48}  {total_n:>10}  {round(total_c/total_n*100,1):>7.1f}%")
print("=" * 60)

# Ringkasan
by_stu = defaultdict(int)
for r in rows: by_stu[r["student_id"]] += 1
counts = sorted(by_stu.values())
t = len(counts) // 3

print(f"\nRingkasan:")
print(f"  Total siswa       : {len(by_stu)} (160 latih / 40 uji)")
print(f"  Total interaksi   : {total_n}")
print(f"  Rata-rata per siswa: {round(total_n/len(by_stu),1)}")
print(f"  Min / Maks        : {min(counts)} / {max(counts)}")
print(f"  Akurasi rata-rata : {round(total_c/total_n*100,1)}%")
print(f"\nPer profil (estimasi):")
print(f"  Slow  (bawah 1/3) : {round(sum(counts[:t])/t,1)} interaksi/siswa")
print(f"  Average (tengah)  : {round(sum(counts[t:2*t])/t,1)} interaksi/siswa")
print(f"  Fast  (atas 1/3)  : {round(sum(counts[2*t:])/len(counts[2*t:]),1)} interaksi/siswa")
