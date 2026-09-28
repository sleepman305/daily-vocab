"""Dựng bộ dữ liệu cho app Daily vocab by SirV.

Đọc dữ liệu gốc (bản HTML 100.000 mục cũ, danh sách HSK, từ điển CVDICT) và
xuất ra hai tệp gọn cho app đọc offline:

- ``data/en-1.json`` … ``en-4.json``: kho Anh–Việt tách theo cấp, mỗi mục là mảng
  ``[en, vi, pos, ipa, ex, level, topic]``.
- ``data/zh.json``: kho Trung–Việt theo HSK, mỗi mục là mảng
  ``[hanzi, pinyin, vi, en, level, pos]``.

Căn cứ các quyết định làm sạch:

- Bỏ mục chỉ là tham chiếu hoặc biến thể ngữ pháp ("Xem damn", "Số nhiều của
  foot", "Quá khứ và phân từ quá khứ của …", "Động từ chia ở ngôi thứ ba …",
  "Dạng phân từ …", "Cách viết khác : …") — đây là lỗi hiển thị "Xem exotic"
  trong ảnh chụp màn hình người dùng gửi ngày 28/9/2026: câu hỏi không có nghĩa
  thật để đoán.
- Cấp độ Anh–Việt tính theo tần suất Zipf của thư viện ``wordfreq``
  (thang 0–8, từ xuất hiện 1 lần/1 tỷ từ ≈ 1): ≥4,5 Cơ bản; ≥3,5 Thông dụng;
  ≥2,5 Nâng cao; còn lại Chuyên sâu. Thay cho cách cũ đoán độ khó theo độ dài
  chữ, vốn xếp "shemmas" ngang "fulfill".
- Cấp HSK lấy theo chuẩn HSK 3.0 (2021, 9 bậc; bậc 7–9 gộp làm "7") trong
  complete-hsk-vocabulary (khoá ``n``); thiếu thì dùng HSK 2.0 (khoá ``o``).
- Nghĩa tiếng Việt của từ tiếng Trung lấy từ CVDICT (CC BY-SA 4.0), khớp theo
  chữ giản thể + pinyin số; không dùng máy dịch lúc chạy vì cách cũ gọi Google
  Dịch khi mở đáp án nên mất mạng là hiện "Chưa lấy được chữ Hán".

Cách chạy::

    python tools/build_data.py <file_html_goc> <complete.min.json> <CVDICT.u8>

Lỗi có thể gặp: FileNotFoundError khi thiếu tệp nguồn; ImportError nếu chưa
``pip install wordfreq``.
"""
import json
import re
import sys
from pathlib import Path

from wordfreq import zipf_frequency

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data"

# Mục chỉ là tham chiếu/biến thể ngữ pháp, không có nghĩa riêng để học.
JUNK = re.compile(
    r"^(xem\s+[\w\-' ]+\.?$|số nhiều\.?$|số nhiều của|(dạng |động từ |đồng từ )?quá khứ (đơn|và|hoàn thành|của)|"
    r"(hiện tại )?phân từ( quá khứ| hiện tại)? của|động từ chia|dạng (phân từ|so sánh|khác của)|so sánh (hơn|nhất)|"
    r"cách viết khác|trạng từ\.?$|từ đồng nghĩa của|english word|một tên dành)",
    re.I,
)
POS_MAP = {"noun": "danh từ", "tính từ / danh từ": "tính từ"}
POS_OK = {"danh từ", "tính từ", "động từ", "trạng từ", "cụm từ"}
# Nhóm "… mở rộng" chỉ là nhãn từ loại, không phải chủ đề — gộp về "chung".
NOT_TOPIC = re.compile(r"mở rộng$")


def level_en(word: str, curated: bool) -> int:
    """Xếp cấp 1–4 theo tần suất Zipf (wordfreq).

    wordfreq ước tần suất cụm theo từng mảnh, nên "be in", "have in" bị xếp
    ngang "be"; vì vậy cụm bị trừ điểm: trừ 1 nếu thuộc nhóm chủ đề đã biên soạn
    tay (curated, vd "make sure"), trừ 2,5 nếu chỉ đến từ từ điển mở rộng.
    Tiền tố/hậu tố ("a-", "-ness") luôn xếp Chuyên sâu.

    Args:
        word: từ hoặc cụm từ tiếng Anh.
        curated: True nếu mục thuộc một nhóm chủ đề trong bản gốc.
    Returns:
        1 Cơ bản, 2 Thông dụng, 3 Nâng cao, 4 Chuyên sâu.
    """
    if word.startswith("-") or word.endswith("-"):
        return 4
    z = zipf_frequency(word, "en")
    if re.search(r"[\s\-]", word):
        z -= 1 if curated else 2.5
    return 1 if z >= 4.5 else 2 if z >= 3.5 else 3 if z >= 2.5 else 4


def clean_vi(s: str) -> str:
    """Bỏ khoảng trắng thừa và dấu chấm cuối cho nghĩa tiếng Việt gọn khi hiển thị."""
    s = re.sub(r"\s+", " ", s).strip().lstrip(",; ")
    s = re.sub(r"\s*\.+$", "", s)
    return s[:1].upper() + s[1:] if s else s


