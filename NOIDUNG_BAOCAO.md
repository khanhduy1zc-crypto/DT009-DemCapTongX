# NỘI DUNG BÁO CÁO ĐỀ TÀI CUỐI KỲ — DT009

**Sinh viên:** Lê Khánh Duy — MSSV N24DCDT020 — Lớp D24CQDT01-N
**Môn:** Cấu trúc dữ liệu và giải thuật (INT13185) — Nhóm 03 — GV Hồ Nhựt Minh
**Đề tài:** DT009 — Đếm tất cả cặp chỉ số có tổng bằng X
**Ngôn ngữ:** Python 3.14.7 (chỉ dùng thư viện chuẩn)
**Commit C (mã/test/input):** [THAY BẰNG SHA THẬT từ `git rev-parse HEAD` trên máy sinh viên sau khi push]

> Hướng dẫn: Copy từng chương vào khung Word `02_Mau_bao_cao_de_tai_ca_nhan.docx`,
> dán bảng vào đúng chỗ, chèn ảnh A01–A11 vào các khung ảnh, cập nhật mục lục.

---

## CHƯƠNG 1: ĐẶC TẢ BÀI TOÁN

### 1.1 Bài toán
Đếm số lượng các cặp chỉ số `(i, j)` với `i < j` sao cho tổng hai phần tử tương ứng
`a[i] + a[j] == X`. Các phần tử có giá trị bằng nhau vẫn được coi là khác nhau vì
gắn với chỉ số khác nhau; không được dùng cùng một vị trí hai lần. Với `n ≤ 10`,
chương trình in thêm danh sách các cặp chỉ số theo quy ước 1-based, không in lặp
`(i, j)` và `(j, i)`.

### 1.2 Mục tiêu
- Tự cài đặt hàm đếm cặp theo phương pháp duyệt hai vòng (O(n²)).
- Cài đặt thêm phương pháp sau khi sắp xếp (O(n log n)) để đối chứng kết quả và
  so sánh hiệu năng.
- Xử lý đúng trường hợp phần tử trùng (đếm theo chỉ số, không theo giá trị).
- Chạy đủ hai ví dụ và năm ca kiểm tra trên phiếu; bổ sung đủ 12 ca kiểm thử độc lập.

### 1.3 Phạm vi
- `n` từ 0 đến 2000; `|a[i]| ≤ 10^6`; `|X| ≤ 2·10^6`.
- Số cặp lưu bằng kiểu 64 bit (trong Python là int độ chính xác bất kỳ).
- Dữ liệu nhập từ bàn phím hoặc khai báo trực tiếp trong chương trình; không dùng
  file ngoài.

### 1.4 Hợp đồng đầu vào / đầu ra
**Đầu vào:**
- `a`: dãy số nguyên, `0 ≤ n ≤ 2000`, `|a[i]| ≤ 10^6`.
- `X`: số nguyên, `|X| ≤ 2·10^6`.

**Đầu ra:**
- Số cặp `(i, j)` với `i < j` và `a[i] + a[j] == X` (kiểu nguyên, 64 bit).
- Nếu `n ≤ 10`: in thêm danh sách cặp chỉ số 1-based `(i, j)`, `i < j`.

**Hai ví dụ trên phiếu:**
- Ví dụ 1: `a = [1, 2, 2, 3]`, `X = 4` → **2 cặp**: `(1, 4)` và `(2, 3)`.
  (Hai số 2 ở vị trí 2 và 3 tạo một cặp; số 1 ở vị trí 1 cộng số 3 ở vị trí 4 bằng 4.)
- Ví dụ 2: `a = [2, 2, 2]`, `X = 4` → **3 cặp**: `(1,2), (1,3), (2,3)`.
  (Ba cách chọn hai chỉ số trong ba vị trí: C(3,2) = 3.)

---

## CHƯƠNG 2: CƠ SỞ LÝ THUYẾT VÀ CẤU TRÚC DỮ LIỆU

### 2.1 Cơ sở giáo trình
- Chương 1, Mục 1.6 bài 21; liên hệ Mục 2.8 bài 25.
- Trang in 32, 61; trang PDF 44, 73 (Giáo trình INT1306).

### 2.2 Quy ước
- Chỉ số mảng trong báo cáo và output dùng **1-based** theo yêu cầu phiếu; trong
  code dùng 0-based và chuyển đổi khi in ra.
- Cặp `(i, j)` chỉ tính khi `i < j`, đảm bảo mỗi cặp được đếm đúng một lần.
- Phần tử trùng giá trị nhưng khác chỉ số vẫn được tính là các cặp riêng biệt.

