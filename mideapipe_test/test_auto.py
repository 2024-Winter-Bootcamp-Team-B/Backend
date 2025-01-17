from test import result_data

def validate_hand_shapes(result_data):
    """
    Mediapipe 실행 결과 데이터를 받아 분석된 손 모양 배열의 순서를 검증합니다.
    """
    # 00001부터 11111까지의 예상 손 모양 배열 생성
    expected_shapes = [f"{i:05b}" for i in range(0, 32)]  # 00000~11111
    expected_shapes = [[int(bit) for bit in shape] for shape in expected_shapes]

    errors = []  # 순서가 틀린 항목을 기록할 리스트
    index = 0  # 예상 손 모양 리스트의 인덱스

    for line in result_data:
        # "분석된 손 모양"만 처리
        if "분석된 손 모양:" in line:
            # 분석된 손 모양 추출
            parts = line.split(":")[-1].strip()
            actual_shape = [int(x) for x in parts.strip("[]").split(",")]

            # 검증: 예상 손 모양과 실제 손 모양 비교
            if actual_shape != expected_shapes[index]:
                errors.append({
                    "expected": expected_shapes[index],
                    "actual": actual_shape,
                    "filename": f"{index:05b}"  # 파일 이름을 이진수 형식으로 저장
                })
            index += 1

            # 모든 손 모양 검증 완료 시 종료
            if index >= len(expected_shapes):
                break

    # 결과 출력
    if not errors:
        print("모든 손 모양 배열이 올바른 순서로 정렬되어 있습니다!")
    else:
        print("다음 손 모양 배열에서 순서가 틀렸습니다:")
        for error in errors:
            print(f"파일 {error['filename']}: 예상 모양 {error['expected']} / 실제 모양 {error['actual']}")

# # Mediapipe 결과 데이터 (예시: result_data 리스트)
# result_data = [
#     "[00000] 이미지를 불러올 수 없습니다. 경로를 확인하세요.",
#     "[00001] 분석된 손 모양: [0, 0, 0, 0, 1]",
#     "[00001] 손 모양이 요청한 모양과 다릅니다.",
#     "[00010] 분석된 손 모양: [0, 0, 0, 1, 0]",
#     "[00010] 손 모양이 요청한 모양과 다릅니다.",
#     "[00011] 분석된 손 모양: [0, 0, 0, 1, 1]",
#     "[00011] 손 모양이 요청한 모양과 다릅니다.",
#     "[11111] 분석된 손 모양: [1, 1, 1, 1, 1]",
#     "[11111] 손 모양이 요청한 모양과 다릅니다.",
# ]

# 자동화 코드 실행
validate_hand_shapes(result_data)