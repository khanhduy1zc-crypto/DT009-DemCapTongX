# -*- coding: utf-8 -*-
"""
Demo DT009 — Đếm cặp chỉ số có tổng bằng X
Chạy: python demo.py (Windows) / python3 demo.py (Linux, macOS)
Sinh viên: Lê Khánh Duy — N24DCDT020
"""
import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from DeTai import (
    kiem_tra_dau_vao, dem_cap, liet_ke_cap,
    dem_cap_sau_sap_xep, dem_cap_hai_con_tro, sinh_mang_ngau_nhien,
)

NGAN_CACH = "=" * 78


def in_vidu(ten, a, X, expected):
    print(NGAN_CACH)
    print(ten)
    print(f"  Input : a = {a}, n = {len(a)}, X = {X}")
    hop_le, ly_do = kiem_tra_dau_vao(a, X)
    print(f"  Kiem tra dau vao: {'HOP LE' if hop_le else 'SAI — ' + ly_do}")
    if not hop_le:
        return
    c1 = dem_cap(a, X)
    c2 = dem_cap_sau_sap_xep(a, X)
    c3 = dem_cap_hai_con_tro(a, X)
    print(f"  So cap (duyet 2 vong O(n^2))     : {c1}")
    print(f"  So cap (sort + tim nhi phan)     : {c2}")
    print(f"  So cap (sort + hai con tro)      : {c3}")
    print(f"  Ky vong                           : {expected}")
    if len(a) <= 10:
        ds = liet_ke_cap(a, X)
        print(f"  Cac cap chi so 1-based (i<j)     : {ds}")
    assert c1 == c2 == c3 == expected, f"Ket qua 3 thuat toan khong khop hoac sai ky vong!"
    print("  => 3 thuat toan cho cung ket qua, dung voi ky vong.")


print(NGAN_CACH)
print("DE TAI CUOI KY — DT009: DEM TAT CA CAP CHI SO CO TONG BANG X")
print("Sinh vien: Le Khanh Duy — MSSV N24DCDT020 — Lop D24CQDT01-N")
print("Mon: Cau truc du lieu va giai thuat INT13185 — Nhom 03 — GV Ho Nhu Minh")
print(NGAN_CACH)

# --- Hai ví dụ trên phiếu ---
in_vidu("VI DU 1 (tren phieu): a=[1,2,2,3], X=4", [1, 2, 2, 3], 4, 2)
in_vidu("VI DU 2 (tren phieu): a=[2,2,2], X=4", [2, 2, 2], 4, 3)

# --- Năm ca kiểm tra bắt buộc trên phiếu ---
in_vidu("CA KIEM 1: a=[1,2,2,3], X=4", [1, 2, 2, 3], 4, 2)
in_vidu("CA KIEM 2: a=[2,2,2], X=4", [2, 2, 2], 4, 3)
in_vidu("CA KIEM 3: a=[1,4], X=8", [1, 4], 8, 0)
in_vidu("CA KIEM 4: a=[-2,0,2], X=0", [-2, 0, 2], 0, 1)
in_vidu("CA KIEM 5a: mang rong a=[], X=0", [], 0, 0)
in_vidu("CA KIEM 5b: mot phan tu a=[7], X=14", [7], 14, 0)
# --- Ca tu thiet ke va ca bien (cho anh A03-A07 theo rubric) ---
in_vidu("CA TU THIET KE 1 (A03): a=[7,7,7,7], X=14 — trung nhieu, C(4,2)=6", [7, 7, 7, 7], 14, 6)
in_vidu("CA TU THIET KE 2 (A04): a=[1,2,3,4,5], X=5 — khong trung, 2 cap (1,4),(2,3)", [1, 2, 3, 4, 5], 5, 2)
in_vidu("CA BIEN 1 (A05): mang rong a=[], X=0 — kich thuoc nho nhat", [], 0, 0)
in_vidu("CA BIEN 2 (A06): a=[1000000,1000000], X=2000000 — bien |X|=2e6", [1000000, 1000000], 2000000, 1)
in_vidu("CA BIEN 3 (A07): a=[1000000,-1000000], X=0 — bien |a[i]|=1e6", [1000000, -1000000], 0, 1)

# --- Đo thời gian ba thuật toán theo các quy mô trong phân tích phiếu ---
print(NGAN_CACH)
print("DO THOI GIAN 3 THUAT TOAN THEO QUY MO n (mang ngau nhien, cung seed)")
print(f"{'n':>6} | {'O(n^2) us':>12} | {'sort+np us':>12} | {'2 con tro us':>13} | {'ket qua':>8}")
print("-" * 78)
QUY_MO = [5, 20, 100, 500, 2000]
for n in QUY_MO:
    a = sinh_mang_ngau_nhien(n, seed=20261021 + n)
    X = 0  # X=0 làm tăng khả năng có cặp, đủ tổng quát
    t0 = time.perf_counter(); k1 = dem_cap(a, X); t1 = time.perf_counter()
    k2 = dem_cap_sau_sap_xep(a, X); t2 = time.perf_counter()
    k3 = dem_cap_hai_con_tro(a, X); t3 = time.perf_counter()
    assert k1 == k2 == k3
    print(f"{n:>6} | {(t1-t0)*1e6:>12.1f} | {(t2-t1)*1e6:>12.1f} | {(t3-t2)*1e6:>13.1f} | {k1:>8}")

print(NGAN_CACH)
print("Demo hoan tat. Xem log trong docs/logs/demo.log")
