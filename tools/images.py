"""旧サイト(WordPress書き出し)の画像から、新サイト用の WebP を生成する。

usage: python3 tools/images.py /path/to/maimy_photo
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageOps

SRC = Path(sys.argv[1]) / "wp-content/uploads/2023"
OUT = Path(__file__).resolve().parent.parent / "docs/img"
WIDTHS = (800, 1600)

# 新サイトでの名前 -> 旧サイトの元画像(最大解像度のもの)
IMAGES = {
    "hero-family": "03/573A4007.jpg",
    "hero-wedding": "03/573A5142.jpg",
    "hero-newborn": "06/12-1.jpg",
    "hero-kids": "04/6573A0548.jpg",
    "family": "02/MG_6568-195-2048x1365.jpg",
    "family-square": "04/MG_6568-195-edited-scaled.jpg",
    "newborn": "06/12-1.jpg",
    "newborn-feet": "06/04.jpg",
    "shichigosan": "01/573A2461-scaled.jpg",
    "shichigosan-square": "05/573A1030-scaled-e1685436878437.jpg",
    "kimono": "05/573A3673-2048x1365.jpg",
    "wedding": "03/573A5074-Edit.jpg",
    "wedding-sakura": "03/573A9071-Edit-10.jpg",
    "wedding-field": "03/573A4750.jpg",
    "profile": "04/573A6329.jpg",
    "profile-square": "05/573A6355-edited.jpg",
    "profile-camera": "01/最終2-4-scaled.jpg",
    "profile-green": "06/573A4300-scaled-e1685607829842.jpg",
    "interior": "04/573A8780-12.jpg",
    "interior-arch": "04/573A1413.jpg",
    "interior-chair": "05/573A2241-1-scaled.jpg",
    "interior-office": "04/573A1433.jpg",
    "interior-desk": "04/573A6246.jpg",
    "about": "01/573A6951-edited-scaled.jpg",
    "sea": "06/573A9462-202-1024x683.jpg",
    "ratta-10": "04/ratta-10.jpg",
    "ratta-15": "04/ratta-15.jpg",
    "ratta-28": "04/ratta-28.jpg",
    "ratta-40": "04/ratta-40.jpg",
    "ratta-65": "04/ratta-65.jpg",
    "ratta-92": "04/ratta-92.jpg",
    "yamada-lead": "04/lead-1.jpg",
    "yamada-ex": "04/ex2-1.jpg",
    "yamada-ex2": "04/ex-2-1.jpg",
    "yamada-more01": "04/more01-1.jpg",
    "yamada-more02": "04/more02-1.jpg",
    "yamada-store": "04/store-1.jpg",
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    meta = {}
    for name, rel in IMAGES.items():
        im = ImageOps.exif_transpose(Image.open(SRC / rel)).convert("RGB")
        w, h = im.size
        sizes = []
        for target in WIDTHS:
            tw = min(target, w)
            if sizes and tw == sizes[-1]:
                continue
            resized = im.resize((tw, round(h * tw / w)), Image.LANCZOS)
            resized.save(OUT / f"{name}-{tw}.webp", "WEBP", quality=80, method=6)
            sizes.append(tw)
        meta[name] = {"w": w, "h": h, "sizes": sizes}
        print(f"{name:22} {w}x{h} -> {sizes}")
    (OUT / "meta.json").write_text(json.dumps(meta, indent=1))


if __name__ == "__main__":
    main()
