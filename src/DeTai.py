# -*- coding: utf-8 -*-
"""
DT009 — Đếm tất cả cặp chỉ số có tổng bằng X
Sinh viên: Lê Khánh Duy — MSSV N24DCDT020 — Lớp D24CQDT01-N
Môn: Cấu trúc dữ liệu và giải thuật (INT13185) — Nhóm 03

Ba thuật toán:
  1. dem_cap            : duyệt hai vòng (trực tiếp)        — O(n^2), bộ nhớ O(1)
  2. dem_cap_sau_sap_xep: sắp xếp + tìm nhị phân phần bù    — O(n log n), bộ nhớ O(n)
  3. dem_cap_hai_con_tro: sắp xếp + hai con trỏ, gom trùng  — O(n log n), bộ nhớ O(n)
Hàm phụ:
  - kiem_tra_dau_vao : kiểm tra hợp đồng input theo phiếu
  - liet_ke_cap      : liệt kê các cặp chỉ số 1-based (dùng cho n nhỏ, n<=10)
"""

from bisect import bisect_left, bisect_right

# ---------------------------------------------------------------------------
# Hợp đồng đầu vào theo phiếu DT009
#   a: dãy số nguyên, 0 <= n <= 2000, |a[i]| <= 10^6
#   X: số nguyên, |X| <= 2*10^6
#   số cặp lưu bằng 64 bit (Python int tự động độ chính xác bất kỳ)
# ---------------------------------------------------------------------------
GIOI_HAN_N = 2000
GIOI_HAN_PT = 10 ** 6
GIOI_HAN_X = 2 * 10 ** 6


def kiem_tra_dau_vao(a, X):
    """Trả về (hop_le: bool, ly_do: str)."""
    if not isinstance(a, (list, tuple)):
        return False, "a phai la list hoac tuple cac so nguyen"
    n = len(a)
    if n < 0 or n > GIOI_HAN_N:
        return False, f"n = {n} nam ngoai mien 0..{GIOI_HAN_N}"
    for i, x in enumerate(a):
        if not isinstance(x, int) or isinstance(x, bool):
            return False, f"a[{i+1}] = {x!r} khong phai so nguyen"
        if abs(x) > GIOI_HAN_PT:
            return False, f"|a[{i+1}]| = {abs(x)} > {GIOI_HAN_PT}"
    if not isinstance(X, int) or isinstance(X, bool):
        return False, f"X = {X!r} khong phai so nguyen"
    if abs(X) > GIOI_HAN_X:
        return False, f"|X| = {abs(X)} > {GIOI_HAN_X}"
    return True, ""


# ---------------------------------------------------------------------------
# 1. Duyệt hai vòng — O(n^2)
# ---------------------------------------------------------------------------
def dem_cap(a, X):
    """Đếm số cặp chỉ số i<j (0-based trong code) sao cho a[i]+a[j]==X."""
    n = len(a)
    so_cap = 0
    for i in range(n):
        for j in range(i + 1, n):
            if a[i] + a[j] == X:
                so_cap += 1
    return so_cap


def liet_ke_cap(a, X):
    """Trả về danh sách các cặp chỉ số 1-based (i, j) với i<j và a[i]+a[j]==X."""
    n = len(a)
    ket_qua = []
    for i in range(n):
        for j in range(i + 1, n):
            if a[i] + a[j] == X:
                ket_qua.append((i + 1, j + 1))  # chuyển sang 1-based theo phiếu
    return ket_qua


# ---------------------------------------------------------------------------
# 2. Sắp xếp + tìm nhị phân phần bù — O(n log n)
#    Với mỗi phần tử b[i], đếm số lần xuất hiện của (X - b[i]) trong đoạn bên phải.
# ---------------------------------------------------------------------------
def dem_cap_sau_sap_xep(a, X):
    n = len(a)
    if n < 2:
        return 0
    b = sorted(a)
    so_cap = 0
    for i in range(n):
        target = X - b[i]
        # chỉ xét trong đoạn i+1 .. n-1 để mỗi cặp được đếm đúng một lần
        trai = bisect_left(b, target, i + 1, n)
        phai = bisect_right(b, target, i + 1, n)
        so_cap += (phai - trai)
    return so_cap


# ---------------------------------------------------------------------------
# 3. Sắp xếp + hai con trỏ, gom nhóm phần tử trùng — O(n log n)
# ---------------------------------------------------------------------------
def dem_cap_hai_con_tro(a, X):
    n = len(a)
    if n < 2:
        return 0
    b = sorted(a)
    trai = 0
    phai = n - 1
    so_cap = 0
    while trai < phai:
        tong = b[trai] + b[phai]
        if tong == X:
            if b[trai] == b[phai]:
                # Toàn bộ đoạn [trai..phai] đều bằng nhau (vì mảng đã sắp xếp)
                so_luong = phai - trai + 1
                so_cap += so_luong * (so_luong - 1) // 2  # C(k,2)
                break
            # Gom nhóm các phần tử trùng ở hai đầu
            dem_trai = 1
            while trai + dem_trai < phai and b[trai + dem_trai] == b[trai]:
                dem_trai += 1
            dem_phai = 1
            while phai - dem_phai > trai and b[phai - dem_phai] == b[phai]:
                dem_phai += 1
            so_cap += dem_trai * dem_phai
            trai += dem_trai
            phai -= dem_phai
        elif tong < X:
            trai += 1
        else:
            phai -= 1
    return so_cap


# ---------------------------------------------------------------------------
# Hàm tiện ích: sinh mảng ngẫu nhiên trong miền hợp lệ để đo thời gian
# ---------------------------------------------------------------------------
import random


def sinh_mang_ngau_nhien(n, seed=None):
    if seed is not None:
        random.seed(seed)
    return [random.randint(-GIOI_HAN_PT, GIOI_HAN_PT) for _ in range(n)]
