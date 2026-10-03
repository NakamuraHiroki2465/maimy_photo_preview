# maimy photo — リニューアル プレビュー

maimy photo（https://maiyamada.com）リニューアル版のプレビュー環境です。
GitHub Pages の `docs/` から配信しています。

- プレビューURL: https://nakamurahiroki2465.github.io/maimy_photo_preview/
- 全ページに `<meta name="robots" content="noindex, nofollow, ...">` を付与し、検索エンジンにインデックスされないようにしています。
  本番に移行する際はこの meta タグを外してください（`tools/build.py` の `layout()`）。

## 構成

```
docs/            公開される静的サイト（生成物 + assets）
  assets/        style.css / main.js（手書き）
  img/           最適化済み WebP（tools/images.py で生成）
tools/
  images.py      旧サイトの画像から WebP を生成
  build.py       ページ HTML を生成（文言・料金はここで編集）
```

## 更新方法

```sh
# 画像を作り直す場合（旧サイトのリポジトリを指定）
python3 tools/images.py ../maimy_photo   # Pillow が必要

# HTML を再生成
python3 tools/build.py
```

料金やプラン内容は `tools/build.py` の `PLANS` を編集して再生成してください。
