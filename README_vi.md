# Deckmaker — Hướng dẫn từng bước cho người mới bắt đầu

[🇬🇧 English](README.md)

> **Lưu ý:** Tài liệu này đã được AI cập nhật bổ sung liên kết chuyển đổi ngôn ngữ, hướng dẫn tính năng kéo-thả (drag-and-drop) file CSV bất kỳ, và đồng bộ nội dung với bản tiếng Anh.

## Chương trình này làm gì?

Bạn có một danh sách từ vựng IELTS trong Google Sheets. Chương trình này sẽ
biến danh sách đó thành **bộ thẻ Anki** để bạn ôn tập, bao gồm:

1. **Thẻ từ vựng** — mặt trước hiện từ tiếng Anh + nút nghe phát âm, mặt sau
   hiện nghĩa tiếng Việt và câu ví dụ.
2. **Thẻ trắc nghiệm** — câu ví dụ khuyết từ, bạn chọn đáp án đúng trong 4 lựa
   chọn. Mặt sau tô xanh/đỏ và cho biết bạn chọn đúng hay sai.

Tất cả chỉ cần **3 bước** bên dưới.

---

## Bước 1: Tải file CSV từ Google Sheets

File CSV là file dữ liệu chứa danh sách từ vựng của bạn. Bạn sẽ tải nó về từ
Google Sheets.

1. Mở Google Sheets chứa danh sách từ vựng của bạn.
2. Vào menu **File → Download → Comma Separated Values (.csv)**.
3. File sẽ được tải về máy (thường nằm trong thư mục **Downloads**).

> ⚠️ **Quan trọng:** File CSV của bạn phải có **đúng 6 cột** với tên như sau
> (hàng đầu tiên là tiêu đề, viết đúng chính tả và dấu):
>
> | Từ  | Phát âm | Loại từ | Ý nghĩa | Ví dụ | Ghi chú |
> | --- | ------- | ------- | ------- | ----- | ------- |

---

## Bước 2: Chuẩn bị file CSV

Bạn **không cần phải đổi tên file** thành `vocab.csv` nữa. Chương trình có thể đọc bất kỳ file CSV nào có đủ 6 cột tiêu đề ở Bước 1.

File `.apkg` kết quả sẽ được tạo ra ngay tại thư mục chứa file CSV của bạn (ví dụ: `IELTS_Vocab.csv` sẽ tạo ra `IELTS_Vocab.apkg`).

---

## Bước 3: Chạy chương trình

### Cách 1 (Dễ nhất): Kéo và thả file CSV vào deckmaker.exe

1. Mở thư mục chứa file CSV bạn vừa tải về và thư mục chứa **`deckmaker.exe`**.
2. **Kéo file CSV thả thẳng vào file `deckmaker.exe`**.
3. Cửa sổ dòng lệnh sẽ hiện ra và xử lý. Khi xong, bạn sẽ thấy thông báo:
   **`✅ [Tên-file].apkg`**.
4. Nhấn Enter để đóng cửa sổ nếu có lời nhắc.

### Cách 2: Nhấp đúp chuột

1. Nếu bạn để file có tên `vocab.csv` cùng thư mục với `deckmaker.exe`: chỉ cần **nhấp đúp** vào `deckmaker.exe`.
2. Nếu không tìm thấy file `vocab.csv`, chương trình sẽ hỏi bạn: bạn chỉ cần **kéo file CSV thả vào cửa sổ màn hình đen** rồi nhấn Enter.


> ℹ️ Lần đầu chạy, Windows có thể hiện cảnh báo "Windows protected your PC".
> Nhấn **More info** (Thông tin thêm) rồi **Run anyway** (Vẫn chạy).

### Cách 3: Chạy bằng dòng lệnh (Terminal / Python)

Nếu bạn là lập trình viên hoặc muốn chạy từ terminal:

```bash
# Chạy với file vocab.csv mặc định (hoặc nhập đường dẫn nếu chưa có)
python deckmaker.py

# Chạy với file CSV cụ thể
python deckmaker.py duong/dan/tu_vung.csv

# Bỏ qua tạo file phát âm (nếu file audio đã có sẵn)
python deckmaker.py duong/dan/tu_vung.csv --no-audio
```

Với file `.exe` trên Windows:

```powershell
.\dist\deckmaker.exe [duong\dan\tu_vung.csv] [--no-audio]
```

---

## ⚠️ Cần làm trước khi import: Cài Add-on cho thẻ trắc nghiệm

Để thẻ trắc nghiệm hiển thị đúng (tô màu xanh/đỏ, hiện đúng/sai), bạn **phải**
cài add-on này trong Anki **trước khi import**:

1. Mở Anki, vào **Tools → Add-ons** (Công cụ → Tiện ích).
2. Nhấn **Get Add-ons…** (Tải tiện ích…).
3. Nhập mã: **`1566095810`**
4. Nhấn OK, sau đó **khởi động lại Anki**.

> Nếu quên cài add-on này, thẻ trắc nghiệm sẽ không hoạt động. Bạn vẫn có thể
> cài add-on sau đó, nhưng cần import lại file `.apkg`.

