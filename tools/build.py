"""maimy photo 静的サイトジェネレータ。docs/ 以下に HTML を書き出す。

usage: python3 tools/build.py
"""
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
META = json.loads((DOCS / "img/meta.json").read_text())

LINE_URL = "https://lin.ee/narDqNW"
INSTAGRAM_URL = "https://www.instagram.com/maimy_photo/"
YEAR = 2026
CURRENT = ' aria-current="page"'
PRESSED = ' aria-pressed="true"'
UNPRESSED = ' aria-pressed="false"'

NAV = [
    ("plan/", "Plan & Price", "撮影プラン"),
    ("flow/", "Flow", "ご予約の流れ"),
    ("gallery/", "Gallery", "作品"),
    ("about/", "About", "わたしについて"),
    ("goods/", "Goods", "おすすめのお店"),
    ("contact/", "Contact", "お問い合わせ"),
]


# ---------------------------------------------------------------- helpers

def img(base, name, alt, sizes="100vw", cls="", eager=False):
    m = META[name]
    srcset = ", ".join(f"{base}img/{name}-{w}.webp {w}w" for w in m["sizes"])
    largest = m["sizes"][-1]
    attrs = [
        f'src="{base}img/{name}-{m["sizes"][0]}.webp"',
        f'srcset="{srcset}"',
        f'sizes="{sizes}"',
        f'width="{largest}" height="{round(m["h"] * largest / m["w"])}"',
        f'alt="{escape(alt)}"',
        'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"',
        'decoding="async"',
    ]
    if cls:
        attrs.append(f'class="{cls}"')
    return f"<img {' '.join(attrs)}>"


def line_button(label="公式LINEで相談する", cls="btn btn--line"):
    return (
        f'<a class="{cls}" href="{LINE_URL}" target="_blank" rel="noopener">'
        '<svg aria-hidden="true" viewBox="0 0 24 24" width="20" height="20"><path fill="currentColor" d="M12 3C6.48 3 2 6.6 2 11.04c0 3.98 3.55 7.31 8.35 7.94.33.07.77.22.88.5.1.25.07.65.03.9l-.14.85c-.04.25-.2.98.86.53 1.06-.45 5.73-3.37 7.82-5.78C21.24 14.4 22 12.8 22 11.04 22 6.6 17.52 3 12 3Zm-3.6 10.4H6.42a.53.53 0 0 1-.53-.53V8.9a.53.53 0 1 1 1.06 0v3.44H8.4a.53.53 0 1 1 0 1.06Zm2.05-.53a.53.53 0 1 1-1.06 0V8.9a.53.53 0 1 1 1.06 0v3.97Zm4.77 0a.53.53 0 0 1-.95.32l-2.03-2.77v2.45a.53.53 0 1 1-1.06 0V8.9a.53.53 0 0 1 .95-.32l2.03 2.77V8.9a.53.53 0 1 1 1.06 0v3.97Zm3.21-2.51a.53.53 0 1 1 0 1.06h-1.45v.92h1.45a.53.53 0 1 1 0 1.06h-1.98a.53.53 0 0 1-.53-.53V8.9c0-.29.24-.53.53-.53h1.98a.53.53 0 1 1 0 1.06h-1.45v.93h1.45Z"/></svg>'
        f"<span>{label}</span></a>"
    )


def section_head(en, ja, align=""):
    cls = f"section-head {align}".strip()
    return f'<header class="{cls}"><p class="eyebrow">{en}</p><h2>{ja}</h2></header>'


# ---------------------------------------------------------------- layout

def layout(path, title, body, description, current="", base=None, body_class=""):
    if base is None:
        base = "../" * path.count("/")
    nav_items = "".join(
        f'<li><a href="{base}{href}"{CURRENT if href == current else ""}>'
        f'<span class="en">{en}</span><span class="ja">{ja}</span></a></li>'
        for href, en, ja in NAV
    )
    full_title = f"{title} | maimy photo" if title else "maimy photo | 埼玉・出張撮影カメラマン"
    return f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<!-- プレビュー環境: 検索エンジンにインデックスさせない -->
<meta name="robots" content="noindex, nofollow, noarchive, nosnippet, noimageindex">
<meta name="googlebot" content="noindex, nofollow">
<title>{escape(full_title)}</title>
<meta name="description" content="{escape(description)}">
<meta name="theme-color" content="#f7f3ee">
<link rel="icon" href="{base}favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400&family=Shippori+Mincho:wght@400;500&family=Zen+Kaku+Gothic+New:wght@400;500&display=swap">
<link rel="stylesheet" href="{base}assets/style.css">
<script src="{base}assets/main.js" defer></script>
</head>
<body class="{body_class}">
<a class="skip" href="#main">本文へスキップ</a>
<header class="site-header" data-header>
  <div class="site-header__inner">
    <a class="logo" href="{base}" aria-label="maimy photo トップへ">maimy <i>photo</i></a>
    <nav class="gnav" aria-label="メインメニュー">
      <ul>{nav_items}</ul>
    </nav>
    <a class="header-cta" href="{LINE_URL}" target="_blank" rel="noopener">Reserve</a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="drawer" data-menu-toggle>
      <span></span><span></span><span class="sr">メニュー</span>
    </button>
  </div>
</header>
<div class="drawer" id="drawer" hidden data-drawer>
  <nav aria-label="モバイルメニュー"><ul>{nav_items}</ul></nav>
  {line_button("公式LINEでご予約・ご相談")}
