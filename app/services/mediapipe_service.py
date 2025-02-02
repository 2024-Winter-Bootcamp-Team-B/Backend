import cv2 
import mediapipe as mp
import numpy as np

# Mediapipe 초기화
mp_hands = mp.solutions.hands
# hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.8, model_complexity=0)  # GPU 비활성화 추가
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

    print(f"Starting analysis for file: {image_path}")  # 로그 추가

    image = cv2.imread(image_path) # 이미지 읽기 & 실패 시 예외 처리
    if image is None:
        raise ValueError("이미지 로드 실패")

    # 이미지 크기 확인
    if image.size == 0:
        raise ValueError("이미지 크기가 0입니다. 손상된 파일일 수 있습니다.")

    # BGR -> RGB 변환
    try:
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        print("이미지 RGB 변환 성공")
    except Exception as e:
        raise ValueError(f"이미지 RGB 변환 실패: {str(e)}")
    
    # try:
    #     print("mediapipe로 이미지 처리 전")  # 디버깅용 로그 추가
    #     print(f"Starting Mediapipe process for file: {image_path}")  # 로그 추가
    #     print(image_rgb.shape)  # (높이, 너비, 3) 형태로 출력되어야 함
    #     results = hands.process(image_rgb) # Mediapipe로 이미지 처리
    #     print("mediapipe로 이미지 처리 후")  # 디버깅용 로그 추가
    # except Exception as e:
    #     raise ValueError(f"Mediapipe 이미지 처리 실패: {str(e)}")
    
        # Hands 객체 동적 생성
    with mp.solutions.hands.Hands(
        static_image_mode=True, 
        max_num_hands=1, 
        min_detection_confidence=0.8
    ) as hands:
        print("mediapipe로 이미지 처리 전")
        print(f"Starting Mediapipe process for file: {image_path}")  # 로그 추가
        results = hands.process(image_rgb)
        print("mediapipe로 이미지 처리 후")


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