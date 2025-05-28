from pydub import AudioSegment
from openai import OpenAI
import os
from dotenv import load_dotenv

# 📦 .env 환경 변수 로드
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path)

# 🔑 OpenAI API Key 로드 및 클라이언트 초기화
openai_key = os.getenv("OPENAI_API_KEY")
if not openai_key:
    raise ValueError("❌ OPENAI_API_KEY가 .env에 정의되지 않았습니다.")
client = OpenAI(api_key=openai_key)

# 🔄 오디오 포맷을 Whisper API 호환 wav로 변환
def convert_audio_to_wav(input_path: str, output_path: str):
    """
    입력 오디오 파일을 16kHz, mono wav 형식으로 변환
    """
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_frame_rate(16000).set_channels(1)
    audio.export(output_path, format="wav")

# 🧠 OpenAI Whisper API를 통한 STT 수행
def transcribe_audio_file(file_path: str) -> str:
    """
    Whisper API를 사용하여 주어진 오디오 파일을 텍스트로 전사함
    """
    with open(file_path, "rb") as f:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            response_format="text"  # 또는 "json"
        )
    return transcript.strip()

# from pydub import AudioSegment
# import whisper
# from pyannote.audio import Pipeline
# import os
# from dotenv import load_dotenv
#
# # Whisper 모델 로드
# model = whisper.load_model("small")
#
# # 환경 변수 로드
# dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
# #load_dotenv()
# load_dotenv(dotenv_path)
# HUGGINGFACE_TOKEN = os.getenv("HF_TOKEN")
# print(f"HUGGINGFACE_TOKEN: {HUGGINGFACE_TOKEN[:8]}..." if HUGGINGFACE_TOKEN else "❌ 환경 변수 로드 실패")
#
# # pyannote 화자 분리 파이프라인
# diarization_pipeline = Pipeline.from_pretrained(
#     "pyannote/speaker-diarization",
#     use_auth_token=HUGGINGFACE_TOKEN
# )
#
# def convert_webm_to_wav(webm_path, wav_path):
#     audio = AudioSegment.from_file(webm_path, format="webm")
#     audio.export(wav_path, format="wav")
# # 오디오 변환 (확장자 무관)
# def convert_audio_to_wav(input_path: str, output_path: str):
#     audio = AudioSegment.from_file(input_path)
#     audio = audio.set_frame_rate(16000).set_channels(1)  # 샘플레이트 및 채널 설정
#     audio.export(output_path, format="wav")
#
# # Whisper 단순 전사
# def transcribe_audio_file(file_path: str) -> str:
#     result = model.transcribe(file_path)
#     return result["text"]
#
# # Whisper + pyannote 화자 분리 전사
# def transcribe_audio_file_with_speaker_labels(wav_path: str) -> list:
#     diarization = diarization_pipeline(wav_path)
#     result = model.transcribe(wav_path, verbose=False)
#
#     segments = []
#     for turn in diarization.itertracks(yield_label=True):
#         start, end = turn[0].start, turn[0].end
#         speaker = turn[2]
#         spoken_texts = [
#             seg['text'] for seg in result['segments']
#             if not (seg['end'] < start or seg['start'] > end)
#         ]
#         combined = ' '.join(spoken_texts).strip()
#         if combined:
#             segments.append({
#                 "speaker": speaker,
#                 "start": round(start, 1),
#                 "end": round(end, 1),
#                 "text": combined
#             })
#     return segments