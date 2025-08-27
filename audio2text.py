import os
import whisper

model = whisper.load_model("turbo")

video_folder = "movie"
audio_folder = "audio"
text_folder  = "text"

# video_folderを走査してmp3ファイルを作成する
# for filename in os.listdir(video_folder):
#     # mp4, mkv
#     if filename.endswith(".mov"):
#         video_path = os.path.join(video_folder, filename)
#         video = VideoFileClip(video_path)
#         output_audio_path = os.path.join(audio_folder, filename + ".mp3")
#         video.audio.write_audiofile(output_audio_path)

# audio_folderを走査してtextファイルを作成する
for filename in os.listdir(audio_folder):
    if filename.endswith(".mp3"):
        output_audio_path = os.path.join(audio_folder, filename)
        result = model.transcribe(output_audio_path)

        output_text_path = os.path.join(text_folder, filename + ".txt")
        # result をテキストファイルとして保存する
        with open(output_text_path, "w") as f:
            # f.write(result["text"])
            for i in result['segments']:
                f.write(f"[Time {i['start']} --> {i['end']}]")
                f.write(i["text"])
                f.write("\n")