from pydub import AudioSegment
from openai import OpenAI
import os
from dotenv import load_dotenv
import os, shutil, subprocess, uuid

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

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "../routers/uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

def extract_audio_from_video(video_path: str, audio_path: str):
    command = [
        "ffmpeg", "-i", video_path,
        "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
        audio_path, "-y"
    ]
    subprocess.run(command, check=True)

def process_stt_from_video(video_chunk_file) -> str:
    unique_id = str(uuid.uuid4())
    video_path = os.path.join(UPLOAD_DIR, f"{unique_id}.webm")
    audio_path = os.path.join(UPLOAD_DIR, f"{unique_id}.wav")

    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(video_chunk_file, buffer)

    extract_audio_from_video(video_path, audio_path)
    from app.services.stt_service import transcribe_audio_file
    text = transcribe_audio_file(audio_path)
    return text

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

'''
# ------------------- 화자 분리 코드 (주석) -------------------
# from openai import OpenAI  # ✅ 새로운 방식
# import json
# from dotenv import load_dotenv
#
# load_dotenv()  # .env 로드
#
# # ✅ 새로운 OpenAI 클라이언트 초기화
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
#
# # 🧠 GPT에게 역할 분류 요청
# def classify_speakers_with_gpt(speaker_segments: list) -> dict:
#     dialogue = "\n".join(f"{seg['speaker']}: {seg['text']}" for seg in speaker_segments)
#
#     prompt = (
#         "다음은 화자 분리된 대화 내용입니다:\n\n"
#         f"{dialogue}\n\n"
#         "각 SPEAKER가 '면접관'인지 '지원자'인지 분류해주세요.\n"
#         "다음 형식으로 JSON으로 출력하세요:\n"
#         "{ \"SPEAKER_00\": \"면접관\", \"SPEAKER_01\": \"지원자\" }"
#     )
#
#     try:
#         response = client.chat.completions.create(
#         model="gpt-4o-mini",  # 또는 "gpt-3.5-turbo"
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0,
#         )
#         return json.loads(response.choices[0].message.content)
#     except Exception as e:
#         print("[GPT 오류]", e)
#         return {}
#
# # 🔁 같은 화자 블록 묶기
# def group_by_speaker(segments: list, speaker_map: dict) -> str:
#     result_lines = []
#     current_speaker = None
#     current_text = ""
#
#     for seg in segments:
#         spk = seg["speaker"]
#         role = speaker_map.get(spk, spk)
#         text = seg["text"].strip()
#
#         if spk != current_speaker:
#             if current_speaker is not None:
#                 result_lines.append(f"{speaker_map[current_speaker]}: {current_text.strip()}")
#             current_speaker = spk
#             current_text = text
#         else:
#             current_text += " " + text
#
#     if current_speaker and current_text:
#         result_lines.append(f"{speaker_map[current_speaker]}: {current_text.strip()}")
#
#     return "\n".join(result_lines)
#
# @router.post("/")
# async def stt_with_diarization(audio: UploadFile = File(...)):
#     input_path = os.path.join(UPLOAD_DIR, audio.filename)
#
#     with open(input_path, "wb") as buffer:
#         shutil.copyfileobj(audio.file, buffer)
#
#     try:
#         base_name = os.path.splitext(input_path)[0]
#         wav_path = base_name + ".wav"
#
#         convert_audio_to_wav(input_path, wav_path)
#         speaker_segments = transcribe_audio_file_with_speaker_labels(wav_path)
#
#         # 🧠 GPT로 화자 역할 판단
#         speaker_map = classify_speakers_with_gpt(speaker_segments)
#
#         # 📜 문장 묶기
#         result_text = group_by_speaker(speaker_segments, speaker_map)
#
#         os.remove(input_path)
#         os.remove(wav_path)
#
#         return {"result": result_text}
#
#     except Exception as e:
#         return {"error": str(e)}
# ----------------------------------------------------------