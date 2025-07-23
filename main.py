import cv2
import mediapipe as mp
import sys
import os
import argparse

# argparseでコマンドライン引数をパース
parser = argparse.ArgumentParser(description='MediaPipe Pose 動画処理')
parser.add_argument('--input', type=str, default='input.mp4', help='入力動画ファイルパス')
parser.add_argument('--output', type=str, default='output.avi', help='出力動画ファイルパス')
args = parser.parse_args()

input_video_path = args.input
output_video_path = args.output

# 入力ファイルの存在確認
if not os.path.exists(input_video_path):
    print(f"エラー: 入力ファイルが存在しません: {input_video_path}")
    sys.exit(1)

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# 動画ファイルを開く
cap = cv2.VideoCapture(input_video_path)

# capが開けているか確認
if not cap.isOpened():
    print(f"エラー: 動画ファイルを開けません: {input_video_path}")
    sys.exit(1)

# 動画のプロパティ取得
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # 総フレーム数を取得

# 出力動画の設定（avi, MJPGコーデック）
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

with mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    enable_segmentation=False,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as pose:
    current_frame = 0  # 現在のフレーム数
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        current_frame += 1

        # BGR→RGB
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # 推論
        results = pose.process(image_rgb)

        # ボーンを描画
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=2),
                connection_drawing_spec=mp_drawing.DrawingSpec(color=(0,0,255), thickness=2, circle_radius=2)
            )

        # フレームを書き出し
        out.write(frame)

        # 進捗をコマンドラインに表示
        print(f"解析中: {current_frame}/{total_frames} フレーム", end='\r')

    cap.release()
    out.release()

print('\n出力動画ファイル:', output_video_path) 