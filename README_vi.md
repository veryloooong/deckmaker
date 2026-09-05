# Deckmaker — Hướng dẫn từng bước cho người mới bắt đầu

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

## Bước 2: Đổi tên file và đặt vào thư mục

Sau khi tải về, file của bạn sẽ có tên giống tên Google Sheets (ví dụ:
`Kế hoạch ôn thi IELTS - Từ vựng.csv`). Bạn cần đổi tên nó thành `vocab.csv`
và đặt cùng chỗ với chương trình.

1. Mở thư mục **Downloads** (hoặc nơi bạn vừa tải file về).
2. Tìm file CSV vừa tải, **nhấp chuột phải → Rename** (Đổi tên).
3. Gõ đúng tên: **`vocab.csv`**
4. **Copy** file `vocab.csv` đó vào thư mục chứa `deckmaker.exe`.
   - Nếu bạn chưa giải nén: giải nén file `.zip` bạn nhận được ra một thư mục,
     sau đó dán file `vocab.csv` vào thư mục đó.

> 💡 **Mẹo:** Sau khi copy vào, mở thư mục đó lên bạn sẽ thấy `deckmaker.exe`
> và `vocab.csv` nằm cạnh nhau — như vậy là đúng.

---

## Bước 3: Chạy chương trình

### Cách đơn giản nhất: Nhấp đúp chuột

1. Nhấp đúp vào file **`deckmaker.exe`**.
2. Một cửa sổ màu đen (dòng lệnh) sẽ hiện ra, chạy khoảng 1-2 phút.
3. Khi thấy dòng **`✅ vocab.apkg`** là xong! Cửa sổ sẽ tự đóng.

> ℹ️ Lần đầu chạy, Windows có thể hiện cảnh báo "Windows protected your PC".
> Nhấn **More info** (Thông tin thêm) rồi **Run anyway** (Vẫn chạy).

### Nếu muốn chạy lại (đã có sẵn âm thanh)

Khi chạy lại lần sau, nếu bạn không muốn tải lại file phát âm (đỡ tốn thời gian):

1. Mở thư mục chứa `deckmaker.exe`.
2. Gõ **`cmd`** vào thanh địa chỉ của File Explorer, nhấn Enter.
3. Trong cửa sổ đen hiện ra, gõ:
   ```
   deckmaker.exe --no-audio
   ```
4. Nhấn Enter.

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

Sau khi chạy xong, trong thư mục sẽ có file **`vocab.apkg`**. Đây chính là bộ
thẻ của bạn.

1. Mở **Anki**.
2. Vào menu **File → Import…** (Tệp → Nhập…).
3. Chọn file `vocab.apkg`.
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

| File / Thư mục    | Là gì?                                       |
| ----------------- | -------------------------------------------- |
| `vocab.apkg`      | Bộ thẻ Anki — **file bạn cần import**        |
| `audio\`          | Thư mục chứa file âm thanh phát âm từng từ   |

---

## Xử lý sự cố

| Vấn đề                              | Cách khắc phục                                                      |
| ----------------------------------- | ------------------------------------------------------------------- |
| "File not found: vocab.csv"         | File `vocab.csv` chưa nằm cùng thư mục với `deckmaker.exe`. Copy nó vào. |
| File CSV bị lỗi font / chữ lạ       | Mở file CSV bằng Notepad, chọn **File → Save As → UTF-8**, lưu lại. |
| Không có âm thanh                   | Máy cần có Internet khi chạy chương trình.                          |
| Thẻ trắc nghiệm không hiển thị đúng | Chưa cài add-on `1566095810`. Vào Anki cài rồi import lại.         |
| Windows SmartScreen chặn file .exe  | Nhấn **More info → Run anyway**.                                    |

---

## Cập nhật danh sách từ vựng

Khi bạn thêm từ mới hoặc sửa từ cũ trong Google Sheets, bạn cần làm lại bộ thẻ
để những thay đổi đó xuất hiện trong Anki. Các bước làm:

1. Mở Google Sheets, thêm/sửa từ xong thì vào **File → Download → Comma
   Separated Values (.csv)** để tải file mới về.
2. **Đổi tên** file vừa tải thành `vocab.csv`.
3. Copy file `vocab.csv` mới vào thư mục chứa `deckmaker.exe`, **ghi đè** lên
   file cũ.
4. Chạy lại chương trình (nhấp đúp `deckmaker.exe`).
5. Vào Anki, import lại file `vocab.apkg` mới (giống hệt Bước 4 ở trên).
   Những từ đã học sẽ được giữ nguyên, chỉ có từ mới được thêm vào.

> 💡 Nếu bạn chỉ muốn thêm từ mà không muốn tải lại toàn bộ audio, dùng
> `--no-audio` như hướng dẫn ở Bước 3. Audio của từ cũ vẫn giữ nguyên, chỉ
> thiếu phát âm cho từ mới thêm.

---

## Ghi chú thêm

- Chương trình dùng **Google Text-to-Speech** để đọc từ — cần có mạng khi tạo audio.
- Mỗi lần chạy, chỉ tải audio cho **từ mới**, từ đã có thì bỏ qua.
- File `vocab.apkg` sẽ bị **ghi đè** mỗi lần chạy.
