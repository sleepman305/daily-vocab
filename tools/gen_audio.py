"""Tạo sẵn âm thanh giọng AI tự nhiên cho Daily vocab.

Dùng mô hình Kokoro-82M (giấy phép Apache-2.0) chạy trên máy qua kokoro-onnx;
tiếng Trung chuyển chữ Hán → âm vị bằng misaki[zh] (espeak đọc sai chữ Hán).
Âm thanh sinh ra được phát hành cùng app, không phụ thuộc dịch vụ trả phí.

Phạm vi (cân đối chất lượng và dung lượng tải về điện thoại):
- Tiếng Anh, 4 giọng: từ cấp Cơ bản (en-1) + thuật ngữ Hải quan (en-5),
  kèm câu ví dụ của mục Hải quan.
- Tiếng Trung, 2 giọng: HSK 1–3.
Từ ngoài phạm vi thì app tự dùng giọng của máy.

Tên tệp: ``audio/<giọng>/<fnv1a32(chuỗi)>.mp3`` — app tính cùng hàm băm
FNV-1a 32 bit trên UTF-8 (xem ``audioKey`` trong app.js). Chạy lại thì bỏ qua
tệp đã có, nên dừng giữa chừng vẫn chạy tiếp được.

Cách chạy::

    pip install kokoro-onnx soundfile "misaki[zh]"
    python tools/gen_audio.py <thư mục chứa kokoro-v1.0.onnx và voices-v1.0.bin> [số tiến trình]

Lỗi có thể gặp: FileNotFoundError nếu thiếu tệp mô hình.
"""
import json
import sys
from multiprocessing import Pool
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
AUDIO = ROOT / "audio"
EN_VOICES = {"af_heart": "en-us", "am_michael": "en-us", "bf_emma": "en-gb", "bm_george": "en-gb"}
ZH_VOICES = ["zf_xiaoxiao", "zm_yunxi"]


def fnv1a(text: str) -> str:
    """Băm FNV-1a 32 bit của chuỗi UTF-8, trả 8 ký tự hex (khớp audioKey trong app.js)."""
    h = 0x811C9DC5
    for b in text.encode("utf-8"):
        h ^= b
        h = (h * 0x01000193) & 0xFFFFFFFF
    return f"{h:08x}"


def jobs() -> list:
    """Liệt kê (giọng, ngôn ngữ, chuỗi, tốc độ) cần tạo, bỏ qua tệp đã có."""
    load = lambda n: json.loads((ROOT / "data" / f"{n}.json").read_text(encoding="utf-8"))
    hq_words = [r[0] for r in load("en-5")]
    hq_sent = [r[4] for r in load("en-5") if r[4]]
    zh_words = [r[0] for r in load("zh") if r[4] <= 3]
    basic = [r[0] for r in load("en-1")]
    # Thứ tự ưu tiên (chạy dở vẫn dùng được): Hải quan → HSK 1–3 → từ Cơ bản.
    out = []
    for group, speed in ((hq_words, 0.9), (hq_sent, 0.95)):
        for v, lang in EN_VOICES.items():
            out += [(v, lang, t, speed) for t in dict.fromkeys(group)]
    for v in ZH_VOICES:
        out += [(v, "zh", t, 0.9) for t in dict.fromkeys(zh_words)]
    for v, lang in EN_VOICES.items():
        out += [(v, lang, t, 0.9) for t in dict.fromkeys(basic)]
    return [j for j in out if not (AUDIO / j[0] / f"{fnv1a(j[2])}.mp3").exists()]


_k = None
_g2p = None


def _init(model_dir):
    """Mỗi tiến trình nạp một bản mô hình, giới hạn 4 luồng để chạy song song nhiều tiến trình."""
    global _k, _g2p
    import onnxruntime as ort
    from kokoro_onnx import Kokoro
    opt = ort.SessionOptions()
    opt.intra_op_num_threads = 4
    opt.inter_op_num_threads = 1
    sess = ort.InferenceSession(str(Path(model_dir) / "kokoro-v1.0.onnx"), opt, providers=["CPUExecutionProvider"])
    _k = Kokoro.from_session(sess, str(Path(model_dir) / "voices-v1.0.bin"))
    from misaki import zh
    _g2p = zh.ZHG2P()


def trim(a: np.ndarray, sr: int) -> np.ndarray:
    """Cắt khoảng lặng hai đầu (giữ 60 ms đệm) và chuẩn hoá đỉnh về -1 dBFS."""
    idx = np.where(np.abs(a) > 0.01)[0]
    if len(idx):
        pad = int(0.06 * sr)
        a = a[max(0, idx[0] - pad): idx[-1] + pad]
    peak = np.max(np.abs(a)) or 1
    return (a / peak * 0.89).astype(np.float32)


def work(job):
    import soundfile as sf
    voice, lang, text, speed = job
    try:
        if lang == "zh":
            ph = _g2p(text)
            ph = ph[0] if isinstance(ph, tuple) else ph
            a, sr = _k.create(ph, voice=voice, speed=speed, is_phonemes=True)
        else:
            a, sr = _k.create(text, voice=voice, speed=speed, lang=lang)
        out = AUDIO / voice / f"{fnv1a(text)}.mp3"
        out.parent.mkdir(parents=True, exist_ok=True)
        # 24 kHz mono, mức nén 0.7 ≈ 40 kbps: đủ rõ cho giọng nói, ~3 KB mỗi từ.
        sf.write(str(out), trim(a, sr), sr, format="MP3", subtype="MPEG_LAYER_III", compression_level=0.7)
        return None
    except Exception as e:  # ghi lại để chạy bù, không làm hỏng cả lượt
        return f"{voice}\t{text}\t{e}"


def main():
    model_dir = sys.argv[1]
    procs = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    todo = jobs()
    print(f"cần tạo {len(todo)} tệp", flush=True)
    errors = []
    with Pool(procs, initializer=_init, initargs=(model_dir,)) as pool:
        for i, err in enumerate(pool.imap_unordered(work, todo, chunksize=8), 1):
            if err:
                errors.append(err)
            if i % 500 == 0:
                print(f"{i}/{len(todo)}", flush=True)
    print(f"xong, lỗi {len(errors)}")
    for e in errors[:20]:
        print(e)


if __name__ == "__main__":
    main()
