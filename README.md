# Daily vocab by SirV

App học từ vựng **Anh–Việt** và **Trung–Việt (HSK 1–9)** mỗi ngày, chạy trên điện thoại như một ứng dụng (PWA), dùng được cả khi không có mạng.

**Mở app:** https://sleepman305.github.io/daily-vocab/

## Tính năng
- Đoán từ qua nghĩa tiếng Việt: ô chữ gợi ý, đếm giờ, gõ đáp án (tiếng Trung nhận pinyin có/không dấu hoặc chữ Hán).
- Lặp lại ngắt quãng (hộp Leitner): "Chưa nhớ" ôn lại ngay trong lượt, "Đã nhớ" giãn lịch 1 → 3 → 7 → 14 → 30… ngày.
- 85.523 từ tiếng Anh xếp 4 cấp theo tần suất thực tế; 11.384 từ HSK 3.0 kèm pinyin và nghĩa tiếng Việt, **có sẵn trong app, không cần máy dịch**.
- Kho từ tìm không dấu, mục tiêu mỗi ngày, chuỗi ngày học, biểu đồ 7 ngày, sao lưu/khôi phục tiến độ.
- **Tiếng Anh chuyên ngành Hải quan**: 308 thuật ngữ / 12 chủ đề (thủ tục, trị giá, phân loại HS, xuất xứ, KTSTQ, chống buôn lậu, Incoterms…), mỗi từ có câu ví dụ và bản dịch. Thuật ngữ theo WCO Glossary of International Customs Terms; nghĩa tiếng Việt theo Luật Hải quan 54/2014 và văn bản hướng dẫn.
- Giọng AI tự nhiên (Kokoro-82M, Apache-2.0) 4 giọng Anh + 2 giọng Trung, tạo sẵn cho từ Cơ bản, mục Hải quan và HSK 1–3; có thể chọn cả giọng có sẵn trên máy.
- Trả lời bằng micro, tự chuyển từ, chủ đề sáng/tối.

## Cài lên điện thoại
- iPhone: mở link bằng **Safari** → nút Chia sẻ → **Thêm vào MH chính**.
- Android: Chrome → menu ⋮ → **Cài đặt ứng dụng**.

## Dựng lại dữ liệu
```
pip install wordfreq kokoro-onnx soundfile "misaki[zh]"
python tools/build_data.py <Tu_vung_moi_ngay_100000.html> <complete.min.json> <CVDICT.u8>
python tools/gen_audio.py <thư mục chứa kokoro-v1.0.onnx, voices-v1.0.bin> [số tiến trình]
```

## Giấy phép
- Mã nguồn: MIT.
- Dữ liệu trong `data/` là bản phái sinh, phát hành theo **CC BY-SA 4.0**:
  - Từ điển Anh–Việt thichhoc.com (thichhoc-dict), CC BY-SA 4.0 — nguồn gốc WordNet 3.1 (Princeton), CMUdict (CMU), Wiktionary. WordNet 3.1 Copyright 2011 The Trustees of Princeton University. All rights reserved.
  - CVDICT của Phong Phan (CC BY-SA 4.0), chuyển dịch từ CC-CEDICT.
  - complete-hsk-vocabulary của Yanis Zafirópulos (MIT).
  - Xếp cấp theo tần suất từ wordfreq (MIT).
  - Âm thanh giọng AI tạo bằng mô hình Kokoro-82M (hexgrad, Apache-2.0).
  - Đã chỉnh sửa dữ liệu: chọn nghĩa, bỏ mục tham chiếu/biến thể ngữ pháp, ghép nghĩa tiếng Việt cho từ HSK, xếp cấp.
