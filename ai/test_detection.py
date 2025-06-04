# test_detection.py

import time
from threading import Event

# 모듈 경로는 자신의 프로젝트 구조에 맞게 조정하세요.
from app.services.interview.mediapipe_service import mouth_open_state, VideoStreamer
from app.services.interview.recorder_service import CombinedAudioRecorder

# 0) 매우 짧게 출력하기 위한 헬퍼 함수
def print_state(mouth_state, speaker):
    print(f"[{time.strftime('%H:%M:%S')}] mouth_open_state = {mouth_state}, detected speaker = {speaker}")

# 1) CombinedAudioRecorder용 간단한 callback
def test_callback(speaker_tag, wav_bytes):
    # 실제 STT 대신, 세그먼트가 끝날 때마다 화자 태그만 출력
    print(f"[{time.strftime('%H:%M:%S')}] *** SEGMENT END → speaker = {speaker_tag}, bytes={len(wav_bytes)}")

if __name__ == "__main__":
    # 2) VideoStreamer(입열림 감지)와 CombinedAudioRecorder(화자 분리) 초기화
    video = VideoStreamer(camera_index=0)
    audio = CombinedAudioRecorder(
        samplerate=16000,
        channels=1,
        callback=test_callback
    )

    try:
        print("▶️ 비디오 스트리머 시작 중...")
        video.start()
        print("▶️ 오디오 녹음기(CombinedAudioRecorder) 시작 중...")
        audio.start()

        print("┌────────────────────────────────────────┐")
        print("│  테스트 시작: 입을 벌리면 Applicant     │")
        print("│  입을 닫고 말하면 Interviewer로 인식됨 │")
        print("│  종료하려면 Ctrl+C                       │")
        print("└────────────────────────────────────────┘\n")

        # 3) 메인 루프: 주기적으로 mouth_open_state 출력
        while True:
            # mouth_open_state는 [왼쪽 지원자, 오른쪽 지원자]
            # 예: [True, False]면 왼쪽 지원자 말 중, [False, False] & 음량 높으면 면접관
            current_mouth = mouth_open_state.copy()
            # speaker 정보는 CombinedAudioRecorder 내부에서 test_callback 으로 출력됨
            print_state(current_mouth, speaker="(speech segments는 callback에서 출력)")

            time.sleep(1.0)

    except KeyboardInterrupt:
        print("\n🛑 테스트 종료 요청 감지 → 스트리머/녹음기 중단 중...")

    finally:
        # 4) 리소스 해제
        audio.stop()
        video.stop()
        print("✅ 모든 스트리머가 중단되었습니다. 프로그램 종료.")
