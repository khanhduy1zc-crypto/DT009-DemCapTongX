# DT009 — Đếm tất cả cặp chỉ số có tổng bằng X

**Sinh viên:** Lê Khánh Duy — MSSV N24DCDT020 — Lớp D24CQDT01-N
**Môn:** Cấu trúc dữ liệu và giải thuật (INT13185) — Nhóm 03 — GV Hồ Nhựt Minh
**Ngôn ngữ:** Python 3.14.7 (chỉ dùng thư viện chuẩn)

## Đề bài
Đếm các cặp chỉ số `i < j` sao cho `a[i] + a[j] == X`. Các phần tử bằng nhau vẫn có chỉ số riêng; không dùng một vị trí hai lần. Với `n ≤ 10`, in thêm danh sách cặp chỉ số 1-based.

## Hợp đồng đầu vào (theo phiếu)
- `a`: dãy số nguyên, `0 ≤ n ≤ 2000`, `|a[i]| ≤ 10^6`
- `X`: số nguyên, `|X| ≤ 2·10^6`
- Số cặp lưu bằng 64 bit (Python int tự động độ chính xác bất kỳ)

## Cấu trúc thư mục
```
DT009_LeKhanhDuy/
├── README.md
├── demo.py                  # Chạy ví dụ + ca kiểm + đo thời gian
├── src/
│   └── DeTai.py             # 3 thuật toán + validator + sinh dữ liệu
├── test/
│   └── runtests.py          # 23 ca kiểm thử độc lập (PASS hết)
├── scripts/
│   └── trace_scales.py      # Sinh bảng truy vết tay và khảo sát quy mô
└── docs/
    ├── anh_ket_qua/         # Lưu 11 ảnh A01–A11 (sinh viên tự chụp)
    └── logs/                # Log chạy thật: demo.log, tests.log, trace.log
```

## Các hàm chính
| Hàm | Mô tả | Độ phức tạp thời gian | Bộ nhớ |
|---|---|---|---|
| `kiem_tra_dau_vao(a, X)` | Kiểm tra hợp đồng input | O(n) | O(1) |
| `dem_cap(a, X)` | Duyệt hai vòng, đếm cặp | O(n²) | O(1) |
| `liet_ke_cap(a, X)` | Liệt kê cặp chỉ số 1-based | O(n²) | O(k), k=số cặp |
| `dem_cap_sau_sap_xep(a, X)` | Sort + tìm nhị phân phần bù | O(n log n) | O(n) |
| `dem_cap_hai_con_tro(a, X)` | Sort + hai con trỏ, gom trùng | O(n log n) | O(n) |

## Chạy chương trình
Mở terminal tại thư mục dự án:
```powershell
python --version          # Python 3.14.7
python demo.py            # Chạy ví dụ + 5 ca bắt buộc + đo thời gian
python test/runtests.py   # Chạy bộ kiểm thử 23 ca
python scripts/trace_scales.py  # Sinh bảng truy vết tay
```

## Kết quả kiểm thử
- **23/23 ca kiểm thử độc lập PASS** (xem `docs/logs/tests.log`)
- 3 thuật toán luôn cho cùng kết quả trên mọi ca (bất biến đối chứng)
- Ví dụ 1: `[1,2,2,3], X=4 → 2 cặp: (1,4), (2,3)`
- Ví dụ 2: `[2,2,2], X=4 → 3 cặp: (1,2), (1,3), (2,3)`

## GitHub và commit
- Commit C (mã/test/input dùng chạy và chụp ảnh): xem `git rev-parse HEAD`
- Commit S (thêm ảnh/báo cáo): tạo sau khi chụp đủ 11 ảnh
- Clone chạy lại:
  ```powershell
  git clone <URL_REPO_CUA_BAN> kiem_tra_DT009
  cd kiem_tra_DT009
  python demo.py
  python test/runtests.py
  ```

## Lưu ý
- Không dùng ảnh mẫu BFS làm bằng chứng cá nhân. Chụp ảnh thật từ máy mình.
- Điền `ThongTinNop.txt` sau khi chốt commit S, nộp rời cùng Word, PDF, ZIP mã.