</div>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="container site-footer__inner">
    <div>
      <a class="logo logo--lg" href="{base}">maimy <i>photo</i></a>
      <p class="site-footer__lead">埼玉を拠点に、ご家族・ニューボーン・七五三・ウェディング・<br class="pc">プロフィール・内装写真の出張撮影をしています。</p>
    </div>
    <nav aria-label="フッターメニュー">
      <ul class="fnav">{''.join(f'<li><a href="{base}{href}">{en}</a></li>' for href, en, _ in NAV)}</ul>
    </nav>
    <div class="site-footer__social">
      <a href="{INSTAGRAM_URL}" target="_blank" rel="noopener">Instagram</a>
      <a href="{LINE_URL}" target="_blank" rel="noopener">LINE</a>
    </div>
  </div>
  <p class="copyright container">© {YEAR} maimy photo</p>
</footer>
</body>
</html>
"""


# ---------------------------------------------------------------- plans

PLANS = [
    {
        "slug": "family",
        "en": "Family",
        "ja": "家族写真",
        "image": "family",
        "thumb": "family-square",
        "catch": "いつもの笑顔を、ずっと残る一枚に。",
        "lead": "お散歩の途中のような、自然体のご家族の時間を撮影します。公園や海辺、ご自宅の近くなど、思い出の場所でどうぞ。",
        "from": "24,000",
        "prices": [("平日", "24,000"), ("土日祝", "26,000")],
        "tax": "税込",
        "specs": [("撮影時間", "1時間程度"), ("納品枚数", "100枚以上"), ("撮影場所", "1箇所")],
        "notes": [
            "公園や公共施設での撮影をご希望の際は、事前に撮影許可についてご確認ください。",
            "遠方の場合は別途交通費をいただく場合がございます。",
        ],
        "gallery": ["hero-family", "hero-kids", "family"],
    },
    {
        "slug": "newborn",
        "en": "Newborn",
        "ja": "ニューボーンフォト",
        "image": "newborn",
        "thumb": "newborn",
        "catch": "生まれたての、今しかない小ささを。",
        "lead": "日常のミルクの様子などに加え、おくるみ撮影が含まれているプランです。撮影セットをご自宅にお持ちして撮影します。",
        "from": "33,000",
        "prices": [("平日", "33,000"), ("土日祝", "35,000")],
        "tax": "税込",
        "specs": [
            ("撮影時間", "2〜3時間程度"),
            ("納品枚数", "50枚以上"),
            ("撮影可能時期", "生後3週間まで"),
            ("撮影場所", "ご自宅"),
        ],
        "notes": [
            "小物や撮影セットはこちらで準備いたします。一緒に写したいもの（指輪やエコー写真、ぬいぐるみなど）がありましたらご準備ください。",
            "生花はアレルギーが発症する場合があるため、造花で撮影しています。生花との撮影をご希望の際はご準備をお願いします。",
            "赤ちゃんを第一とした撮影を行っておりますので、場合によっては納品枚数が50枚に達しない場合がございます。",
            "ご予約は妊娠後期（28週以降）をおすすめしています。出産予定の前後にはできる限り柔軟に対応いたしますが、ご希望の日程に延期できない場合もございます。",
            "おくるみを巻くのは専門的な知識が必要です。ご自身で巻くのは危険ですのでご遠慮ください。",
            "遠方の場合は別途交通費をいただく場合がございます。",
        ],
        "gallery": ["newborn", "newborn-feet"],
    },
    {
        "slug": "753",
        "en": "Shichi-Go-San",
        "ja": "七五三",
        "image": "shichigosan",
        "thumb": "shichigosan-square",
        "catch": "晴れの日の、凛とした表情と家族の笑顔。",
        "lead": "お子さまのお写真はもちろん、家族写真やお参りしている当日の様子などを撮影します。3歳の女の子限定で、お着物セットプランもご用意しています。",
        "from": "25,000",
        "prices": [("撮影料金", "25,000")],
        "tax": "税込 + 交通費",
        "specs": [
            ("撮影時間", "1時間程度"),
            ("納品枚数", "80枚以上"),
            ("納品形式", "データのみ"),
            ("撮影場所", "ご希望の神社"),
        ],
        "options": [("ご兄弟1人追加", "3,000円", "納品枚数は100枚保証になります"), ("土日祝撮影", "3,000円", "")],
        "notes": [
            "番傘や手毬、千歳飴の袋など、撮影小物の貸出は行っておりません。",
            "撮影不可の神社や、カメラマンと提携している神社もありますので事前にご確認ください。撮影申請はお客様にてお願いしています。ご祈祷中の撮影をご希望の方は、あわせて可否をご確認ください。",
            "交通費は基本的に大宮駅から神社の最寄り駅またはバス停までの往復分です。撮影状況により変更になる場合がございます。",
        ],
        "related": "753-kimono",
        "gallery": ["shichigosan", "shichigosan-square"],
    },
    {
        "slug": "753-kimono",
        "en": "Kimono Set",
        "ja": "七五三 お着物セット",
        "image": "kimono",
        "thumb": "kimono",
        "catch": "3歳の女の子限定、準備まるごとおまかせ。",
        "lead": "お着物も髪飾りもヘアメイクも、撮影依頼もご祈祷の予約も…「やることがたくさんで大変！」というママさんパパさんのためのプランです。お着物レンタルからお着付け、簡単なヘアセット、撮影までがセットになっています。",
        "from": "33,000",
        "prices": [("撮影料金", "33,000")],
        "tax": "税込 + 交通費",
        "specs": [("撮影時間", "3時間程度"), ("納品枚数", "100枚以上"), ("撮影場所", "1箇所")],
        "options": [("ご兄弟1人追加", "3,000円", "納品枚数は100枚保証になります"), ("土日祝撮影", "3,000円", "")],
        "set": ["撮影・編集・データ納品", "お着物レンタル", "お支度（着付けとヘアセット）", "※V字の肌着だけご用意をお願いしています"],
        "steps": [
            ("ご自宅でお支度", "ご自宅にお伺いし、お着付け・お支度をします（約30分〜1時間）"),
            ("神社で撮影", "神社に移動して撮影します（1時間〜1時間半）"),
            ("解散", "そのまま解散、もしくはお着替え＆お着物の返却"),
        ],
        "details": [
            (
                "お着物レンタルについて",
                [
                    "レンタル期間は撮影当日までです。撮影後、解散した後もご家族でお写真を撮っていただいて構いません。",
                    "撮影日の翌日までに、指定の住所へご郵送ください（郵送料はご負担をお願いします）。撮影終了後にそのままお着替え→返却でも構いません。",
                    "返却が遅れる場合は必ずご連絡ください。お客様都合で返却が遅れる場合は、1日につき3,000円をご負担いただきます。",
                    "クリーニングは不要です。そのまま梱包してください。過度な汚れがある場合はあらかじめご相談ください。",
                    "著しい汚損・破損の場合はクリーニング代・修理費等の実費を、紛失の場合は商品代金の実費をご請求させていただきます。",
                ],
            ),
            (
                "ヘアセット・お支度について",
                [
                    "ヘアセットは簡単なアップヘアのみの対応です。巻き髪や編み込み、日本髪など20分以上かかるヘアセットをご希望の場合は、ご自身でお願いしています。",
                    "簡易的なご希望（ひとつ結び、二つ結びなど）はお伺いしますが、毛量によって使える飾りも異なるため、基本的にはおまかせとなります。",
                ],
            ),
        ],
        "notes": [
            "番傘や手毬、千歳飴の袋など、撮影小物の貸出は行っておりません。",
            "撮影不可の神社や、カメラマンと提携している神社もありますので事前にご確認ください。撮影申請はお客様にてお願いしています。",
            "交通費は基本的に、大宮駅→ご自宅→神社（電車代もしくはタクシー代。お客様のお車に乗せていただける場合は不要）→大宮駅の合計です。",
            "お着物の数に限りがあるため、お早めにご相談ください。",
        ],
        "gallery": ["kimono", "shichigosan"],
    },
    {
        "slug": "wedding",
        "en": "Wedding",
        "ja": "ウェディングフォト",
        "image": "wedding",
        "thumb": "wedding-field",
        "catch": "ふたりらしい空気ごと、やわらかく。",
        "lead": "桜の下や海辺、思い出の場所で。ロケーションでのウェディングフォトを撮影します。",
        "from": "25,000",
        "prices": [("平日", "25,000"), ("土日祝", "27,000")],
        "tax": "税込",
        "specs": [
            ("撮影時間", "1時間半程度"),
            ("納品枚数", "100枚以上"),
            ("納品形式", "データのみ"),
            ("撮影場所", "1箇所"),
        ],
        "notes": [
            "ドレス、ブーケ、ベールなど、衣装小物関係はすべてお客様にご用意をお願いしています。",
            "公園や公共施設での撮影をご希望の際は、事前に撮影許可についてご確認ください。",
            "遠方の場合は別途交通費をいただく場合がございます。",
        ],
        "gallery": ["wedding-sakura", "hero-wedding", "wedding"],
    },
    {
        "slug": "profile",
        "en": "Profile",
        "ja": "プロフィール写真",
        "image": "profile",
        "thumb": "profile-square",
        "catch": "あなたらしさが伝わる、自然な表情を。",
        "lead": "SNSやお仕事用のプロフィール写真を撮影します。撮られるのが苦手な方も、お話ししながらリラックスして撮影しましょう。",
        "from": "24,000",
        "prices": [("平日", "24,000"), ("土日祝", "26,000")],
        "tax": "税込",
        "specs": [("撮影時間", "1時間程度"), ("納品枚数", "100枚以上"), ("撮影場所", "1箇所")],
        "notes": [
            "公園や公共施設での撮影をご希望の際は、事前に撮影許可についてご確認ください。",
            "遠方の場合は別途交通費をいただく場合がございます。",
        ],
        "gallery": ["profile-camera", "profile-green", "profile"],
    },
    {
        "slug": "interior",
        "en": "Interior",
        "ja": "内装・竣工写真",
        "image": "interior",
        "thumb": "interior-chair",
        "catch": "空間の魅力まで伝わる写真を。",
        "lead": "企業さま向けの内装写真・竣工写真の撮影プランです。「ただ空間がわかる」写真ではなく、「その空間の魅力が伝わる」写真を心がけています。前職の設計・デザインの経験を活かして撮影します。",
        "from": "50,000",
        "prices": [("撮影料金", "50,000")],
        "tax": "税抜 + 交通費",
        "specs": [
            ("撮影時間", "2時間"),
            ("納品枚数", "30枚以上"),
            ("納品形式", "データのみ"),
            ("撮影場所", "1案件"),
        ],
        "steps": [
            ("お見積もり", "公式LINEにて撮影概要をお伺いした後、お見積もりをいたします。"),
            ("お打ち合わせ", "必要なカットなどについてお打ち合わせをします。"),
            ("撮影", "お写真をご確認いただきながら撮影を進めます。"),
            ("納品・ご請求", "2週間以内に納品と請求書の発行をいたします。指定の口座へお振り込みをお願いします。"),
        ],
        "notes": [
            "交通費は大宮駅からの往復分をいただいています。撮影状況により変更になる場合がございます。",
            "平米数や撮影内容によって追加料金をいただく場合がございます。お見積もりは公式LINEにてご連絡ください。",
            "基本的には撮影日より2週間以内に納品いたします。お急ぎの際はご相談ください。",
        ],
        "gallery": ["interior-arch", "interior-office", "interior-chair", "interior-desk"],
    },
]
PLAN_BY_SLUG = {p["slug"]: p for p in PLANS}


def plan_card(base, p, href_prefix="plan/"):
    unit = "〜" if len(p["prices"]) > 1 else ""
    return f"""<li class="plan-card reveal">
  <a href="{base}{href_prefix}{p['slug']}/">
    <div class="plan-card__img">{img(base, p['thumb'], p['ja'], sizes='(min-width: 960px) 30vw, (min-width: 600px) 45vw, 90vw')}</div>
    <div class="plan-card__body">
      <p class="plan-card__en">{p['en']}</p>
      <h3>{p['ja']}</h3>
      <p class="plan-card__price">¥{p['from']}<small>{unit}（{p['tax'].split(' ')[0]}）</small></p>
    </div>
  </a>
