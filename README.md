# MediapipeOnVideo

## main.exe の使い方

main.exe は、動画ファイルに対してMediaPipe Poseを用いた骨格推定を行い、結果を動画やCSVとして出力するツールです。

### コマンドライン引数

| 引数           | 必須 | 説明                                      | デフォルト値      |
|----------------|------|-------------------------------------------|------------------|
| --input        | 任意 | 入力動画ファイルのパス                     | input.mp4        |
| --output       | 任意 | 出力動画ファイルのパス（骨格描画付き）     | なし             |
| --outputcsv    | 任意 | 各フレームごとの2D座標CSV出力フォルダパス  | なし             |

### 実行例

1. 入力動画 input.mp4 を解析し、骨格描画付き動画 output.avi を出力する:

```
main.exe --input input.mp4 --output output.avi
```

2. 入力動画 input.mp4 を解析し、各フレームの2D座標をCSVで output_csv フォルダに出力する:

```
main.exe --input input.mp4 --outputcsv output_csv
```

3. 両方同時に出力する:

```
main.exe --input input.mp4 --output output.avi --outputcsv output_csv
```

### 出力内容
- --output を指定した場合: 骨格が描画された動画ファイルが出力されます。
- --outputcsv を指定した場合: 各フレームごとに `frame_00001.csv` のようなCSVファイルが指定フォルダに出力されます。
  - CSVの各行は `id, x, y` 形式で、MediaPipe PoseのランドマークIDと2D座標（ピクセル値）です。

### 依存パッケージ
- mediapipe
- opencv-python

### 注意事項
- 入力動画ファイルが存在しない場合、エラーとなります。
- 出力先フォルダは自動生成されます。
- main.exe は main.py をPyInstaller等でexe化したものです。
