import cv2
import mediapipe as mp
import numpy as np

from absl import logging
logging.set_verbosity(logging.ERROR)  # 오류만 출력

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # TensorFlow 경고 숨기기

# Mediapipe Hand Tracking 초기화
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.8)
mp_drawing = mp.solutions.drawing_utils

# 요청된 손 모양 정의 (11011 -> [1, 1, 0, 1, 1])
requested_hand_shape = [1, 1, 0, 1, 1]

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
        # if tip == 4:
        #     print(f"엄지: landmarks[4].y = {landmarks[4].y}, landmarks[3].y = {landmarks[3].y}")
        #     print(f"엄지: landmarks[4].x = {landmarks[4].x}, landmarks[3].x = {landmarks[3].x}")

        #     if landmarks[4].y < landmarks[3].y:
        #         finger_status.append(0)
        #     else:
        #         if landmarks[4].x < landmarks[3].x:
        #             finger_status.append(0)
        #         else:
        #             finger_status.append(1)
        #     continue

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

        if landmarks[tip].y < landmarks[tip - 2].y:  # 손가락이 펴져 있으면
            finger_status.append(1)
        else:
            finger_status.append(0)

    return finger_status

# 사용자 이미지 로드
image_path = "/Users/dohoon/Desktop/techeer/mideapipe_test/img/01010.png"  # 업로드된 이미지 경로
image = cv2.imread(image_path)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Mediapipe로 손 분석
results = hands.process(image_rgb)

if results.multi_hand_landmarks:
    for hand_landmarks in results.multi_hand_landmarks:
        # 손가락 상태 추출
        finger_status = get_finger_status(hand_landmarks.landmark)

        # 결과 비교
        print("분석된 손 모양:", finger_status) 

        if finger_status == requested_hand_shape:
            print("손 모양이 요청한 모양과 일치합니다.")
        else:
            print("손 모양이 요청한 모양과 다릅니다.")

        # 손 랜드마크 그리기
        mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

# 결과 이미지 출력
cv2.imshow("Result", image)
cv2.waitKey(10000)
cv2.destroyAllWindows()

# Mediapipe 리소스 해제
hands.close()


# import cv2
# import mediapipe as mp
# import numpy as np
# from absl import logging
# import os

# # Mediapipe 초기화
# logging.set_verbosity(logging.ERROR)  # Mediapipe 로그 최소화
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # TensorFlow 경고 숨기기

# # Mediapipe Hand Tracking 초기화
# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.5)
# mp_drawing = mp.solutions.drawing_utils

# # 요청된 손 모양 정의
# requested_hand_shape = [1, 1, 0, 1, 1]

# def remove_background(image):
#     """
#     배경 제거를 통해 손을 더 명확히 인식하도록 조정.
#     """
#     # 배경 제거 모델 초기화
#     fgbg = cv2.createBackgroundSubtractorMOG2()

#     # 배경 제거 적용
#     fgmask = fgbg.apply(image)

#     # 팽창 및 침식 연산으로 잡음 제거
#     kernel = np.ones((5, 5), np.uint8)
#     cleaned = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)

#     return cleaned

# def preprocess_image_for_shadow(image):
#     """
#     입력 이미지를 전처리하여 Mediapipe가 손을 더 잘 인식할 수 있도록 조정.
#     """
#     # 1. 대비 조정 (손과 배경을 더 명확히 구분)
#     adjusted = cv2.convertScaleAbs(image, alpha=1.8, beta=40)

#     # 2. 그레이스케일 변환
#     gray = cv2.cvtColor(adjusted, cv2.COLOR_BGR2GRAY)

#     # 3. 적응형 이진화 (손과 배경 분리)
#     binary = cv2.adaptiveThreshold(
#         gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#         cv2.THRESH_BINARY_INV, blockSize=15, C=5
#     )

#     # 4. 모폴로지 연산 (잡음 제거)
#     kernel = np.ones((5, 5), np.uint8)
#     morphed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

#     # 5. RGB 변환
#     processed_image = cv2.cvtColor(morphed, cv2.COLOR_GRAY2RGB)

#     return processed_image

# def get_finger_status(landmarks):
#     """
#     Mediapipe 손 랜드마크를 기반으로 손가락 상태를 계산합니다.
#     """
#     finger_status = []
#     finger_tips = [4, 8, 12, 16, 20]

#     for tip in finger_tips:
#         if tip == 4:  # 엄지 판별
#             if landmarks[4].y < landmarks[3].y and landmarks[4].x < landmarks[3].x:
#                 finger_status.append(1)  # 엄지가 펴진 상태
#             else:
#                 finger_status.append(0)  # 엄지가 접힌 상태
#             continue

#         if landmarks[tip].y < landmarks[tip - 2].y:  # 손가락이 펴진 상태
#             finger_status.append(1)
#         else:
#             finger_status.append(0)  # 손가락이 접힌 상태

#     return finger_status

# # 사용자 이미지 로드
# image_path = "/Users/dohoon/Desktop/techeer/mideapipe_test/img/01010.png"  # 업로드된 이미지 경로
# image = cv2.imread(image_path)

# if image is None:
#     print(f"이미지를 불러올 수 없습니다. 경로를 확인하세요: {image_path}")
#     exit()

# # Mediapipe로 손 분석
# results = hands.process(preprocess_image_for_shadow)

# if results.multi_hand_landmarks is None:
#     print("손이 인식되지 않았습니다. 이미지를 확인하세요.")
#     exit()
# else:
#     print("손이 성공적으로 인식되었습니다.")

# if results.multi_hand_landmarks:
#     for hand_landmarks in results.multi_hand_landmarks:
#         # 손가락 상태 추출
#         finger_status = get_finger_status(hand_landmarks.landmark)

#         # 결과 비교
#         print("분석된 손 모양:", finger_status)

#         if finger_status == requested_hand_shape:
#             print("손 모양이 요청한 모양과 일치합니다.")
#         else:
#             print("손 모양이 요청한 모양과 다릅니다.")

#         # 손 랜드마크 그리기
#         mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

# # 결과 이미지 출력
# cv2.imshow("Result", image)
# cv2.waitKey(10000)
# cv2.destroyAllWindows()

# # Mediapipe 리소스 해제
# hands.close()