</li>"""


def plan_page(p):
    base = "../../"
    prices = "".join(
        f'<div class="price"><dt>{label}</dt><dd><span class="yen">¥</span>{v}</dd></div>' for label, v in p["prices"]
    )
    specs = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in p["specs"])
    blocks = []
    if p.get("set"):
        items = "".join(f"<li>{s}</li>" for s in p["set"])
        blocks.append(f'<section class="plan-block"><h2 class="plan-block__title">セット内容</h2><ul class="checklist">{items}</ul></section>')
    if p.get("options"):
        items = "".join(
            f'<li><span>{n}</span><span class="opt-price">+{v}</span>{f"<small>{s}</small>" if s else ""}</li>'
            for n, v, s in p["options"]
        )
        blocks.append(f'<section class="plan-block"><h2 class="plan-block__title">追加オプション</h2><ul class="options">{items}</ul></section>')
    if p.get("steps"):
        title = "当日の流れ" if p["slug"] == "753-kimono" else "撮影までの流れ"
        items = "".join(f"<li><h3>{t}</h3><p>{d}</p></li>" for t, d in p["steps"])
        blocks.append(f'<section class="plan-block"><h2 class="plan-block__title">{title}</h2><ol class="steps">{items}</ol></section>')
    for title, lines in p.get("details", []):
        items = "".join(f"<li>{l}</li>" for l in lines)
        blocks.append(
            f'<details class="accordion"><summary>{title}</summary><ul class="notes">{items}</ul></details>'
        )
    notes = "".join(f"<li>{n}</li>" for n in p["notes"])
    blocks.append(f'<section class="plan-block"><h2 class="plan-block__title">ご注意事項</h2><ul class="notes">{notes}</ul></section>')

    related = ""
    if p.get("related"):
        r = PLAN_BY_SLUG[p["related"]]
        related = f"""<a class="related reveal" href="../{r['slug']}/">
  <div class="related__img">{img(base, r['thumb'], r['ja'], sizes='(min-width: 760px) 280px, 100vw')}</div>
  <div class="related__body"><p class="eyebrow">{r['en']}</p><p class="related__title">{r['ja']}プランはこちら</p><p>{r['catch']}</p><span class="link-arrow">詳しく見る</span></div>
