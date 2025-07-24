import cv2
import mediapipe as mp
import sys
import os
import argparse
import csv

# argparseでコマンドライン引数をパース
parser = argparse.ArgumentParser(description='MediaPipe Pose 動画処理')
parser.add_argument('--input', type=str, default='input.mp4', help='入力動画ファイルパス')
parser.add_argument('--output', type=str, default=None, help='出力動画ファイルパス')
parser.add_argument('--outputcsv', type=str, default=None, help='各フレームの2D座標を出力するフォルダパス')
args = parser.parse_args()

input_video_path = args.input
output_video_path = args.output
output_csv_dir = args.outputcsv

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
out = None
if output_video_path is not None:
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

# Mediapipe Pose ランドマークID対応表
# 0: NOSE
# 1: LEFT_EYE_INNER
# 2: LEFT_EYE
# 3: LEFT_EYE_OUTER
# 4: RIGHT_EYE_INNER
# 5: RIGHT_EYE
# 6: RIGHT_EYE_OUTER
# 7: LEFT_EAR
# 8: RIGHT_EAR
# 9: MOUTH_LEFT
# 10: MOUTH_RIGHT
# 11: LEFT_SHOULDER
# 12: RIGHT_SHOULDER
# 13: LEFT_ELBOW
# 14: RIGHT_ELBOW
# 15: LEFT_WRIST
# 16: RIGHT_WRIST
# 17: LEFT_PINKY
# 18: RIGHT_PINKY
# 19: LEFT_INDEX
# 20: RIGHT_INDEX
# 21: LEFT_THUMB
# 22: RIGHT_THUMB
# 23: LEFT_HIP
# 24: RIGHT_HIP
# 25: LEFT_KNEE
# 26: RIGHT_KNEE
# 27: LEFT_ANKLE
# 28: RIGHT_ANKLE
# 29: LEFT_HEEL
# 30: RIGHT_HEEL
# 31: LEFT_FOOT_INDEX
# 32: RIGHT_FOOT_INDEX
#
# 各CSVの1行は上記IDに対応する関節の2D座標です。
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
            # --outputcsvでフォルダパスが指定されていればCSV出力
            if output_csv_dir:
                os.makedirs(output_csv_dir, exist_ok=True)
                csv_filename = os.path.join(output_csv_dir, f"frame_{current_frame:05d}.csv")
                with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['id', 'x', 'y'])
                    for idx, landmark in enumerate(results.pose_landmarks.landmark):
                        x_pixel = landmark.x * width
                        y_pixel = landmark.y * height
                        writer.writerow([idx, x_pixel, y_pixel])

        # フレームを書き出し
        if out is not None:
            out.write(frame)

        # 進捗をコマンドラインに表示
        print(f"解析中: {current_frame}/{total_frames} フレーム", end='\r')

    cap.release()
    if out is not None:
        out.release()

if output_video_path is not None:
    print('\n出力動画ファイル:', output_video_path) 