### 2.3 Cấu trúc dữ liệu sử dụng
- **Mảng (list) một chiều** `a`: lưu dãy số nguyên đầu vào.
- **Biến đếm `so_cap`**: kiểu nguyên, lưu số cặp thỏa mãn (tối đa C(2000,2) ≈ 2·10⁶,
  vừa 32 bit nhưng dùng 64 bit theo yêu cầu).
- **Danh sách cặp** `ket_qua`: chỉ dùng khi `n ≤ 10`, lưu các bộ `(i, j)` 1-based.
- **Mảng đã sắp xếp `b`**: dùng trong hai thuật toán O(n log n), là bản sao của `a`
  đã được sắp xếp tăng dần.
- **Con trỏ `trai`, `phai`**: dùng trong thuật toán hai con trỏ.

### 2.4 Nguyên lý các thuật toán
**Thuật toán 1 — Duyệt hai vòng (trực tiếp), O(n²):**
Xét mọi cặp chỉ số `i < j`; nếu `a[i] + a[j] == X` thì tăng biến đếm. Đúng vì
là duyệt toàn bộ không gian lời giải.

**Thuật toán 2 — Sắp xếp + tìm nhị phân phần bù, O(n log n):**
Sắp xếp `a` thành `b`. Với mỗi phần tử `b[i]`, phần còn lại cần tìm là
`target = X - b[i]`. Đếm số lần xuất hiện của `target` trong đoạn `b[i+1..n-1]`
bằng tìm nhị phân (`bisect_left`, `bisect_right`). Chỉ xét đoạn bên phải để mỗi
cặp được đếm đúng một lần.

**Thuật toán 3 — Sắp xếp + hai con trỏ, O(n log n):**
Sắp xếp `a` thành `b`. Đặt `trai = 0`, `phai = n-1`. Nếu `b[trai] + b[phai] == X`:
- Nếu `b[trai] == b[phai]` thì toàn bộ đoạn giữa đều bằng nhau, số cặp là C(k,2).
- Ngược lại, gom nhóm các phần tử trùng ở hai đầu, cộng `dem_trai * dem_phai`,
  rồi di chuyển cả hai con trỏ qua nhóm.
Nếu tổng `< X` thì tăng `trai`; nếu `> X` thì giảm `phai`.

---

## CHƯƠNG 3: THIẾT KẾ THUẬT TOÁN VÀ CHỨNG MINH

### 3.1 Các hàm và tiền/hậu điều kiện

| Hàm | Tiền điều kiện | Hậu điều kiện |
|---|---|---|
| `kiem_tra_dau_vao(a,X)` | `a` là dãy, `X` là số | Trả về `(True,"")` nếu hợp lệ; `(False, lý do)` nếu sai |
| `dem_cap(a,X)` | Đầu vào hợp lệ | Trả về số cặp `i<j` có tổng bằng X, không sửa `a` |
| `liet_ke_cap(a,X)` | Đầu vào hợp lệ | Trả về danh sách cặp `(i,j)` 1-based, `i<j`, không lặp |
| `dem_cap_sau_sap_xep(a,X)` | Đầu vào hợp lệ | Trả về số cặp bằng `dem_cap`, không sửa `a` gốc |
| `dem_cap_hai_con_tro(a,X)` | Đầu vào hợp lệ | Trả về số cặp bằng `dem_cap`, không sửa `a` gốc |

### 3.2 Giả mã (pseudocode)

**Giả mã `dem_cap` (O(n²)):**
```
hàm dem_cap(a, X):
    n ← độ dài(a)
    so_cap ← 0
    cho i từ 0 đến n-1:
        cho j từ i+1 đến n-1:
            nếu a[i] + a[j] = X:
                so_cap ← so_cap + 1
    trả về so_cap
```

**Giả mã `dem_cap_sau_sap_xep` (O(n log n)):**
```
hàm dem_cap_sau_sap_xep(a, X):
    n ← độ dài(a)
    nếu n < 2: trả về 0
    b ← sắp xếp tăng(a)
    so_cap ← 0
    cho i từ 0 đến n-1:
        target ← X - b[i]
        trai ← vị trí đầu tiên của target trong b[i+1..n-1]
        phai ← vị trí sau cuối của target trong b[i+1..n-1]
        so_cap ← so_cap + (phai - trai)
    trả về so_cap
```