def build_en(html_path: Path) -> list:
    """Tách JSON từ vựng khỏi file HTML cũ, lọc rác, gắn cấp độ.

    Returns:
        Danh sách mục ``[en, vi, pos, ipa, ex, level, topic]`` đã sắp theo cấp.
    """
    html = html_path.read_text(encoding="utf-8")
    m = re.search(r'<script id="vocabulary" type="application/json">(.*?)</script>', html, re.S)
    data = json.loads(m.group(1))
    seen, rows, dropped = set(), [], 0
    for w in data:
        en, vi = w["en"].strip(), w["vi"].strip()
        if not en or not vi or JUNK.search(vi) or en.lower() in seen:
            dropped += 1
            continue
        seen.add(en.lower())
        pos = POS_MAP.get(w.get("pos") or "", w.get("pos") or "")
        pos = pos if pos in POS_OK else ""
        topic = "" if NOT_TOPIC.search(w["cat"]) or w["cat"] == "Từ điển mở rộng" else w["cat"]
        rows.append([en, clean_vi(vi), pos, w.get("ipa") or "", w.get("ex") or "", level_en(en, bool(topic)), topic,
                     zipf_frequency(en, "en")])
    # Trong cùng cấp, từ hay gặp đứng trước để lượt "Từ mới" ưu tiên từ đáng học.
    rows.sort(key=lambda r: (r[5], -r[7]))
    for r in rows:
        r.pop()
    print(f"en: giữ {len(rows)}, bỏ {dropped}")
    return rows


def load_cvdict(path: Path) -> dict:
    """Đọc CVDICT thành dict ``giản thể -> [(pinyin số viết thường, [nghĩa])]``."""
    d = {}
    line_re = re.compile(r"^(\S+) (\S+) \[([^\]]*)\] /(.*)/$")
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("#"):
            continue
        m = line_re.match(line)
        if m:
            d.setdefault(m.group(2), []).append((m.group(3).lower().replace("u:", "v"), m.group(4).split("/")))
    return d


BAD_SENSE = re.compile(r"^(biến thể|họ |xem |cũng được viết|dạng phồn thể|viết tắt của|CL:)", re.I)


def pick_vi(senses: list) -> str:
    """Chọn tối đa 3 nghĩa dùng được, bỏ nghĩa kiểu "biến thể của…", "họ …"."""
    good = []
    for s in senses:
        if not s or BAD_SENSE.search(s):
            continue
        s = re.sub(r"\[[a-z0-9: ]+\]", "", s)  # bỏ pinyin tham chiếu kiểu 您[nin2]
        s = re.sub(r"[㐀-鿿]+\|", "", s).strip()  # 詞|词 -> 词
        good.append(s)
    return "; ".join(list(dict.fromkeys(g for g in good if g))[:3])


def build_zh(hsk_path: Path, cvdict_path: Path) -> list:
    """Ghép danh sách HSK với nghĩa tiếng Việt từ CVDICT.

    Returns:
        Danh sách ``[hanzi, pinyin, vi, en, level, pos]`` sắp theo cấp HSK rồi tần suất.
    """
    cv = load_cvdict(cvdict_path)
    hsk = json.loads(hsk_path.read_text(encoding="utf-8"))
    rows, miss = [], 0
    for w in hsk:
        levels = w.get("l", [])
        new = [int(x[1:]) for x in levels if x.startswith("n")]
        old = [int(x[1:]) for x in levels if x.startswith("o")]
        if not new and not old:
            continue
        level = min(new) if new else min(old)
        form = w["f"][0]
        py_num = form["i"]["n"].lower().replace("u:", "v")
        cands = cv.get(w["s"], [])
        exact = [s for p, s in cands if p.replace(" ", "") == py_num.replace(" ", "")]
        vi = ""
        for senses in exact + [s for _, s in cands]:
            vi = pick_vi(senses)
            if vi:
                break
        if not vi:
            miss += 1
            continue
        en = "; ".join(form["m"][:3])
        rows.append([w["s"], form["i"]["y"], vi[:1].upper() + vi[1:], en, level, (w.get("p") or [""])[0], w.get("q", 99999)])
    rows.sort(key=lambda r: (r[4], r[6]))
    for r in rows:
        r.pop()
    print(f"zh: giữ {len(rows)}, thiếu nghĩa {miss}")
    return rows


def main():
    html, hsk, cvd = map(Path, sys.argv[1:4])
    OUT.mkdir(exist_ok=True)
    en = build_en(html)
    # Tách kho Anh theo cấp: mở app chỉ tải cấp đang học (cấp 1 ≈ 0,4 MB) thay vì 11 MB.
    files = {f"en-{lv}": [r for r in en if r[5] == lv] for lv in (1, 2, 3, 4)}
    files["zh"] = build_zh(hsk, cvd)
    for name, rows in files.items():
        (OUT / f"{name}.json").write_text(json.dumps(rows, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    # meta.json: số từ mỗi cấp + danh sách chủ đề, để app vẽ bộ lọc/tiến độ
    # mà không phải tải hết 11 MB dữ liệu.
    topics = sorted({r[6] for r in en if r[6]})
    meta = {
        "en": {"levels": {lv: len(files[f"en-{lv}"]) for lv in (1, 2, 3, 4)}, "topics": topics},
        "zh": {"levels": {lv: sum(1 for r in files["zh"] if r[4] == lv) for lv in range(1, 8)}},
    }
    (OUT / "meta.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