---

## Bước 4: Import vào Anki

Sau khi chạy xong, trong thư mục chứa file CSV sẽ có file **`<tên-file>.apkg`** (ví dụ: `vocab.apkg`). Đây chính là bộ thẻ của bạn.

1. Mở **Anki**.
2. Vào menu **File → Import…** (Tệp → Nhập…).
3. Chọn file `<tên-file>.apkg`.
4. Nhấn **Import** (Nhập).
5. Một cửa sổ nhỏ hiện ra báo đã import thành công — **nhấn Close** (Đóng) để
   tắt nó đi.
6. Bộ thẻ "IELTS Vocabulary" giờ đã xuất hiện ở màn hình chính của Anki.

### Cách học bộ thẻ

Sau khi import xong, đây là cách bạn bắt đầu ôn tập:

1. Ở màn hình chính của Anki, bạn sẽ thấy một mục tên là **"IELTS Vocabulary"**.
2. **Nhấp chuột** vào tên đó để chọn nó (nó sẽ được tô sáng lên).
3. Nhấn nút **Study Now** (Học ngay) ở phía trên.
4. Thẻ đầu tiên sẽ hiện ra — bạn xem câu hỏi, cố gắng nhớ đáp án, rồi nhấn
   **Show Answer** (Hiện đáp án) để xem mặt sau.
5. Ở mặt sau, bạn tự đánh giá mức độ nhớ của mình bằng cách nhấn một trong các nút:
   - **Again** (Lại) — chưa nhớ được, thẻ này sẽ hỏi lại sớm.
   - **Hard** (Khó) — có nhớ nhưng hơi vất vả.
   - **Good** (Tốt) — nhớ được bình thường.
   - **Easy** (Dễ) — quá dễ, không cần hỏi lại sớm.
6. Tiếp tục với các thẻ tiếp theo cho đến khi hết. Mỗi ngày Anki sẽ tự động đưa
   ra những thẻ đến hạn ôn tập cho bạn — bạn chỉ cần mở Anki lên và nhấn
   **Study Now** là được.

---

## Kết quả sau khi chạy

| File / Thư mục      | Là gì?                                                            |
| ------------------- | ----------------------------------------------------------------- |
| `<tên-file>.apkg`   | Bộ thẻ Anki kết quả — **file bạn cần import vào Anki**            |
| `audio/`            | Thư mục lưu trữ các file phát âm mp3 (dùng chung giữa các lần)   |

---

## Xử lý sự cố

| Vấn đề | Cách khắc phục |
| ------ | -------------- |
| "CSV file is missing required headers" | Kiểm tra hàng đầu tiên của CSV, phải có đủ: `Từ, Phát âm, Loại từ, Ý nghĩa, Ví dụ, Ghi chú`. |
| "File not found" | Kiểm tra lại đường dẫn file hoặc kéo thả file CSV trực tiếp vào `deckmaker.exe` / terminal. |
| File CSV bị lỗi font / chữ lạ | Mở file CSV bằng Notepad hoặc VS Code, chọn **Save As → UTF-8 with BOM**, lưu lại. |
| Không có âm thanh / lỗi tải audio | Cần kết nối Internet để `gTTS` tải phát âm cho các từ mới. |
| Thẻ trắc nghiệm không hiển thị đúng | Chưa cài add-on `1566095810`. Vào Anki cài tiện ích rồi khởi động lại trước khi import. |
| Windows SmartScreen chặn file .exe | Nhấn **More info → Run anyway** (Thông tin thêm → Vẫn chạy). |

---

## Cập nhật danh sách từ vựng

Chương trình gán mã định danh cố định (stable ID) cho từng thẻ, do đó việc import lại là **hoàn toàn an toàn: tiến độ học của các từ cũ được giữ nguyên, chỉ có từ mới được bổ sung vào.**

1. Mở Google Sheets, thêm hoặc sửa từ vựng rồi tải file `.csv` mới về máy.
2. Kéo file CSV mới thả vào `deckmaker.exe` (hoặc chạy lại qua dòng lệnh).
3. Mở Anki, chọn **File → Import** file `.apkg` mới tạo — Anki sẽ tự động sáp nhập thẻ mới vào bộ thẻ hiện có mà không làm mất lịch sử học.

> **Lưu ý chuyển đổi một lần:** Các bản deck tạo *trước* khi có tính năng stable ID sẽ dùng ID ngẫu nhiên và có thể bị nhân đôi trong lần import đầu tiên. Để có bộ thẻ sạch, hãy xóa bộ thẻ "IELTS Vocabulary" cũ trong Anki một lần rồi import lại. Các lần sau sẽ cập nhật lũy tiến bình thường.

---

## Ghi chú thêm

- Chương trình dùng **Google Text-to-Speech (gTTS)** để đọc từ — cần có mạng khi tạo audio.
- Mỗi lần chạy, chỉ tải audio cho **từ mới**, từ đã có trong thư mục `audio/` sẽ được tái sử dụng.
- File `<tên-file>.apkg` sẽ được ghi đè/cập nhật tương ứng mỗi lần chạy với file CSV đó.
