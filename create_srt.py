import re
from glob import glob
from pathlib import Path

def to_srt_time(total_seconds):
    """Converts seconds to SRT time format HH:MM:SS,ms."""
    # Calculate hours, minutes, seconds, and milliseconds
    hours = int(total_seconds / 3600)
    minutes = int((total_seconds % 3600) / 60)
    seconds = int(total_seconds % 60)
    milliseconds = int((total_seconds - int(total_seconds)) * 1000)
    
    # Format and return the time string
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

def create_srt_from_transcription(input_file, output_file):
    """
    Reads a transcription file and converts it to an SRT subtitle file.
    
    Expected input format: [Time START --> END]Subtitle text
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f_in, \
             open(output_file, 'w', encoding='utf-8') as f_out:
            
            subtitle_index = 1
            for line in f_in:
                # Use regex to find timestamps and text
                match = re.search(r"\[Time (\d+\.?\d*) --> (\d+\.?\d*)\](.*)", line)
                
                if match:
                    start_time_sec = float(match.group(1))
                    end_time_sec = float(match.group(2))
                    text = match.group(3).strip()
                    
                    # Convert seconds to SRT time format
                    start_srt = to_srt_time(start_time_sec)
                    end_srt = to_srt_time(end_time_sec)
                    
                    # Write the SRT block
                    f_out.write(f"{subtitle_index}\n")
                    f_out.write(f"{start_srt} --> {end_srt}\n")
                    f_out.write(f"{text}\n\n")
                    
                    subtitle_index += 1
            
            print(f"Successfully created '{output_file}' with {subtitle_index - 1} entries.")

    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# --- How to use it ---
# 1. Save your transcription text into a file named 'transcription.txt'.
# 2. Run this script. It will generate a file named 'subtitles.srt'.
# 3. `ffmpeg -i my_video.mp4 -i subtitles.srt -c copy -c:s mov_text output_video.mp4`
if __name__ == '__main__':
    for fn in glob("text/*"):
        create_srt_from_transcription(fn, f"subtitles/{Path(fn).stem}.srt")