**Giả mã `dem_cap_hai_con_tro` (O(n log n)):**
```
hàm dem_cap_hai_con_tro(a, X):
    n ← độ dài(a)
    nếu n < 2: trả về 0
    b ← sắp xếp tăng(a)
    trai ← 0; phai ← n-1; so_cap ← 0
    trong khi trai < phai:
        tong ← b[trai] + b[phai]
        nếu tong = X:
            nếu b[trai] = b[phai]:
                k ← phai - trai + 1
                so_cap ← so_cap + k*(k-1)/2
                thoát
            dem_trai ← số phần tử liên tiếp = b[trai] (từ trai)
            dem_phai ← số phần tử liên tiếp = b[phai] (từ phai)
            so_cap ← so_cap + dem_trai * dem_phai
            trai ← trai + dem_trai; phai ← phai - dem_phai
        ngược lại nếu tong < X: trai ← trai + 1
        ngược lại: phai ← phai - 1
    trả về so_cap
```

### 3.3 Truy vết tay (lần vết) — Ví dụ 1
`a = [1, 2, 2, 3]` (1-based), `X = 4`. Ban đầu `so_cap = 0`.

| i | j | a[i] | a[j] | a[i]+a[j] | == X? | so_cap sau |
|---|---|------|------|-----------|-------|------------|
| 1 | 2 | 1 | 2 | 3 | không | 0 |
| 1 | 3 | 1 | 2 | 3 | không | 0 |
| 1 | 4 | 1 | 3 | 4 | **có** | 1 |
| 2 | 3 | 2 | 2 | 4 | **có** | 2 |
| 2 | 4 | 2 | 3 | 5 | không | 2 |
| 3 | 4 | 2 | 3 | 5 | không | 2 |

Tổng số phép so sánh: 6 = n(n-1)/2 = 4·3/2. Kết quả: **2 cặp**, đúng kỳ vọng.

### 3.4 Chứng minh tính đúng
- **`dem_cap`:** Duyệt toàn bộ các cặp `i < j` (không lặp, không thiếu). Mỗi cặp
  được xét đúng một lần. Điều kiện `a[i]+a[j]==X` chính là định nghĩa bài toán.
  → Đúng.
- **`dem_cap_sau_sap_xep`:** Sắp xếp không làm thay đổi tập hợp giá trị và số lần
  xuất hiện. Với mỗi `b[i]`, chỉ xét phần bù `X-b[i]` trong đoạn bên phải nên mỗi
  cặp được đếm đúng một lần (phần tử nhỏ hơn trong cặp luôn đứng trước sau khi sắp
  xếp, trừ khi bằng nhau — nhưng đoạn bên phải vẫn đảm bảo i<j trong mảng đã sắp).
  → Đúng.
- **`dem_cap_hai_con_tro`:** Vì mảng đã sắp xếp, nếu tổng hai đầu nhỏ hơn X thì
  phải tăng đầu trái; nếu lớn hơn X thì phải giảm đầu phải. Khi bằng X, gom nhóm
  trùng đảm bảo đếm đủ tổ hợp giữa hai nhóm giá trị; khi hai đầu bằng nhau thì toàn
  bộ đoạn giữa cùng giá trị, dùng C(k,2). → Đúng.
- **Bất biến đối chứng:** Trên mọi ca kiểm thử, `dem_cap(a,X) ==
  dem_cap_sau_sap_xep(a,X) == dem_cap_hai_con_tro(a,X)`.

### 3.5 Độ phức tạp

| Thuật toán | Thời gian | Bộ nhớ phụ | Ghi chú |
|---|---|---|---|
| `dem_cap` | O(n²) | O(1) | Số phép so sánh đúng bằng n(n-1)/2 |
| `dem_cap_sau_sap_xep` | O(n log n) | O(n) | Sort O(n log n) + n lần tìm nhị phân O(log n) |
| `dem_cap_hai_con_tro` | O(n log n) | O(n) | Sort O(n log n) + duyệt 2 con trỏ O(n) |

Số phép so sánh của bản O(n²) theo n: n=5→10, n=20→190, n=100→4950,
n=500→124750, n=2000→1999000.

---

## CHƯƠNG 4: KIỂM THỬ VÀ KẾT QUẢ

### 4.1 Môi trường
- Hệ điều hành: Windows 10/11, Python 3.14.7 (chạy kiểm thử trên máy sinh viên).
- Chỉ dùng thư viện chuẩn (`bisect`, `random`, `time`, `sys`, `os`).
- Lệnh chạy (trong PowerShell tại thư mục dự án):
  - Ví dụ/ca kiểm/đo thời gian: `python demo.py`
  - Bộ kiểm thử: `python test/runtests.py`
  - Truy vết tay: `python scripts/trace_scales.py`