</a>"""

    gallery = "".join(
        f'<figure class="reveal">{img(base, g, p["ja"] + "の撮影例", sizes="(min-width: 960px) 33vw, 50vw")}</figure>'
        for g in p["gallery"]
    )
    others = "".join(plan_card(base, o, "plan/") for o in PLANS if o["slug"] != p["slug"])

    body = f"""
<section class="plan-hero">
  <div class="plan-hero__img">{img(base, p['image'], p['ja'], eager=True)}</div>
  <div class="container plan-hero__text">
    <nav class="breadcrumb" aria-label="パンくず"><a href="{base}">Home</a><span>/</span><a href="../">Plan</a><span>/</span><span>{p['en']}</span></nav>
    <p class="eyebrow">{p['en']} Plan</p>
    <h1>{p['ja']}</h1>
    <p class="catch">{p['catch']}</p>
  </div>
</section>

<section class="section container plan-detail">
  <div class="plan-detail__main">
    <p class="lead">{p['lead']}</p>
    <div class="price-box reveal">
      <dl class="prices">{prices}</dl>
      <p class="tax">（{p['tax']}）</p>
      <dl class="specs">{specs}</dl>
    </div>
    {''.join(blocks)}
    <div class="before-booking">
      <p>ご予約の前に必ず<a href="{base}flow/">ご予約の流れ・ご利用案内</a>をご確認ください。<br>その他ご質問や空き日程の確認は、お気軽に公式LINEにてご連絡ください。</p>
      {line_button("このプランを相談する")}
    </div>
    {related}
  </div>
  <aside class="plan-detail__side">
    <div class="sticky-gallery">{gallery}</div>
  </aside>
</section>

<section class="section section--tint">
  <div class="container">
    {section_head("Other Plans", "ほかのプラン")}
    <ul class="plan-grid plan-grid--small">{others}</ul>
  </div>
</section>
"""
    return layout(f"plan/{p['slug']}/", f"{p['ja']}プラン", body, f"maimy photo の{p['ja']}プラン。{p['lead']}", "plan/")


# ---------------------------------------------------------------- pages

def contact_band(base):
    return f"""
<section class="cta-band">
  <div class="cta-band__bg">{img(base, 'sea', '', sizes='100vw')}</div>
  <div class="container cta-band__inner reveal">
    <p class="eyebrow">Reservation</p>
    <h2>撮影のご予約・ご相談は<br>公式LINEから</h2>
    <p>「子どもが泣いてしまったら…」「撮られるのが苦手で…」<br class="pc">そんな不安も、一緒に考えながら解決していけたらと思っています。</p>
    {line_button()}
  </div>
