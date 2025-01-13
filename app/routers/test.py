import cv2

# OpenCV 버전 출력
print("OpenCV Version:", cv2.__version__)

# 간단한 이미지 생성 및 저장 테스트
img = cv2.imread("app/routers/01010(O).png")  # example.jpg 대신 임의의 이미지 파일 경로
if img is None:
    print("이미지를 불러올 수 없습니다. 경로를 확인하세요.")
else:
    cv2.imwrite("output.jpg", img)
    print("이미지를 성공적으로 저장했습니다: output.jpg")