import mediapipe as mp
import math, time
import cv2 as cv
from mediapipe.tasks.python import vision
from mediapipe.tasks import python as mp_python

from visualization import draw_manual, print_RSP_result


## 필요한 함수 작성

MODEL_PATH = "hand_landmarker.task"

FINGERS = {
    'INDEX_FINGER': (8, 6),
    'MIDDLE_FINGER': (12, 10),
    'RING_FINGER': (16, 14),
    'PINKY': (20, 18),
}

ROCK, PAPER, SCISSORS = 0, 1, 2


def is_open(lm, tip, pip):
    wrist = lm[0]
    tip_distance = math.hypot(lm[tip].x - wrist.x, lm[tip].y - wrist.y)
    pip_distance = math.hypot(lm[pip].x - wrist.x, lm[pip].y - wrist.y)
    
    return tip_distance > pip_distance # tip_distance가 더 크면 쫙 핀 것 . . !! 

if __name__ == "__main__":
    # 실행 로직
    options = vision.HandLandmarkerOptions(
        base_options=mp_python.BaseOptions(model_asset_path=MODEL_PATH),
        running_mode=vision.RunningMode.VIDEO,
        num_hands=1,
    )
    
    # 손을 인식할 도구, 루프 바깥에 딱 한 번 써놓으면 됨
    landmarker = vision.HandLandmarker.create_from_options(options)
    
    # 카메라, 루프 바깥에 딱 한 번 써놓으면 됨
    cap = cv.VideoCapture(0)
    start_time = time.time()
    
    # 계속 움직이는 손을 봐야 하기 때문에 멈출 때까지 무한 루프
    while True:
        # 카메라가 순간 한 장을 찍어서 ret에는 성공 여부 T/F, frame에는 찍힌 데이터
        ret, frame = cap.read()
        # ret이 false이면 while문 나가기
        if not ret:
            break
        
        # 기본적으로 이미지가 반대로 나오기 때문에 좌우로 뒤집기 
        frame = cv.flip(frame, 1)
        # openCV의 색상 형식은 BGR이므로 RGB로 바꾸기
        rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        # MediaPipe 형식에 맞춰 rgb 값을 넘겨줌
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        # 지금 시간 - 시작한 시간을 ms로 바꿔 ts에 저장
        ts = int((time.time() - start_time) * 1000)
        # landmarker 모델에게 mp_image와 ts를 넘겨 손을 인식하고, 좌표를 result에 저장
        result = landmarker.detect_for_video(mp_image, ts)
        
        # 좌표를 점과 선으로 그리는 visualization.py의 draw_manual() 함수 사용
        # 찍은 사진 frame이랑 좌표 result을 같이 넣으면 인식 선을 그려서 frame에 저장
        frame = draw_manual(frame, result)
        
        # rps는 판별 결과를 담을 변수
        rps = None
        
        # 손이 보이면 아래를 실행
        if result.hand_landmarks:
            # lm에 좌표 리스트 담기
            lm = result.hand_landmarks[0]
            
            # open_state는 손가락별 결과를 담을 딕셔너리
            open_state = {}
            
            # 손가락을 하나씩 돌아가면서 판별해서 open_state에 저장
            for name, (tip, pip) in FINGERS.items():
                open_state[name] = is_open(lm, tip, pip)
            
            # 펴진 손가락은 1, 접힌 손가락은 0으로 계산되어 그 합이 count에 저장됨
            count = sum(open_state.values())
            
            # 주먹
            if count == 0:
                rps = ROCK
            # 보
            elif count == 4:
                rps = PAPER
            # 가위
            elif open_state['INDEX_FINGER'] and open_state['MIDDLE_FINGER'] and count == 2:
                rps = SCISSORS
                
        # 선이 그려진 사진 frame과 rps로 최종 결과물을 만들어 frame에 저장
        frame = print_RSP_result(frame, rps)
        cv.imshow("Rock Paper Scissors", frame)
        
        # q 누르면 루프 끝
        if cv.waitKey(1) == ord("q"):
            break
        
    # 카메라 반납하기
    cap.release()
    # openCV 닫기
    cv.destroyAllWindows()
    # landmarker 해제
    landmarker.close()