</section>"""


def page_home():
    base = ""
    slides = ["hero-family", "hero-wedding", "hero-kids", "profile-green"]
    slide_html = "".join(
        f'<div class="hero__slide{" is-active" if i == 0 else ""}">{img(base, s, "", sizes="(min-width: 960px) 50vw, 100vw", eager=i == 0)}</div>'
        for i, s in enumerate(slides)
    )
    cards = "".join(plan_card(base, p) for p in PLANS if p["slug"] != "753-kimono")
    strip = ["newborn", "wedding-sakura", "kimono", "interior-arch", "family", "profile-camera", "newborn-feet", "interior-office"]
    strip_html = "".join(
        f'<li>{img(base, s, "作例写真", sizes="(min-width: 960px) 25vw, 50vw")}</li>' for s in strip
    )
    steps = [
        ("01", "ご予約", "公式LINEを友だち追加して、メッセージをお送りください。"),
        ("02", "お打ち合わせ", "ご希望のカットや撮影の割合など、詳細をご相談します。"),
        ("03", "撮影", "現地集合でご挨拶したのち、お話ししながら楽しく撮影。"),
        ("04", "お渡し", "撮影から2週間以内に、データで納品いたします。"),
    ]
    steps_html = "".join(
        f'<li class="reveal"><span class="num">{n}</span><h3>{t}</h3><p>{d}</p></li>' for n, t, d in steps
    )
    body = f"""
<section class="hero">
  <div class="hero__text">
    <p class="eyebrow">Outdoor &amp; Home Photography — Saitama</p>
    <h1 class="hero__title">自然で、<br>あったかくて、<br>思わず笑顔になる<br>写真を。</h1>
    <p class="hero__lead">埼玉を拠点にした出張撮影カメラマンです。<br>ご家族の何気ない幸せを、ずっと見返したくなる一枚に。</p>
    <div class="hero__actions">
      <a class="btn" href="plan/">プランを見る</a>
      <a class="link-arrow" href="gallery/">作品を見る</a>
    </div>
  </div>
  <div class="hero__visual" data-slideshow>{slide_html}</div>
  <p class="hero__scroll" aria-hidden="true">Scroll</p>
</section>

<section class="section container intro">
  <div class="intro__img reveal">{img(base, 'about', 'カメラマン まい', sizes='(min-width: 960px) 40vw, 100vw')}</div>
  <div class="intro__text reveal">
    <p class="eyebrow">Message</p>
    <h2>目の前にある幸せを、<br>写真で実感できるように。</h2>
    <p>忙しい日々の中で見逃してしまいがちな、目の前にある幸せ。写真を見返したとき、自分のことをもっと好きになれるように、心が温かく包まれるように——そんな想いで撮影しています。</p>
    <a class="link-arrow" href="about/">わたしについて</a>
  </div>
</section>

<section class="section section--tint">
  <div class="container">
    {section_head("Plan &amp; Price", "撮影プラン")}
    <ul class="plan-grid">{cards}</ul>
    <p class="center"><a class="btn btn--ghost" href="plan/">すべてのプランを見る</a></p>
  </div>
</section>

<section class="section">
  <div class="container">{section_head("Gallery", "作品")}</div>
  <ul class="strip" aria-label="作例">{strip_html}</ul>
  <p class="center"><a class="link-arrow" href="gallery/">ギャラリーへ</a></p>
</section>

<section class="section container">
  {section_head("Flow", "ご予約から納品まで")}
  <ol class="flow-steps">{steps_html}</ol>
  <p class="center"><a class="btn btn--ghost" href="flow/">ご予約の流れ・ご利用案内</a></p>
</section>
{contact_band(base)}
"""
    return layout("", "", body, body_class="is-home", description="埼玉を拠点に活動する出張撮影カメラマン maimy photo。家族写真、ニューボーンフォト、七五三、ウェディング、プロフィール、内装写真の撮影を承っています。")


def page_header(en, ja, lead=""):
    lead_html = f'<p class="page-header__lead">{lead}</p>' if lead else ""
    return f'<header class="page-header container"><p class="eyebrow">{en}</p><h1>{ja}</h1>{lead_html}</header>'


def page_plan_index():
    base = "../"
    cards = "".join(plan_card(base, p) for p in PLANS)
    body = f"""
{page_header("Plan &amp; Price", "撮影プラン", "ご家族の記念日から企業さまの内装撮影まで。<br>すべてのプランは出張撮影で、データでの納品となります。")}
<section class="section section--flush container">
  <ul class="plan-grid">{cards}</ul>
</section>
<section class="section container common-info">
  <div class="info-grid">
    <div class="reveal"><h3>納品について</h3><p>撮影から2週間以内に、ギガファイル便もしくはGoogle Driveにてデータでお渡しします。写真の選定は当方で行います。</p></div>
    <div class="reveal"><h3>お支払いについて</h3><p>撮影日の5日前までに指定口座へのお振り込みをお願いしています（内装撮影は納品時にご請求）。</p></div>
    <div class="reveal"><h3>交通費について</h3><p>遠方の場合は別途交通費をいただく場合がございます。詳しくは各プランをご確認ください。</p></div>
  </div>
  <p class="center"><a class="link-arrow" href="../flow/">ご利用案内を見る</a></p>