### 4.2 Bảng kiểm thử tổng hợp (23 ca độc lập, PASS hết)

| ID | Đối tượng | Input | Mục tiêu | Kỳ vọng | Kết quả | Trạng thái |
|---|---|---|---|---|---|---|
| A01 | dem_cap | [1,2,2,3], X=4 | Ví dụ 1 phiếu | 2 | 2 | PASS |
| A01b | sort+np | [1,2,2,3], X=4 | Đối chứng ví dụ 1 | 2 | 2 | PASS |
| A01c | 2 con trỏ | [1,2,2,3], X=4 | Đối chứng ví dụ 1 | 2 | 2 | PASS |
| A02 | dem_cap | [2,2,2], X=4 | Ví dụ 2, trùng | 3 | 3 | PASS |
| A02b | liet_ke_cap | [2,2,2], X=4 | Liệt kê 3 cặp 1-based | [(1,2),(1,3),(2,3)] | đúng | PASS |
| A03 | dem_cap | [1,4], X=8 | Không có cặp | 0 | 0 | PASS |
| A04 | dem_cap | [-2,0,2], X=0 | Số âm, tổng 0 | 1 | 1 | PASS |
| A04b | liet_ke_cap | [-2,0,2], X=0 | Liệt kê cặp âm | [(1,3)] | đúng | PASS |
| A05 | dem_cap | [], X=0 | Mảng rỗng | 0 | 0 | PASS |
| A06 | dem_cap | [5], X=10 | n=1 | 0 | 0 | PASS |
| A07 | dem_cap | [7,7,7,7], X=14 | Trùng nhiều, C(4,2) | 6 | 6 | PASS |
| A07b | sort+np | [7,7,7,7], X=14 | Đối chứng trùng | 6 | 6 | PASS |
| A07c | 2 con trỏ | [7,7,7,7], X=14 | Gom nhóm trùng | 6 | 6 | PASS |
| A08 | dem_cap | [0,0,0,0,0], X=0 | Toàn bộ thỏa, C(5,2) | 10 | 10 | PASS |
| A09 | dem_cap | [1e6,-1e6], X=0 | Biên \|a[i]\|=1e6 | 1 | 1 | PASS |
| A10 | dem_cap | [1e6,1e6], X=2e6 | Biên \|X\|=2e6 | 1 | 1 | PASS |
| A11 | dem_cap | [1,2,3,4,5], X=5 | Không trùng, nhiều cặp | 2 | 2 | PASS |
| A11b | liet_ke_cap | [1,2,3,4,5], X=5 | Liệt kê (1,4),(2,3) | [(1,4),(2,3)] | đúng | PASS |
| A12 | validator | [1,2.5], X=3 | Input sai: phần tử thực | Không hợp lệ | đúng | PASS |
| A13 | validator | n=2001 | Input sai: vượt n | Không hợp lệ | đúng | PASS |
| A14 | validator | [1000001,0], X=0 | Input sai: vượt \|a[i]\| | Không hợp lệ | đúng | PASS |
| A15 | 3 thuật toán | n=50 ngẫu nhiên, X=123456 | Bất biến: 3 kết quả bằng nhau | bằng nhau | đúng | PASS |
| A16 | liet_ke_cap | [1,2,2,3], X=4 | Liệt kê ví dụ 1 | [(1,4),(2,3)] | đúng | PASS |

**Tổng kết: 23/23 ca PASS.**

### 4.3 Ba quy mô khảo sát thời gian (mảng ngẫu nhiên, cùng seed)

| n | O(n²) (µs) | sort+tìm nhị phân (µs) | hai con trỏ (µs) | Kết quả |
|---|-----------|------------------------|------------------|---------|
| 5 | 2.5 | 3.4 | 1.6 | 0 |
| 20 | 9.5 | 27.0 | 2.6 | 0 |
| 100 | 165.1 | 28.7 | 10.9 | 0 |
| 500 | 4261.8 | 147.3 | 60.6 | 0 |
| 2000 | 72570.1 | 674.2 | 290.8 | 2 |

