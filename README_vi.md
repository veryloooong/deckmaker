# Deckmaker — Hướng dẫn sử dụng

## Chương trình này làm gì?

Từ một file `vocab.csv` chứa danh sách từ vựng, chương trình sẽ tự động tạo ra
bộ thẻ Anki (file `.apkg`) gồm **hai loại thẻ** để bạn ôn tập:

1. **Thẻ từ vựng cơ bản** — Mặt trước hiển thị từ tiếng Anh kèm nút phát âm.
   Mặt sau hiển thị nghĩa tiếng Việt và câu ví dụ.

2. **Thẻ trắc nghiệm (MCQ)** — Một câu ví dụ bị khuyết từ, bạn chọn từ đúng
   trong 4 đáp án. Mặt sau tô màu xanh (đúng) / đỏ (sai) và hiển thị đáp án.

## Yêu cầu Add-on Anki (quan trọng — làm trước khi import)

Để thẻ trắc nghiệm hoạt động đúng, bạn **cần cài addon** sau trong Anki:

1. Mở Anki, vào **Tools → Add-ons** (Công cụ → Tiện ích)
2. Nhấn **Get Add-ons…** (Tải tiện ích…)
3. Nhập mã: **`1566095810`**
4. Nhấn OK, sau đó **khởi động lại Anki**

## Yêu cầu

- **File `vocab.csv`** đặt cùng thư mục với `deckmaker.exe`
- File CSV phải có **đúng 6 cột** với tên như sau (hàng đầu tiên là tiêu đề):

  | Từ  | Phát âm | Loại từ | Ý nghĩa | Ví dụ | Ghi chú |
  | --- | ------- | ------- | ------- | ----- | ------- |

  > 💡 Mở file CSV mẫu bằng Excel hoặc Notepad để xem cấu trúc.
  > Lưu ý: file phải được lưu với encoding **UTF-8**.

- **Anki** đã được cài đặt trên máy tính.

## Cách chạy

### Cách 1: Nhấp đúp chuột

Nhấp đúp vào `deckmaker.exe`. Một cửa sổ dòng lệnh sẽ hiện ra, hiển thị tiến
trình tạo thẻ. Khi thấy dòng `✅ ielts_vocab.apkg` là xong.

### Cách 2: Chạy từ Command Prompt / PowerShell

Mở Command Prompt hoặc PowerShell trong thư mục chứa chương trình, gõ:

```cmd
deckmaker.exe
```

Nếu bạn đã có sẵn file âm thanh trong thư mục `audio\` và không muốn tải lại, dùng:

```cmd
deckmaker.exe --no-audio
```

## Kết quả

Sau khi chạy xong, trong thư mục sẽ có:

| File / Thư mục     | Mô tả                                        |
| ------------------ | -------------------------------------------- |
| `ielts_vocab.apkg` | Bộ thẻ Anki — **đây là file bạn cần import** |
| `audio\`           | Thư mục chứa file âm thanh phát âm từng từ   |

## Import vào Anki

1. Mở **Anki**
2. Vào menu **File → Import…** (hoặc Tệp → Nhập…)
3. Chọn file `ielts_vocab.apkg`
4. Nhấn **Import** (hoặc Nhập)
5. Xong! Bộ thẻ "IELTS Vocabulary" sẽ xuất hiện trong danh sách deck của bạn

## Hai loại thẻ trong bộ deck

### 1. Thẻ Từ → Nghĩa

- **Mặt trước:** từ tiếng Anh (chữ to), phiên âm IPA, loại từ, và nút ▶ để
  nghe phát âm
- **Mặt sau:** nghĩa tiếng Việt, câu ví dụ, ghi chú (nếu có)

### 2. Thẻ Trắc nghiệm (MCQ)

- **Mặt trước:** câu ví dụ bị khuyết từ, bên dưới là 4 lựa chọn (radio button).
  Chọn một đáp án rồi nhấn **Show Answer**.
- **Mặt sau:**
  - Bảng lựa chọn của bạn được tô màu: 🟢 xanh = đúng, 🔴 đỏ = sai
  - Bảng đáp án đúng bên dưới
  - Hiển thị "Correct!" nếu bạn chọn đúng, hoặc "Nope." nếu sai
  - Nghĩa tiếng Việt và câu đầy đủ

## Xử lý sự cố

| Vấn đề                              | Cách khắc phục                                                      |
| ----------------------------------- | ------------------------------------------------------------------- |
| "File not found: vocab.csv"         | Đảm bảo file `vocab.csv` nằm **cùng thư mục** với `deckmaker.exe`   |
| File CSV bị lỗi font/chữ            | Mở file CSV bằng Notepad, chọn **Save As → UTF-8**                  |
| Thẻ trắc nghiệm không hiển thị đúng | Kiểm tra đã cài addon `1566095810` và khởi động lại Anki chưa       |
| Không có âm thanh phát âm           | Đảm bảo máy tính có kết nối Internet khi chạy chương trình          |
| Chương trình báo lỗi âm thanh       | Chạy lại với `--no-audio`, thẻ vẫn dùng được chỉ thiếu phần phát âm |
| Windows SmartScreen chặn file .exe  | Nhấn **More info → Run anyway** (Thông tin thêm → Vẫn chạy)         |

## Thông tin thêm

- Chương trình sử dụng công nghệ **Google Text-to-Speech** để tạo giọng đọc —
  cần kết nối Internet khi tạo audio.
- Mỗi lần chạy, chương trình chỉ tải audio cho những từ chưa có — các từ đã có
  sẽ được bỏ qua.
- File `ielts_vocab.apkg` sẽ bị **ghi đè** mỗi lần chạy.
- Muốn thêm/sửa từ vựng: chỉnh sửa file `vocab.csv` rồi chạy lại chương trình.