</section>
{contact_band(base)}
"""
    return layout("plan/", "撮影プラン・料金", body, "maimy photo の撮影プランと料金一覧。", "plan/")


TERMS = [
    ("1. 当サービスについてのご案内", [
        ("ア. ご利用時間について", "予約のお時間に集合場所へお越しください。ご予約時間に遅れますと100％のサービス（カット数、パターン数等）が提供できない場合がございます。この場合も料金の変更はございません。また1時間以上の遅刻は当日キャンセル扱いとさせていただきます。"),
        ("イ. 撮影できるご家族単位について", "撮影プランの料金は一家族での料金となります。お友達同士の撮影をご希望の場合は、どの撮影においても家族数分のお値段を頂戴しております（3家族の場合、通常のお値段×3家族分）。"),
        ("ウ. お渡しするデータについて", "お写真はデータのみ、撮影から2週間以内のお渡しになります。データはギガファイル便もしくはGoogle Driveでのお渡しになります。選定は当サービスにて行います。アートニューボーンプラン以外のプランでのお顔や傷などの修正は承っておりません。当サービスでのデータの保証期間は撮影日より3ヶ月とさせていただいております。また、保証期間の終了日にご連絡は致しておりません。"),
        ("エ. お支払いについて", "基本的には撮影日の5日前までに指定の口座にお振り込みをお願いしています。interior PLANに関してのみ、撮影前に見積書を、納品時に合わせて請求書をお送りいたします。"),
    ]),
]

CANCEL = [("撮影当日", "100%", "40%"), ("前日", "70%", "30%"), ("3日前", "60%", "20%"), ("4日前", "50%", "10%"), ("5日以上前", "無料", "無料")]


def page_flow():
    base = "../"
    steps = [
        ("01", "ご予約", "公式LINEをお友だち追加の上、メッセージをお送りください。3日以内にご返信いたします。"),
        ("02", "お打ち合わせ", "ご希望のカットや撮影の割合など、撮影の詳細についてお打ち合わせをします。撮影の5日前までに撮影料金のお支払いをお願いしています。"),
        ("03", "撮影", "現地集合で少しご挨拶させていただいた後、撮影に入ります。撮影中はお話ししながら楽しく撮影しています。"),
        ("04", "お渡し", "撮影から2週間以内にデータで納品します。ギガファイル便というオンラインサービスでのお渡しになるため、PCでのダウンロードをおすすめしています。"),
    ]
    steps_html = "".join(
        f'<li class="reveal"><span class="num">{n}</span><div><h3>{t}</h3><p>{d}</p></div></li>' for n, t, d in steps
    )
    terms_html = ""
    for _, items in TERMS:
        terms_html += "".join(f"<details class=\"accordion\"><summary>{t}</summary><p>{d}</p></details>" for t, d in items)
    rows = "".join(f"<tr><th scope=\"row\">{d}</th><td>{c}</td><td>{p}</td></tr>" for d, c, p in CANCEL)
    body = f"""
{page_header("Flow", "ご予約の流れ", "ご予約から納品まで、4つのステップで進みます。")}
<section class="section section--flush container narrow">
  <ol class="flow-list">{steps_html}</ol>
  <p class="center">{line_button("公式LINEで予約する")}</p>
</section>

<section class="section section--tint" id="terms">
  <div class="container narrow">
    {section_head("Terms", "ご利用案内")}
    <p class="terms-intro">maimy photoにて提供されるサービス（以下、本サービス）をご利用されるお客様には、以下のご利用案内（以下、本規約）が適用されます。本規約の内容に同意いただけない場合には、ご依頼をお断りさせていただきます。</p>

    <h3 class="terms-h">1. 当サービスについてのご案内</h3>
    {terms_html}
    <details class="accordion" open>
      <summary>オ. キャンセル・延期について</summary>
      <p><strong>A. キャンセル・延期方法</strong><br>撮影予約の取り消しや延期を希望する場合、公式LINEにてご連絡ください。無断キャンセルの場合は、ご利用料金の100%のキャンセル料を請求させていただきます。金融機関の5営業日以内に、指定の口座にお振込みいただきます。お振込がない場合、法的な措置を取らせていただく場合がございます。</p>
      <p><strong>B. キャンセル料・C. 延期料</strong><br>警報および緊急事態宣言が出た場合、キャンセル料・延期料は頂戴しません。それ以外の場合、以下の料金が発生いたします（ご利用料金に対する割合）。</p>
      <div class="table-wrap">
        <table class="fee-table">
          <thead><tr><th scope="col">撮影予定日の</th><th scope="col">キャンセル料</th><th scope="col">延期料</th></tr></thead>
          <tbody>{rows}</tbody>
        </table>
      </div>
      <p>撮影時間に1時間以上遅刻した場合は、当日キャンセル扱いとさせていただきます。またご予約時間から30分過ぎてもご連絡がない場合は無断キャンセルとみなし、当日キャンセル扱いとさせていただきます。</p>
      <p>newborn PLANに関して、ご出産の前後による延期は無料で延期が可能です。延期日はご希望の日程でお伺いできない場合もございますのでご了承ください。</p>
    </details>
    <details class="accordion">
      <summary>カ. お写真掲載について</summary>
      <p>お客様による事前の同意がある場合に限り、本サービスのプロモーション等において、撮影データを利用することができるものとします。お客様による同意が撤回された場合、当サービスはプロモーション等での利用をすみやかに停止します。</p>
    </details>
    <details class="accordion">
      <summary>キ. 本サービスの転用・転売の禁止</summary>
      <p>本サービス上に掲載された画像を無断転載・無断利用することは禁止します。また、撮影したお写真は当サービスに著作権が帰属いたします。個人的な利用以外の目的（広告を伴うWeb上での公開も含む）にて、複製、配布、販売、公開等を行うことはできません。</p>
    </details>

    <h3 class="terms-h">2. ご利用上のルール及びご注意事項</h3>
    <ul class="notes notes--plain">
      <li>当サービス内でのお客様の転倒・衝突等による事故については、原則として責任を負いかねます。特に小さなお子様からは目を離されないようご注意をお願いします。</li>
      <li>お客様の故意の過失により備品・設備が大きく破損した場合は、相応の弁償をしていただくことがございます。</li>
      <li>天候による警報が出た際や緊急事態宣言、悪天候や交通機関の規制等、やむを得ない事情により当サービスの営業ができないときは、別日程、別時間帯で撮影をご案内させていただくことがあります。また、個人で提供しているサービスのため、体調不良、肉親の葬儀などで日程の変更をお伺いする場合もございます。精一杯尽力いたしますが、万が一の場合があることをご理解いただいた上でご予約ください。</li>
      <li>画像データをお渡しした時点で、その内容にご納得いただけたものと致します。その後は、金品における代償はいたしておりません。</li>
    </ul>

    <h3 class="terms-h">3. 本規約の変更</h3>
    <p>当サービスは、当サービスのWEBサイトに公開することにより本規約を変更することができます。変更した規約等の効力は全てお客様に及ぶものとします。</p>
  </div>
