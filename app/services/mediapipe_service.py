import cv2
import mediapipe as mp
import numpy as np

# Mediapipe 초기화
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.8)
mp_drawing = mp.solutions.drawing_utils

def get_finger_status(landmarks):
    """
    손가락 상태를 Mediapipe 랜드마크로 분석.
    """
    finger_status = []
    finger_tips = [4, 8, 12, 16, 20]

    for tip in finger_tips:
        hand_center_x = (landmarks[0].x + landmarks[9].x) / 2  # 손바닥 중심 X 좌표
        # hand_center_y = (landmarks[0].y + landmarks[9].y) / 2  # 손바닥 중심 Y 좌표

        if tip == 4:
            if landmarks[4].y < landmarks[3].y:  # 엄지 끝이 엄지 관절(3)보다 위에 있는지 확인
                
                # 디버깅 코드
                # print(f"landmarks[4].x = {landmarks[4].x}, hand_center_x = {hand_center_x}")
                
                if landmarks[4].x > hand_center_x:  # 손바닥 중심 기준 오른쪽이면 접힘
                    finger_status.append(0)
                else:
                    if landmarks[4].x > landmarks[3].x: 
                        finger_status.append(0)  # 엄지 끝이 엄지 중간(3)보다 오른쪽이면 접힘
                    else:
                        finger_status.append(1) # 아니면 펴짐
            else:
                finger_status.append(0) # 엄지 끝이 엄지 관절(3)보다 아래에 있으면 접힘
            continue

        if landmarks[tip].y < landmarks[tip - 2].y:  
            finger_status.append(1) # 엄지 제외 손가락 끝이 마디 중간보다 위에 있으면 펴짐
        else:
            finger_status.append(0) # 아니면 접힘

    return finger_status # 채워넣은 finger_status 배열 반환

def analyze_image(image_path: str, requested_hand_shape: list):
    """
    업로드된 이미지를 분석하여 결과를 반환.
    """
    image = cv2.imread(image_path) # 이미지 읽기 & 실패 시 예외 처리
    if image is None:
        raise ValueError("이미지 로드 실패")

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # BGR 이미지를 RGB로 변환
    results = hands.process(image_rgb) # Mediapipe로 이미지 처리

    if results.multi_hand_landmarks: # 손이 감지된 경우
        for hand_landmarks in results.multi_hand_landmarks:
            # 손가락 상태 추출
            finger_status = get_finger_status(hand_landmarks.landmark)
            
            # 결과 비교
            if finger_status == requested_hand_shape:
                return {"match": True, "message": "손 모양이 요청한 모양과 일치합니다."}
            else:
                return {"match": False, "message": "손 모양이 요청한 모양과 다릅니다."}

    return {"match": False, "message": "손이 감지되지 않았습니다."} # 손이 감지되지 않은 경우