import cv2
import mediapipe as mp
import numpy as np

from absl import logging
logging.set_verbosity(logging.ERROR)  # 오류만 출력

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # TensorFlow 경고 숨기기

# Mediapipe Hand Tracking 초기화
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# 요청된 손 모양 정의 (11011 -> [1, 1, 0, 1, 1])
requested_hand_shape = [1, 1, 0, 1, 1]

# 결과를 저장할 리스트
result_data = []

def get_finger_status(landmarks):
    """
    Mediapipe 손 랜드마크를 기반으로 손가락 상태를 계산합니다.
    펴진 손가락은 1, 접힌 손가락은 0으로 판단.
    """
    finger_status = []
    # 손목과 각 손가락 관절의 Y 좌표를 비교하여 손가락 상태 판별
    # 손가락 관절 인덱스: [4, 8, 12, 16, 20]
    finger_tips = [4, 8, 12, 16, 20]
    for tip in finger_tips:
        # 엄지를 판별하는 경우는 따로 처리 

        hand_center_x = (landmarks[0].x + landmarks[9].x) / 2  # 손바닥 중심 X 좌표
        hand_center_y = (landmarks[0].y + landmarks[9].y) / 2  # 손바닥 중심 Y 좌표

        if tip == 4:
            if landmarks[4].y < landmarks[3].y:  # 엄지 끝이 관절보다 위에 있는지 확인
                print(f"landmarks[4].x = {landmarks[4].x}, hand_center_x = {hand_center_x}")
                if landmarks[4].x > hand_center_x:  # 손바닥 중심 기준 오른쪽이면 펴짐
                    finger_status.append(0)
                else:
                    if landmarks[4].x > landmarks[3].x:  # 엄지 끝이 엄지 중간보다 오른쪽이면 펴짐
                        finger_status.append(0)
                    else:
                        finger_status.append(1)
            else:
                finger_status.append(0)
            continue

            # if landmarks[2].x > landmarks[4].x:
            #     finger_status.append(1)
            # else:
            #     finger_status.append(0)
            # continue

        if landmarks[tip].y < landmarks[tip - 2].y:  # 손가락이 펴져 있으면
            finger_status.append(1)
        else:
            finger_status.append(0)

    return finger_status

# 사용자 이미지 로드
# image_path = "/Users/dohoon/Desktop/techeer/mideapipe_test/00101.png"  # 업로드된 이미지 경로
# image = cv2.imread(image_path)
base_path = "/Users/dohoon/Desktop/techeer/mideapipe_test/img"  # 이미지 폴더 경로
for i in range(32):  # 00000부터 11111까지 파일 이름 반복
    # 파일 이름 생성 (5자리로 채움)
    filename = f"{i:05b}"  # 이진수 형식으로 파일 이름 생성

    # 파일 확장자 조건에 따라 설정
    if i <= 15:  # 00000 ~ 01111은 .png
        image_path = os.path.join(base_path, f"{filename}.png")
    else:  # 10000 ~ 11111은 .jpg
        image_path = os.path.join(base_path, f"{filename}.jpg")

    # 이미지 읽기
    image = cv2.imread(image_path)

    if image is None:
        print(f"[{filename}] 이미지를 불러올 수 없습니다. 경로를 확인하세요.")
        continue

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Mediapipe로 손 분석
    results = hands.process(image_rgb)

    if results.multi_hand_landmarks is None:
        print("손이 인식되지 않았습니다. 이미지를 확인하세요.")
        exit()

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # 손가락 상태 추출
            finger_status = get_finger_status(hand_landmarks.landmark)

            # 자동화 위한 코드
            result_data.append(f"[{filename}] 분석된 손 모양: {finger_status}")
            if finger_status == requested_hand_shape:
                result_data.append(f"[{filename}] 손 모양이 요청한 모양과 일치합니다.")
            else:
                result_data.append(f"[{filename}] 손 모양이 요청한 모양과 다릅니다.")

            # 원래 결과 비교
            # print("분석된 손 모양:", finger_status) 

            # if finger_status == requested_hand_shape:
            #     print("손 모양이 요청한 모양과 일치합니다.")
            # else:
            #     print("손 모양이 요청한 모양과 다릅니다.")

            # 손 랜드마크 그리기
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # 결과 이미지 출력
        cv2.imshow("Result", image)
        cv2.waitKey(100)
        cv2.destroyAllWindows()

# Mediapipe 리소스 해제
hands.close()

