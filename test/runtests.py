# -*- coding: utf-8 -*-
"""
Bộ kiểm thử DT009 — Đếm cặp chỉ số có tổng bằng X
Sinh viên: Lê Khánh Duy — N24DCDT020
Ít nhất 12 ca kiểm thử độc lập. Mỗi ca có ID, đối tượng/hàm, input, mục tiêu,
kỳ vọng (tính độc lập), kết quả thực tế và PASS/FAIL.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from DeTai import (
    kiem_tra_dau_vao, dem_cap, liet_ke_cap,
    dem_cap_sau_sap_xep, dem_cap_hai_con_tro, sinh_mang_ngau_nhien,
)

PASS = 0
FAIL = 0
SO_CA = 0
KET_QUA = []


def chay_ca(ma_ca, doi_tuong, input_mo_ta, muc_tieu, expected, actual):
    global PASS, FAIL, SO_CA
    SO_CA += 1
    ok = (actual == expected)
    if ok:
        PASS += 1
        trang_thai = "PASS"
    else:
        FAIL += 1
        trang_thai = "FAIL"
    KET_QUA.append((ma_ca, doi_tuong, input_mo_ta, muc_tieu, expected, actual, trang_thai))
    print(f"[{trang_thai}] {ma_ca} | {doi_tuong} | {muc_tieu}")
    print(f"        input : {input_mo_ta}")
    print(f"        expected = {expected} | actual = {actual}")
    return ok


def chay_ca_validator(ma_ca, input_mo_ta, muc_tieu, a, X, expected_hop_le):
    global PASS, FAIL, SO_CA
    SO_CA += 1
    hop_le, ly_do = kiem_tra_dau_vao(a, X)
    ok = (hop_le == expected_hop_le)
    if ok:
        PASS += 1
        trang_thai = "PASS"
    else:
        FAIL += 1
        trang_thai = "FAIL"
    KET_QUA.append((ma_ca, "kiem_tra_dau_vao", input_mo_ta, muc_tieu,
                    f"hop_le={expected_hop_le}", f"hop_le={hop_le} ({ly_do})", trang_thai))
    print(f"[{trang_thai}] {ma_ca} | kiem_tra_dau_vao | {muc_tieu}")
    print(f"        input : {input_mo_ta}")
    print(f"        expected hop_le={expected_hop_le} | actual hop_le={hop_le} ({ly_do})")
    return ok


print("=" * 78)
print("BO KIEM THU DT009 — Dem cap chi so co tong bang X")
print("Sinh vien: Le Khanh Duy — N24DCDT020 — Lop D24CQDT01-N")
print("=" * 78)

# --- A01: Ví dụ 1 trên phiếu ------------------------------------------------
chay_ca("A01", "dem_cap (O(n^2))", "a=[1,2,2,3], X=4",
        "Vi du 1 tren phieu: hai so 2 o vi tri 2,3 tao 1 cap, cong cap (1,3)=4",
        2, dem_cap([1, 2, 2, 3], 4))
chay_ca("A01b", "dem_cap_sau_sap_xep", "a=[1,2,2,3], X=4",
        "Doi chinh ket qua sort+binary search voi ban truc tiep o vi du 1",
        2, dem_cap_sau_sap_xep([1, 2, 2, 3], 4))
chay_ca("A01c", "dem_cap_hai_con_tro", "a=[1,2,2,3], X=4",
        "Doi chinh ket qua hai con tro o vi du 1",
        2, dem_cap_hai_con_tro([1, 2, 2, 3], 4))

# --- A02: Ví dụ 2 trên phiếu — phần tử trùng --------------------------------
chay_ca("A02", "dem_cap", "a=[2,2,2], X=4",
        "Vi du 2: 3 cach chon 2 chi so trong 3 vi tri = C(3,2)=3",
        3, dem_cap([2, 2, 2], 4))
chay_ca("A02b", "liet_ke_cap", "a=[2,2,2], X=4",
        "Liet ke dung 3 cap 1-based, khong lap (i,j)/(j,i)",
        [(1, 2), (1, 3), (2, 3)], liet_ke_cap([2, 2, 2], 4))

# --- A03: Ca 3 phiếu — không có cặp -----------------------------------------
chay_ca("A03", "dem_cap", "a=[1,4], X=8",
        "Ca 3 phieu: khong co cap nao tong bang 8",
        0, dem_cap([1, 4], 8))

# --- A04: Ca 4 phiếu — số âm, tổng bằng 0 -----------------------------------
chay_ca("A04", "dem_cap", "a=[-2,0,2], X=0",
        "Ca 4 phieu: chi co cap (-2,2) o vi tri 1 va 3",
        1, dem_cap([-2, 0, 2], 0))
chay_ca("A04b", "liet_ke_cap", "a=[-2,0,2], X=0",
        "Liet ke dung chi so 1-based cua cap so am",
        [(1, 3)], liet_ke_cap([-2, 0, 2], 0))

# --- A05: Ca 5 phiếu — mảng rỗng --------------------------------------------
chay_ca("A05", "dem_cap", "a=[], X=0",
        "Ca 5 phieu: mang rong co 0 cap",
        0, dem_cap([], 0))

# --- A06: Biên — mảng 1 phần tử ---------------------------------------------
chay_ca("A06", "dem_cap", "a=[5], X=10",
        "Biên n=1: khong the tao cap i<j",
        0, dem_cap([5], 10))

# --- A07: Phần tử trùng nhiều — công thức tổ hợp ----------------------------
chay_ca("A07", "dem_cap", "a=[7,7,7,7], X=14",
        "4 phan tu bang nhau: C(4,2)=6 cap",
        6, dem_cap([7, 7, 7, 7], 14))
chay_ca("A07b", "dem_cap_sau_sap_xep", "a=[7,7,7,7], X=14",
        "Sort+binary search dem dung 6 cap trung",
        6, dem_cap_sau_sap_xep([7, 7, 7, 7], 14))
chay_ca("A07c", "dem_cap_hai_con_tro", "a=[7,7,7,7], X=14",
        "Hai con tro gom nhom trung phai dem dung C(4,2)=6",
        6, dem_cap_hai_con_tro([7, 7, 7, 7], 14))

# --- A08: X=0, toàn bộ phần tử bằng 0 ---------------------------------------
chay_ca("A08", "dem_cap", "a=[0,0,0,0,0], X=0",
        "5 so 0, X=0: moi cap deu thoa = C(5,2)=10",
        10, dem_cap([0, 0, 0, 0, 0], 0))

# --- A09: Biên |a[i]| = 10^6 ------------------------------------------------
chay_ca("A09", "dem_cap", "a=[1000000, -1000000], X=0",
        "Biên gia tri tuyet doi lon nhat: 1e6 + (-1e6) = 0",
        1, dem_cap([1000000, -1000000], 0))

# --- A10: Biên |X| = 2*10^6 -------------------------------------------------
chay_ca("A10", "dem_cap", "a=[1000000, 1000000], X=2000000",
        "Biên X lon nhat: 1e6 + 1e6 = 2e6",
        1, dem_cap([1000000, 1000000], 2000000))

# --- A11: Mảng không trùng, nhiều cặp đồng thời -----------------------------
chay_ca("A11", "dem_cap", "a=[1,2,3,4,5], X=5",
        "Khong trung: (1,4) va (2,3) -> 2 cap",
        2, dem_cap([1, 2, 3, 4, 5], 5))
chay_ca("A11b", "liet_ke_cap", "a=[1,2,3,4,5], X=5",
        "Liet ke dung 2 cap 1-based: (1,4) va (2,3)",
        [(1, 4), (2, 3)], liet_ke_cap([1, 2, 3, 4, 5], 5))

# --- A12: Input sai — phần tử không phải số nguyên --------------------------
chay_ca_validator("A12", "a=[1, 2.5], X=3",
                  "Input sai: phan tu thuc khong hop le",
                  [1, 2.5], 3, False)

# --- A13: Input sai — n vượt miền -------------------------------------------
chay_ca_validator("A13", "n=2001 (vuot 2000)",
                  "Input sai: kich thuoc mang vuot mien 0..2000",
                  [0] * 2001, 0, False)

# --- A14: Input sai — |a[i]| vượt miền --------------------------------------
chay_ca_validator("A14", "a=[1000001, 0], X=0",
                  "Input sai: |a[i]| vuot 10^6",
                  [1000001, 0], 0, False)

# --- A15: Đối chứng ba thuật toán trên mảng ngẫu nhiên ----------------------
mang_ngau = sinh_mang_ngau_nhien(50, seed=20261021)
X_ngau = 123456
d1 = dem_cap(mang_ngau, X_ngau)
d2 = dem_cap_sau_sap_xep(mang_ngau, X_ngau)
d3 = dem_cap_hai_con_tro(mang_ngau, X_ngau)
chay_ca("A15", "3 thuat toan", "n=50 ngau nhien, X=123456",
        "Bat bien: ket qua 3 thuat toan phai bang nhau",
        (d1, d1), (d2, d3))

# --- A16: Liệt kê ví dụ 1 — đúng chỉ số 1-based -----------------------------
chay_ca("A16", "liet_ke_cap", "a=[1,2,2,3], X=4",
        "Vi du 1: cac cap (1,4) va (2,3) theo chi so 1-based",
        [(1, 4), (2, 3)], liet_ke_cap([1, 2, 2, 3], 4))

# --- Tổng kết ---------------------------------------------------------------
print("=" * 78)
print(f"TONG KET: {SO_CA} ca kiem thu doc lap | PASS = {PASS} | FAIL = {FAIL}")
print("=" * 78)

if FAIL > 0:
    print("\nCac ca FAIL:")
    for hang in KET_QUA:
        if hang[6] == "FAIL":
            print("  ", hang[0], hang[1], "| expected:", hang[4], "| actual:", hang[5])
    sys.exit(1)
else:
    print("Tat ca ca kiem thu deu dat.")
    sys.exit(0)
