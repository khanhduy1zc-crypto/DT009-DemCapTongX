# -*- coding: utf-8 -*-
"""
Sinh bảng truy vết tay (lần vết) cho thuật toán dem_cap O(n^2)
trên Ví dụ 1 và Ví dụ 2 của phiếu DT009, đồng thời khảo sát chi tiết
số phép so sánh theo quy mô.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from DeTai import dem_cap


def trace_dem_cap(a, X, ten):
    n = len(a)
    print("=" * 70)
    print(f"LAN VET (TRUY VET TAY) — {ten}")
    print(f"a = {a} (1-based), X = {X}")
    print("-" * 70)
    print(f"{'i':>3} {'j':>3} {'a[i]':>6} {'a[j]':>6} {'a[i]+a[j]':>10} {'==X?':>6} {'so_cap':>7}")
    print("-" * 70)
    so_cap = 0
    so_so_sanh = 0
    for i in range(n):
        for j in range(i + 1, n):
            so_so_sanh += 1
            tong = a[i] + a[j]
            dat = (tong == X)
            if dat:
                so_cap += 1
            print(f"{i+1:>3} {j+1:>3} {a[i]:>6} {a[j]:>6} {tong:>10} {'CO' if dat else 'khong':>6} {so_cap:>7}")
    print("-" * 70)
    print(f"Tong so phep so sánh: {so_so_sanh} = n(n-1)/2 = {n}*({n}-1)/2 = {n*(n-1)//2}")
    print(f"So cap dat: {so_cap}  (ky vong = {dem_cap(a, X)})")
    print()


trace_dem_cap([1, 2, 2, 3], 4, "Vi du 1: a=[1,2,2,3], X=4")
trace_dem_cap([2, 2, 2], 4, "Vi du 2: a=[2,2,2], X=4")
trace_dem_cap([-2, 0, 2], 0, "Ca kiem 4: a=[-2,0,2], X=0")

# Khảo sát số phép so sánh của bản O(n^2) theo n
print("=" * 70)
print("KHAO SAT SO PHEP SO SANH CUA BAN O(n^2) THEO n")
print(f"{'n':>6} | {'so phep so sanh = n(n-1)/2':>28}")
print("-" * 70)
for n in [5, 20, 100, 500, 2000]:
    print(f"{n:>6} | {n*(n-1)//2:>28}")
print("=" * 70)