</section>
{contact_band(base)}
"""
    return layout("flow/", "ご予約の流れ・ご利用案内", body, "maimy photo のご予約から納品までの流れと、ご利用案内（キャンセル規定など）。", "flow/")


def page_about():
    base = "../"
    body = f"""
{page_header("About", "わたしについて")}
<section class="section section--flush container about">
  <figure class="about__img reveal">{img(base, 'about', 'カメラマン まい', sizes='(min-width: 960px) 45vw, 100vw', eager=True)}</figure>
  <div class="about__text">
    <p class="about__name"><span>mai yamada</span>まい</p>
    <p>フリーランスのカメラマンをしております、「まい」と申します。実家は福島県、現在は埼玉県に住んでいます。</p>
    <p>前職は設計・デザイン職で、大学ではデザインについて学んでいました。カメラマンは小さい頃からの夢で、今こうしてたくさんのご家族にお会いでき、素敵なご縁に恵まれて、とても幸せ者だと思っています。</p>
  </div>
</section>

<section class="section section--tint">
  <div class="container narrow statement">
    <p class="eyebrow">Philosophy</p>
    <p class="statement__quote">“自然であったかくて、<br>思わず笑顔になるような”</p>
    <p>そんな写真を撮るのが得意です。</p>
    <p>私が写真を撮る理由は、どのツールよりも「伝わるもの」があると思っているからです。私が見た幸せや感動、こんなにも幸せが溢れていることを伝えたい。</p>
    <p>忙しい日々の中で見逃してしまいがちな、目の前にある幸せが実感できるように。<br>自分をもっと好きになれるように。<br>写真を見返したときに幸せな気持ちになるように。<br>私が撮った写真が、心を温かく包み込みますように。</p>
    <p>そんな想いを胸に、日々活動しております。</p>
  </div>
</section>

<section class="section container narrow worry">
  {section_head("For You", "はじめての撮影でも大丈夫")}
  <div class="worry__bubbles">
    <p class="bubble reveal">子どもが泣いてしまったらどうしよう</p>
    <p class="bubble reveal">撮られるのが苦手…上手く笑えるかな</p>
  </div>
  <p>撮影を申し込むにあたって、不安なことがたくさんあると思います。特に初めての撮影となると、どうすればいいか分からないことも多くて緊張しますよね。その不安を一緒に考えながら、解決していけたらと思っています。</p>
  <p>ぜひお気軽にご相談ください。皆さまにお会いできるのを楽しみにしています！</p>
</section>
{contact_band(base)}
"""
    return layout("about/", "わたしについて", body, "maimy photo カメラマン まい のプロフィール。", "about/")


GALLERY = [
    ("family", "hero-family"), ("wedding", "hero-wedding"), ("newborn", "newborn"), ("family", "hero-kids"),
    ("interior", "interior-arch"), ("753", "kimono"), ("profile", "profile-camera"), ("wedding", "wedding-sakura"),
    ("753", "shichigosan"), ("family", "family"), ("interior", "interior-chair"), ("newborn", "newborn-feet"),
    ("profile", "profile-green"), ("wedding", "wedding-field"), ("interior", "interior-office"), ("wedding", "wedding"),
    ("profile", "profile"), ("interior", "interior"), ("753", "shichigosan-square"), ("interior", "interior-desk"),
]
IG_ACCOUNTS = [
    ("maimy_photo", "メインアカウント"),
    ("milk_newbornphoto", "ニューボーンフォト"),
    ("imadamaya.to", "ポートレート"),
    ("interiorphoto.m", "内装写真"),
]


def page_gallery():
    base = "../"
    filters = [("all", "All"), ("family", "Family"), ("newborn", "Newborn"), ("753", "753"), ("wedding", "Wedding"), ("profile", "Profile"), ("interior", "Interior")]
    filter_html = "".join(
        f'<button type="button" data-filter="{k}"{PRESSED if k == "all" else UNPRESSED}>{v}</button>'
        for k, v in filters
    )
    items = "".join(
        f'<li data-cat="{cat}"><button type="button" class="masonry__btn" data-lightbox="{base}img/{name}-{META[name]["sizes"][-1]}.webp" aria-label="拡大表示">'
        f'{img(base, name, "作例写真", sizes="(min-width: 960px) 33vw, 50vw")}</button></li>'
        for cat, name in GALLERY
    )
    ig = "".join(
        f'<li><a href="https://www.instagram.com/{a}/" target="_blank" rel="noopener"><span class="ig-handle">@{a}</span><span class="ig-desc">{d}</span></a></li>'
        for a, d in IG_ACCOUNTS
    )
    body = f"""
{page_header("Gallery", "作品", "最新の作例はInstagramにて。お気軽にフォローしていただけたら嬉しいです。")}
<section class="section section--flush container">
  <div class="filters" role="group" aria-label="カテゴリで絞り込み">{filter_html}</div>
  <ul class="masonry" data-masonry>{items}</ul>
</section>
<section class="section section--tint">
  <div class="container narrow">
    {section_head("Instagram", "最新の作例はこちら")}
    <ul class="ig-list">{ig}</ul>
  </div>
