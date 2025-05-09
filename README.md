# 姿勢のゆがみチェックアプリ

このアプリは、アップロードされた全身写真から姿勢のゆがみ（肩や骨盤の左右差）をMediaPipeを使って検出し、結果を可視化します。

## 使用技術

- Streamlit（Webフロント）
- MediaPipe（姿勢推定）
- OpenCV（画像処理）
- Pillow（画像操作）

## 使い方

1. 全身写真をアップロード
2. 姿勢ランドマークが表示され、ゆがみ判定が返ります

## ローカル実行

```bash
pip install -r requirements.txt
streamlit run app.py
