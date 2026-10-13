import whisper
import subprocess
import os

def embed_subtitles(workdir, input_video, subtitle_file, output_video):
    """
    使用 FFmpeg 將字幕硬嵌入影片
    """
    # # 確保路徑是絕對路徑並且正確使用斜槓
    # input_video = os.path.abspath(input_video).replace("\\", "/")
    # subtitle_file = os.path.abspath(subtitle_file).replace("\\", "/")
    # output_video = os.path.abspath(output_video).replace("\\", "/")
    #
    # # 檢查檔案是否存在
    # if not os.path.exists(input_video):
    #     raise FileNotFoundError(f"影片檔案不存在: {input_video}")
    # if not os.path.exists(subtitle_file):
    #     raise FileNotFoundError(f"字幕檔案不存在: {subtitle_file}")

    try:
        # FFmpeg 命令 (將字幕路徑用雙引號包起來)
        ffmpeg_cmd = [
            "ffmpeg",
            "-i", input_video,                                 # 輸入影片
            "-vf", f"subtitles='{subtitle_file}'",             # 加入字幕濾鏡
            output_video                                       # 輸出檔案
        ]
        print("正在燒錄字幕...")

        # 執行 FFmpeg 命令
        result = subprocess.run(ffmpeg_cmd, check=True, stderr=subprocess.PIPE, text=True, cwd=workdir)

        print(f"字幕已燒錄完成！輸出檔案：{output_video}")
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg 執行失敗！錯誤訊息：\n{e.stderr}")
    except Exception as e:
        print(f"發生其他錯誤: {e}")

def video_to_subtitle(video_path: str, subtitle_path: str):
    audio_path = subtitle_path + ".mp3"
    extract_audio(video_path, audio_path)
    transcribe_audio(audio_path, subtitle_path)

def extract_audio(video_path, audio_path):
    """
    從影片中提取音訊並儲存為 MP3 格式。
    """
    command = ["ffmpeg", "-y", "-i", video_path, "-q:a", "0", "-map", "a", audio_path]
    subprocess.run(command, check=True)
    print(f"已提取音訊到: {audio_path}")

def transcribe_audio(audio_path, subtitle_path):
    """
    使用 Whisper 模型轉錄音訊並儲存為 SRT 格式。
    """
    print("正在載入 Whisper 模型...")
    model = whisper.load_model("base")  # 可選 "tiny", "base", "small", "medium", "large"
    print("模型載入完成，開始轉錄...")

    result = model.transcribe(audio_path)
    print("轉錄完成，正在儲存字幕檔案...")

    # 儲存 SRT 格式字幕
    with open(subtitle_path, "w", encoding="utf-8") as srt_file:
        for i, segment in enumerate(result["segments"]):
            start = format_timestamp(segment["start"])
            end = format_timestamp(segment["end"])
            text = segment["text"].strip()
            srt_file.write(f"{i + 1}\n{start} --> {end}\n{text}\n\n")

    print(f"字幕檔案已儲存至: {subtitle_path}")

def format_timestamp(seconds):
    """
    格式化時間戳為 SRT 標準格式：hh:mm:ss,ms
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"