</section>
<dialog class="lightbox" data-lightbox-dialog>
  <img alt="">
  <button type="button" class="lightbox__close" aria-label="閉じる">×</button>
</dialog>
"""
    return layout("gallery/", "作品ギャラリー", body, "maimy photo の撮影作品ギャラリー。", "gallery/")


def page_goods():
    base = "../"
    ratta = ["ratta-10", "ratta-15", "ratta-92", "ratta-28", "ratta-65", "ratta-40"]
    yamada = ["yamada-lead", "yamada-ex", "yamada-more01", "yamada-more02", "yamada-store", "yamada-ex2"]

    def photos(names, alt):
        return "".join(f'<li>{img(base, n, alt, sizes="(min-width: 960px) 20vw, 33vw")}</li>' for n in names)

    body = f"""
{page_header("Goods", "おすすめのお店", "撮影小物やプレゼントにおすすめのお店を2店舗ご紹介します。<br>どちらもオーナーさんが知り合いなので、ご質問は公式LINEにいただいても大丈夫です◎")}

<article class="section section--flush container shop">
  <div class="shop__head reveal">
    <p class="eyebrow">01 — Wooden Toys</p>
    <h2><small>見て遊べるおもちゃ屋さん</small>木のおもちゃ Ratta</h2>
  </div>
  <ul class="shop__photos">{photos(ratta, "木のおもちゃRattaの店内とおもちゃ")}</ul>
  <div class="shop__text reveal">
    <p>“おもちゃコンサルタント”の資格を持っている、センスの良いオーナーさんが厳選して仕入れた素敵な木のおもちゃがたくさん。本当にどれも可愛くて、手に取って遊んでみたくなります。店内では気になったおもちゃで実際に遊ぶこともできます。</p>
    <p>木のおもちゃは肌触りも音も心地よく、私もこちらで購入したおもちゃを撮影で使っています。撮影のときにおもちゃを手放してくれない…！そんなときも、木のおもちゃなら映っていても可愛いのでとても重宝しています。</p>
    <p class="shop__addr">福島県福島市 ／ 福島駅から徒歩5分ほど</p>
    <a class="link-arrow" href="https://www.instagram.com/ratta_ratta_/" target="_blank" rel="noopener">Instagram @ratta_ratta_</a>
  </div>
</article>

<article class="section container shop">
  <div class="shop__head reveal">
    <p class="eyebrow">02 — Embroidery</p>
    <h2><small>オーダーメイドの刺繍専門店</small>YAMADA NAME</h2>
  </div>
  <ul class="shop__photos">{photos(yamada, "YAMADA NAMEの刺繍作品")}</ul>
  <div class="shop__text reveal">
    <p>名前で気付いた方もいるかもしれませんが、実家のお店です。刺繍専門店で、1枚からオーダーメイドで刺繍をお願いすることができます。</p>
    <p>撮影小物はもちろん、オリジナルのプレゼントにもおすすめ。みんなでお揃いのお洋服にワンポイント刺繍を入れたり、1歳のお誕生日には一升餅で使うリュックに名前を入れても可愛いです。最近では刺繍の命名書をお部屋に飾るのも人気です。撮影小物を作りたい方はお気軽にご相談ください♪</p>
    <a class="link-arrow" href="https://yamadaname.com/" target="_blank" rel="noopener">YAMADA NAME 公式サイト</a>
  </div>
</article>
{contact_band(base)}
"""
    return layout("goods/", "おすすめのお店", body, "撮影小物やプレゼントにおすすめのお店のご紹介。", "goods/")


def page_contact():
    base = "../"
    body = f"""
{page_header("Contact", "お問い合わせ")}
<section class="section section--flush container contact">
  <div class="contact__img reveal">{img(base, 'sea', '海の風景', sizes='(min-width: 960px) 50vw, 100vw', eager=True)}</div>
  <div class="contact__text">
    <h2>ご予約・お問い合わせは<br>公式LINEにて承っています</h2>
    <p>公式LINEをお友だち追加の上、チャットにてご連絡ください。<br>3日以内にご返信いたします。</p>
    <ol class="contact__howto">
      <li>下のボタンから公式LINEを友だち追加</li>
      <li>ご希望のプラン・日程・撮影場所をお送りください</li>
      <li>空き状況を確認してご連絡します</li>
    </ol>
    {line_button("公式LINEを友だち追加")}
    <p class="small">ご予約の前に<a href="../flow/#terms">ご利用案内</a>をご確認ください。</p>
  </div>
</section>
"""
    return layout("contact/", "お問い合わせ", body, "maimy photo へのご予約・お問い合わせは公式LINEから。", "contact/")


def page_404():
    # 404.html は存在しない任意の階層で表示されるため、相対パスではなく絶対パスで参照する
    base = "/maimy_photo_preview/"
    body = f"""
<section class="section container narrow center notfound">
  <p class="eyebrow">404</p>
  <h1>ページが見つかりませんでした</h1>
  <p>お探しのページは移動または削除された可能性があります。</p>
  <p><a class="btn" href="{base}">トップへ戻る</a></p>
</section>"""
    return layout("", "ページが見つかりません", body, "ページが見つかりません", base=base)


# ---------------------------------------------------------------- main

def write(path, html):
    out = DOCS / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    print("wrote", out.relative_to(ROOT))


def main():
    write("index.html", page_home())
    write("plan/index.html", page_plan_index())
    for p in PLANS:
        write(f"plan/{p['slug']}/index.html", plan_page(p))
    write("flow/index.html", page_flow())
    write("about/index.html", page_about())
    write("gallery/index.html", page_gallery())
    write("goods/index.html", page_goods())
    write("contact/index.html", page_contact())
    write("404.html", page_404())


if __name__ == "__main__":
    main()