**Nhận xét:** Tại n nhỏ (5, 20) ba thuật toán gần bằng nhau do overhead của sort
và độ phân giải thời gian nhỏ (số liệu có thể dao động giữa các lần chạy). Khi n
tăng, O(n²) tăng rất nhanh: n=2000 chậm khoảng 108 lần so với sort+tìm nhị phân
(72570.1/674.2 ≈ 108) và 250 lần so với hai con trỏ (72570.1/290.8 ≈ 250). Hai
thuật toán O(n log n) cho tốc độ gần nhau, hai con trỏ nhỉnh hơn vì sau sort chỉ
duyệt tuyến tính O(n). (Số liệu đo trên máy sinh viên, Python 3.14.7, trùng với
ảnh minh chứng A06.)

### 4.4 GitHub và clone chạy lại
- Commit C (mã/test/input): lấy từ lệnh `git rev-parse HEAD` sau khi push lên GitHub.
- Sau khi chụp đủ 11 ảnh và hoàn thiện báo cáo, tạo commit S.
- Clone chạy lại: `git clone <URL> kiem_tra_DT009 && cd kiem_tra_DT009 &&
  python demo.py && python test/runtests.py`.

### 4.5 11 ảnh minh chứng cần chụp (A01–A11)
Lưu vào `docs/anh_ket_qua/`, mỗi ảnh có mã ca, input, lệnh chạy, output và chú thích.
*Lưu ý: ID ảnh minh chứng (A01–A11) và ID ca kiểm thử trong bảng 4.2 (A01–A16) là hai hệ đánh số riêng, không trùng nghĩa.*
- A01: Chạy Ví dụ 1 (`python demo.py` phần VI DU 1) — [1,2,2,3], X=4 → 2 cặp.
- A02: Chạy Ví dụ 2 — [2,2,2], X=4 → 3 cặp.
- A03: Chạy ca kiểm 3 — [1,4], X=8 → 0 cặp.
- A04: Chạy ca kiểm 4 — [-2,0,2], X=0 → 1 cặp.
- A05: Chạy ca kiểm 5a + 5b — mảng rỗng `[]` và 1 phần tử `[7]` → 0 cặp.
- A06: Bảng đo thời gian 3 thuật toán ở 5 quy mô (n=5, 20, 100, 500, 2000).
- A07: Bảng truy vết tay (lần vết) của thuật toán O(n²) trên Ví dụ 1 (`python scripts/trace_scales.py`).
- A08: 3 ca input sai và phản hồi validator (A12, A13, A14 trong bộ kiểm thử).
- A09: Chạy toàn bộ bộ kiểm thử (`python test/runtests.py`) — tổng kết 23/23 PASS.
- A10: Clone repo sang thư mục mới, kiểm SHA C, chạy lại demo + bộ kiểm thử.
- A11: Trang GitHub repo thật, hiển thị commit C và permalink file `src/DeTai.py`.

---

## CHƯƠNG 5: KẾT LUẬN

### 5.1 Mức hoàn thành
- Hoàn thành đầy đủ 5 bước theo phiếu: đọc lý thuyết, giải tay ví dụ, cài 3 hàm
  gợi ý + yêu cầu thêm (hai con trỏ), chạy đủ 2 ví dụ + 5 ca bắt buộc, phân tích
  độ phức tạp.
- Bộ kiểm thử: **23 ca độc lập PASS** (vượt yêu cầu tối thiểu 12 ca), gồm ca ví dụ,
  ca tự thiết kế, ca biên, ca input sai (validator) và ca đối chứng bất biến.
- Đo thời gian 3 thuật toán ở 5 quy mô (5, 20, 100, 500, 2000), khẳng định O(n²)
  chậm rõ rệt khi n lớn.
- Có git local commit C với SHA rõ ràng; sẵn sàng push GitHub.

### 5.2 Hạn chế
- Thuật toán O(n²) chỉ phù hợp n nhỏ (n ≤ 2000 theo miền phiếu là chấp nhận được
  nhưng chậm).
- Chưa cài đặt phương pháp dùng băm (hash map) O(n) — có thể mở rộng trong tương lai.
- Chưa có giao diện đồ họa; input chủ yếu khai báo trực tiếp.

### 5.3 Hướng phát triển
- Cài thêm thuật toán dùng dictionary (hash map) đếm tần suất, đạt O(n) thời gian.
- Mở rộng miền n lớn hơn (ví dụ n ≤ 10⁶) để thấy rõ ưu thế của O(n) và O(n log n).
- Thêm chức năng xuất các cặp chỉ số ra file cho n lớn.

---

## PHỤ LỤC: MÃ NGUỒN
Xem file `src/DeTai.py`, `test/runtests.py`, `demo.py`, `scripts/trace_scales.py`
trong thư mục mã nguồn. Toàn bộ mã nguồn được đính kèm trong ZIP nộp bài.
