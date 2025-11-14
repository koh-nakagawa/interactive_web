# README_JPN

## Interactive Web Project  
音入力に反応して中央から円が広がるビジュアルを生成し  
実際のクモ網へ投影するためのインタラクティブアートシステムです  
Python で音処理と合成低音を生成し  
Processing で視覚エフェクトを描画します

---

## 特徴

* 任意のマイク入力をリアルタイムに取得  
* 入力音から低音成分を抽出  
* ハウリング防止のため合成低音のみを出力  
* Processing へ OSC で低音値を送信  
* 低音に合わせて円が中央から外に広がるビジュアル  
* マイクごとに異なる特性に対応するため閾値をコマンドで調整可能  
* 入出力デバイスもコマンドラインで指定可能  

---

## システム概要

このプロジェクトは以下の二つのコンポーネントから構成されます。

### Python Audio Engine  
* マイクから音を取得  
* FFT により低音成分を抽出  
* 合成低音（八十ヘルツ）を生成して出力  
* 処理した低音値を Processing に OSC 送信  
* 起動時にデバイス番号と閾値を指定可能  

### Processing Visual Engine  
* OSC で bass 値を受信  
* bass が閾値を超えるたびに円が生成  
* 円は一定速度で外に広がり、画面外で消滅  
* 同時に複数の円を描画  
* 黒背景に白い円のためプロジェクションに最適  

---

## 必要環境

* macOS Apple Silicon 推奨  
* Python 三系  
* Processing 四系  
* PyAudio、NumPy、python OSC  
* USB マイクまたは内蔵マイク  
* 内蔵スピーカーまたは外部スピーカー  

---

## ディレクトリ構成

```
interactive_web
  device.py
  audio_engine.py
  requirements.txt
  processing
    interactive_web.pde
```

---

## インストール手順

### conda 環境の作成

```
conda create -n interactive_web python=3.11
conda activate interactive_web
```

### 必要ライブラリのインストール

```
pip install -r requirements.txt
```

---

## オーディオデバイスの確認

入出力デバイスの一覧を取得するには

```
python device.py
```

例

```
0  内蔵マイク      IN 1  OUT 0
1  内蔵スピーカー  IN 0  OUT 2
```

---

## Audio Engine の実行

### 実行構文

```
python audio_engine.py --input 入力デバイス番号 --output 出力デバイス番号 --threshold 閾値
```

### 例

```
python audio_engine.py --input 0 --output 1 --threshold 0.002
```

---

## Processing の設定

### スケッチの起動

1. Processing を起動  
2. `interactive_web/processing` を開く  
3. `interactive_web.pde` を実行  

Processing はポート五千五で OSC を受信します。

---

## ビジュアルの動作

* 通常は黒背景  
* bass が閾値を超えると中央に円が生成  
* 円は一定速度で広がる  
* 画面外に出ると自動で消える  
* 音が連続すると複数同時に円が存在  

クモ網への投影で「振動の波紋」を表現できます。

---

## ハウリング防止について

本システムは  
マイク音を直接出力する方式を使わず  
合成低音のみをスピーカーから出すことで  
物理的にハウリングを防ぎます。

---

## トラブルシューティング

### 円が出ない  
* threshold を下げる  
* audio_engine.py が起動しているか確認  
* OSC ポート五千五が競合していないか確認  

### 常に円が出続ける  
* threshold を上げる  
* マイク感度を下げる  

### 音が出ない  
* 出力デバイス番号が正しいか確認  
* macOS のサウンド設定を確認  

---

## ライセンス

MIT License（必要に応じて変更可能）
