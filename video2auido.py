import os
import subprocess
video_folder = "movie"
audio_folder = "audio"
text_folder = "text"

# Create output directories if they don't exist
os.makedirs(audio_folder, exist_ok=True)
os.makedirs(text_folder, exist_ok=True)

def convert_with_ffmpeg(input_path, output_path):
    """Convert video to audio using ffmpeg directly"""
    try:
        subprocess.run([
            'ffmpeg', 
            '-i', input_path,
            '-vn',  # No video
            '-acodec', 'libmp3lame',  # MP3 codec
            '-ab', '192k',  # Audio bitrate
            '-ar', '44100',  # Audio sample rate
            '-y',  # Overwrite output file
            output_path
        ], check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg error: {e.stderr}")
        return False
    except FileNotFoundError:
        print("FFmpeg not found. Please install ffmpeg.")
        return False

# Scan video_folder and create mp3 files
for filename in os.listdir(video_folder):
    print(f"{filename=}")
    if filename.lower().endswith(".mov"):
        video_path = os.path.join(video_folder, filename)
        
        # Remove .mov extension and add .mp3
        audio_filename = os.path.splitext(filename)[0] + ".mp3"
        output_audio_path = os.path.join(audio_folder, audio_filename)
        
        print(f"Converting {filename} to {audio_filename}...")
        
        if convert_with_ffmpeg(video_path, output_audio_path):
            print(f"✓ Created {output_audio_path}")
        else:
            print(f"✗ Failed to convert {filename}")
            continue