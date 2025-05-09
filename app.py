import streamlit as st
import cv2
import numpy as np
import mediapipe as mp
from PIL import Image

# Poseモデル初期化
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True)
mp_drawing = mp.solutions.drawing_utils

def detect_pose(image):
    img_rgb = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    results = pose.process(img_rgb)
    return results.pose_landmarks if results.pose_landmarks else None

def calculate_posture_score(landmarks):
    if not landmarks:
        return "姿勢を検出できませんでした。"

    left_shoulder = landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
    right_shoulder = landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
    left_hip = landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
    right_hip = landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP]

    shoulder_diff = abs(left_shoulder.y - right_shoulder.y)
    hip_diff = abs(left_hip.y - right_hip.y)

    threshold = 0.03
    issues = []
    if shoulder_diff > threshold:
        issues.append("肩の高さにゆがみがあります。")
    if hip_diff > threshold:
        issues.append("骨盤の高さにゆがみがあります。")

    return " ".join(issues) if issues else "姿勢はおおむね正常です。"

def draw_landmarks(image, landmarks):
    annotated = image.copy()
    mp_drawing.draw_landmarks(
        annotated,
        landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0,255,0), thickness=2),
        connection_drawing_spec=mp_drawing.DrawingSpec(color=(255,0,0), thickness=2),
    )
    return annotated

# StreamlitアプリUI
st.title("📸 姿勢のゆがみチェックアプリ")
uploaded_file = st.file_uploader("全身写真をアップロードしてください（JPG/PNG）", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="アップロード画像", use_column_width=True)

    with st.spinner("姿勢を解析中..."):
        landmarks = detect_pose(image)
        result_text = calculate_posture_score(landmarks)
        st.success("解析完了")
        st.markdown(f"**📝 結果:** {result_text}")

        if landmarks:
            result_img = draw_landmarks(np.array(image), landmarks)
            st.image(result_img, caption="姿勢ランドマーク", channels="RGB")
