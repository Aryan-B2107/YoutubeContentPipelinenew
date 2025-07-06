import json
import requests
import os
import subprocess
import re
import time  # Import time for potential retries/delays

# --- Configuration ---
MAIN_AUDIO_FILE = "Fluffy Goes To India ｜ Gabriel Iglesias [ux8GZAtCN-M].f251.webm"
OUTPUT_AUDIO_FILE = "final_audio_with_memes.mp3"  # You can change this to .webm if you want to keep original format
MEME_SOUNDS_DIR = "meme_sounds"  # Directory to save downloaded meme sounds

# Base URL for MyInstants.com sounds
MYINSTANTS_BASE_URL = "https://www.myinstants.com/media/sounds/"

# Transcript data with meme sound assignments
# This should be the JSON structure you provided with the 'meme_sound' keys.
# I've embedded it directly for simplicity, but in a real app, you might load it from a file.
transcript_data = [
    {
        "content": "Martina and I just got back from India",
        "start_time": "0:00",
        "end_time": "0:03"
    },
    {
        "content": "yeah so let me tell you I started",
        "start_time": "0:03",
        "end_time": "0:07"
    },
    {
        "content": "posting on Facebook and Twitter that we",
        "start_time": "0:07",
        "end_time": "0:09"
    },
    {
        "content": "were gonna go out there to do these",
        "start_time": "0:09",
        "end_time": "0:10"
    },
    {
        "content": "shows and then people started sending me",
        "start_time": "0:10",
        "end_time": "0:12"
    },
    {
        "content": "messages questioning what I was gonna do",
        "start_time": "0:12",
        "end_time": "0:14"
    },
    {
        "content": "first of all are they gonna understand",
        "start_time": "0:14",
        "end_time": "0:17"
    },
    {
        "content": "you in India will they understand",
        "start_time": "0:17",
        "end_time": "0:19"
    },
    {
        "content": "English okay will they be able to follow",
        "start_time": "0:19",
        "end_time": "0:21"
    },
    {
        "content": "along with your stories once we got",
        "start_time": "0:21",
        "end_time": "0:24"
    },
    {
        "content": "there I come to find out that more",
        "start_time": "0:24",
        "end_time": "0:26"
    },
    {
        "content": "people speak English in India than in",
        "start_time": "0:26",
        "end_time": "0:29"
    },
    {
        "content": "all of the u.s. and Canada put together",
        "start_time": "0:29",
        "end_time": "0:32",
        "meme_sound": "Shocked sound"
    },
    {
        "content": "might as well throw Mexico in there for",
        "start_time": "0:32",
        "end_time": "0:34"
    },
    {
        "content": "extra credit because there's that many",
        "start_time": "0:34",
        "end_time": "0:38"
    },
    {
        "content": "people and yes they have the internet",
        "start_time": "0:38",
        "end_time": "0:40"
    },
    {
        "content": "they got the Internet they got Bollywood",
        "start_time": "0:40",
        "end_time": "0:42"
    },
    {
        "content": "they got Hollywood they understand",
        "start_time": "0:42",
        "end_time": "0:43"
    },
    {
        "content": "American culture so much more than we",
        "start_time": "0:43",
        "end_time": "0:46"
    },
    {
        "content": "understand theirs",
        "start_time": "0:46",
        "end_time": "0:46",
        "meme_sound": "Galaxy brain meme"
    },
    {
        "content": "second thing people",
        "start_time": "0:46",
        "end_time": "0:49"
    },
    {
        "content": "tried to warn me about going over there",
        "start_time": "0:49",
        "end_time": "0:51"
    },
    {
        "content": "Gabriel be careful India is a",
        "start_time": "0:51",
        "end_time": "0:54"
    },
    {
        "content": "third-world country don't drink the",
        "start_time": "0:54",
        "end_time": "0:56"
    },
    {
        "content": "water in India",
        "start_time": "0:56",
        "end_time": "0:57"
    },
    {
        "content": "it contains parasites that'll make you",
        "start_time": "0:57",
        "end_time": "0:59"
    },
    {
        "content": "really sick don't eat the food from the",
        "start_time": "0:59",
        "end_time": "1:02"
    },
    {
        "content": "street people especially the street meat",
        "start_time": "1:02",
        "end_time": "1:04"
    },
    {
        "content": "it contains a parasite that'll make you",
        "start_time": "1:04",
        "end_time": "1:06"
    },
    {
        "content": "really sick and most importantly there's",
        "start_time": "1:06",
        "end_time": "1:09"
    },
    {
        "content": "a lot of crime over there don't stay out",
        "start_time": "1:09",
        "end_time": "1:11"
    },
    {
        "content": "late when the Sun Goes Down",
        "start_time": "1:11",
        "end_time": "1:16",
        "meme_sound": "dun dun dunnnnnnnn"
    },
    {
        "content": "I'm like is it that bad",
        "start_time": "1:16",
        "end_time": "1:21",
        "meme_sound": "Oh My God Meme"
    },
    {
        "content": "so I'm like let me get this straight",
        "start_time": "1:21",
        "end_time": "1:22"
    }
]

# --- Meme Sound Name Mapping (Expanded for better failsafes) ---
# This dictionary maps the display name of the meme sound to its actual filename on myinstants.com.
# This is crucial because myinstants.com uses inconsistent naming.
# Each value is now a LIST of potential filenames to try, in order of preference.
meme_filename_map = {
    "Sad Violin (the meme one)": ["sad-violin-meme.mp3", "sad-violin.mp3"],
    "Emotional Damage Meme": ["emotional-damage-meme.mp3", "emotional-damage.mp3"],
    "Error SOUNDSS": ["error.mp3", "error-sound.mp3", "error-sounds.mp3"],
    "Scream meme": ["scream-meme.mp3", "scream.mp3"],
    "Among Us role reveal sound": ["among-us-role-reveal.mp3", "among-us-reveal.mp3"],
    "Meme final": ["meme-final.mp3", "final-meme.mp3"],
    "Death sound (Fortnite)": ["death-sound-fortnite.mp3", "fortnite-death-sound.mp3", "death-sound.mp3"],
    "baby laughing meme": ["baby-laughing-meme.mp3", "baby-laugh.mp3"],
    "Fart Meme Sound": ["fart-meme-sound.mp3", "fart-sound.mp3", "fart.mp3"],
    "instagram thud": ["instagram-thud.mp3", "thud-instagram.mp3", "thud.mp3"],
    "RUN vine": ["run-vine.mp3", "run.mp3", "vine-run.mp3"],
    "spiderman meme song": ["spiderman-meme-song.mp3", "spiderman-song.mp3"],
    "Galaxy meme": ["galaxy-meme.mp3", "galaxy-brain-meme.mp3", "galaxy.mp3"],
    "Punch Sound": ["punch-sound.mp3", "punch.mp3"],
    "outro song": ["outro-song.mp3", "outro.mp3"],
    "*Snore* mimimimimimi": ["snore-mimimimimimi.mp3", "snore.mp3"],
    "what da dog doin": ["what-da-dog-doin.mp3"],
    "WIDE PUTIN MEME": ["wide-putin-meme.mp3", "wide-putin.mp3"],
    "cat laugh meme 1": ["cat-laugh-meme.mp3", "cat-laugh.mp3"],
    "DEJA VU MEME": ["deja-vu-meme.mp3", "deja-vu.mp3"],
    "\"Aw Shit! Here go again.\" CJ from GTA SA": ["aw-shit-here-go-again-cj.mp3", "aw-shit-here-we-go-again.mp3"],
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA": ["aaaaaa.mp3", "aaaaaaaa.mp3", "screaming-a.mp3"],
    "-999 Social Credit Siren": ["minus-999-social-credit-siren.mp3", "social-credit-siren.mp3"],
    "Shocked sound": ["shocked-sound.mp3", "shock.mp3"],
    "dun dun dunnnnnnnn": ["dun-dun-dunnnn.mp3", "dun-dun-dun.mp3", "dun-dun-dunnnnn.mp3"],
    "They ask you how you are meme": ["they-ask-you-how-you-are-meme.mp3", "they-ask-you-how-you-are.mp3"],
    "Directed by Robert B Weide": ["directed-by-robert-b-weide.mp3", "robert-b-weide.mp3"],
    "Fart Meme Sound (Better and louder)": ["fart-meme-sound-better-louder.mp3", "fart-loud.mp3"],
    "French meme song": ["french-meme-song.mp3", "french-song.mp3"],
    "Wow Anime meme": ["wow-anime-meme.mp3", "wow-anime.mp3"],
    "Oh My God Meme": ["oh-my-god-meme.mp3", "oh-my-god.mp3"],
    "FBI OPEN UP (with explosion)": ["fbi-open-up-explosion.mp3", "fbi-open-up.mp3"],
    "asian meme huh?": ["asian-meme-huh.mp3", "asian-huh.mp3"],
    "Bruh meme": ["bruh-meme.mp3", "bruh.mp3"],
    "HAha funny laugh": ["haha-funny-laugh.mp3", "funny-laugh.mp3"],
    "'What' Bottom Text Meme (Sanctuary Guardian) - S": ["what-bottom-text-meme.mp3", "what-meme.mp3"],
    "WHAT ARE YOU DOING IN MY SWAMP": ["what-are-you-doing-in-my-swamp.mp3"],
    "Nani FULL": ["nani-full.mp3", "nani.mp3"],
    "Snoop Dogg meme": ["snoop-dogg-meme.mp3", "snoop-dogg.mp3"],
    "Coffin Dance Meme": ["coffin-dance-meme.mp3", "coffin-dance.mp3"],
    "Long brain fart": ["long-brain-fart.mp3", "brain-fart.mp3"],
    "bing chilling": ["bing-chilling.mp3"],
    "Oh No No No Tik Tok Song Sound Effect": ["oh-no-no-no-tik-tok.mp3", "oh-no-no-no.mp3"],
    "jojo - ayayay": ["jojo-ayayay.mp3", "ayayay.mp3"],
    "AUUGHHH": ["auughhh.mp3", "augh.mp3"],
    "frog laughing meme": ["frog-laughing-meme.mp3", "frog-laugh.mp3"],
    "English or Spanish Song": ["english-or-spanish-song.mp3"],
    "We Got Him Meme Song Loud": ["we-got-him-meme-song-loud.mp3"],
    "punch sound effect meme": ["punch-sound-effect-meme.mp3", "punch-effect-meme.mp3"],
    "danger alarm sound effect meme": ["danger-alarm-sound-effect-meme.mp3"],
    "musica triste meme": ["musica-triste-meme.mp3"],
    "æ meme": ["ae-meme.mp3"],
    "oof minecraft": ["oof-minecraft.mp3", "oof.mp3"],
    "Okay let’s go": ["okay-lets-go.mp3", "lets-go.mp3"],
    "meme sound": ["meme-sound.mp3"],
    "Доброе утро моя девочка": ["dobroe-utro-moya-devochka.mp3"],
    "AMOGUS SCREAMING": ["amogus-screaming.mp3"],
    "Lightskin Rizz (Sin City)": ["lightskin-rizz-sin-city.mp3"],
    "Run Meme": ["run-meme.mp3"],
    "windows xp21": ["windows-xp21.mp3"],
    "Galaxy brain meme": ["galaxy-brain-meme.mp3"],  # Already in list, but explicit
    "MUSICA DE SIGMA ESTOURADO": ["musica-de-sigma-estourado.mp3"],
    "Rat dance Music": ["rat-dance-music.mp3"],
    "Lagging/loading": ["lagging-loading.mp3"],
    "Risadinha de ladrão": ["risadinha-de-ladrao.mp3"],
    "“Hello There” Obi Wan": ["hello-there-obi-wan.mp3"],
    "Bad to the Bone Meme": ["bad-to-the-bone-meme.mp3"],
    "Hey let her go!": ["hey-let-her-go.mp3"],
    "Meme mp3": ["meme-mp3.mp3"],
    "Lobotomy Sound Effect": ["lobotomy-sound-effect.mp3"],
    "FIRE IN THE HOLE Geometry Dash": ["fire-in-the-hole-geometry-dash.mp3"],
    "Duck toy sound": ["duck-toy-sound.mp3"],
    "U Got That (meme)": ["u-got-that-meme.mp3"],
    "FAIL SOUND MEME": ["fail-sound-meme.mp3", "fail.mp3"],
    "Gas Gas Gas - Manuel (Short)": ["gas-gas-gas-manuel-short.mp3"],
    "Sicko Mode Meme SFX": ["sicko-mode-meme-sfx.mp3"],
    "Pablo MEME": ["pablo-meme.mp3"],
    "You Are My Sunshine Lebron James": ["you-are-my-sunshine-lebron-james.mp3"],
    "Lá ele": ["la-ele.mp3"],
    "BYE BYE! ~ Lumi Athena SFX": ["bye-bye-lumi-athena-sfx.mp3"],
    "Electric Zoo": ["electric-zoo.mp3"],
    "wee weee weee": ["wee-weee-weee.mp3"],
    "JOJO SONG": ["jojo-song.mp3"],
    "Explosion meme": ["explosion-meme.mp3", "explosion.mp3"],
    "Punch Effect": ["punch-effect.mp3"],
    "lula tira": ["lula-tira.mp3"],
    "Yes King AHHHHHHHHHHHHHHHH": ["yes-king-ahhhhhhhhhhhhhhhh.mp3"],
    "MICHAEL DONT LEAVE ME HERE": ["michael-dont-leave-me-here.mp3"],
    "tom da tank meme": ["tom-da-tank-meme.mp3"],
}


# Function to convert MM:SS or HH:MM:SS to seconds
def time_to_seconds(time_str):
    parts = list(map(int, time_str.split(':')))
    if len(parts) == 3:  # HH:MM:SS
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    elif len(parts) == 2:  # MM:SS
        return parts[0] * 60 + parts[1]
    elif len(parts) == 1:  # S
        return parts[0]
    return 0


# Function to sanitize meme names for filenames and URL paths
# Now returns a list of potential filenames to try
def sanitize_meme_name(name):
    potential_filenames = []

    # 1. Try exact mapping first
    if name in meme_filename_map:
        potential_filenames.extend(meme_filename_map[name])

    # 2. Generate common inferred names if not explicitly mapped or as fallback
    s = name.lower()
    s = re.sub(r'[^a-z0-9\s-]', '', s)  # Remove non-alphanumeric except space and hyphen
    s = re.sub(r'\s+', '-', s)  # Replace spaces with hyphens
    s = s.strip('-')  # Remove leading/trailing hyphens

    # Add common extensions/variations
    if s and s + ".mp3" not in potential_filenames:
        potential_filenames.append(s + ".mp3")
    if s and s + ".wav" not in potential_filenames:  # MyInstants sometimes uses .wav
        potential_filenames.append(s + ".wav")

    # Add variations like "-meme", "-sound", "-effect"
    if s and not s.endswith("-meme") and s + "-meme.mp3" not in potential_filenames:
        potential_filenames.append(s + "-meme.mp3")
    if s and not s.endswith("-sound") and s + "-sound.mp3" not in potential_filenames:
        potential_filenames.append(s + "-sound.mp3")
    if s and not s.endswith("-effect") and s + "-effect.mp3" not in potential_filenames:
        potential_filenames.append(s + "-effect.mp3")

    # Remove duplicates and ensure order of preference
    return list(dict.fromkeys(potential_filenames))


# Function to download a meme sound with failsafes
def download_meme_sound(meme_name, download_dir):
    potential_files = sanitize_meme_name(meme_name)
    temp_file_path = None  # Initialize temp_file_path here

    for sanitized_name in potential_files:
        file_path = os.path.join(download_dir, sanitized_name)
        url = MYINSTANTS_BASE_URL + sanitized_name

        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            print(f"'{meme_name}' already downloaded and valid: {file_path}")
            return file_path

        print(f"Attempting to download '{meme_name}' as '{sanitized_name}' from {url}...")
        try:
            response = requests.get(url, stream=True, timeout=10)  # Added timeout
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)

            # Save to a temporary file first
            temp_file_path = file_path + ".tmp"
            with open(temp_file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            # Check file size after download
            if os.path.getsize(temp_file_path) == 0:
                print(f"Downloaded file '{sanitized_name}' is empty. Trying next alternative...")
                os.remove(temp_file_path)  # Clean up empty file
                continue  # Try next alternative

            # If download successful and not empty, rename to final name
            os.rename(temp_file_path, file_path)
            print(f"Successfully downloaded '{meme_name}' to {file_path}")
            return file_path

        except requests.exceptions.Timeout:
            print(f"Timeout while downloading '{sanitized_name}'. Trying next alternative...")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading '{sanitized_name}' from {url}: {e}. Trying next alternative...")
        except Exception as e:
            print(f"An unexpected error occurred while downloading '{sanitized_name}': {e}. Trying next alternative...")

        # Clean up temporary file if it exists from a failed attempt
        if temp_file_path and os.path.exists(temp_file_path):  # Check if temp_file_path was assigned
            os.remove(temp_file_path)

    print(f"Failed to download '{meme_name}' after trying all alternatives.")
    return None


# Main function to process audio
def process_audio_with_memes():
    if not os.path.exists(MAIN_AUDIO_FILE):
        print(f"Error: Main audio file '{MAIN_AUDIO_FILE}' not found.")
        print("Please ensure the audio file is in the same directory as the script.")
        return

    # Create directory for meme sounds if it doesn't exist
    os.makedirs(MEME_SOUNDS_DIR, exist_ok=True)

    meme_files = []
    filter_complex_parts = []
    input_index = 1  # Start from 1 because 0 is the main audio

    # Collect and download unique meme sounds
    unique_meme_sounds = {item['meme_sound'] for item in transcript_data if 'meme_sound' in item}
    downloaded_meme_paths = {}

    for meme_name in unique_meme_sounds:
        downloaded_path = download_meme_sound(meme_name, MEME_SOUNDS_DIR)
        if downloaded_path:
            downloaded_meme_paths[meme_name] = downloaded_path
            meme_files.append(downloaded_path)
        else:
            print(f"Skipping '{meme_name}' due to download failure.")

    # Build FFmpeg filter_complex string
    # [0:a] is the main audio stream
    # [1:a], [2:a], etc., are the meme sound streams
    # adelay=delay_ms|delay_ms applies a delay to the audio stream
    # amix mixes all streams together

    # Add input flags for FFmpeg
    ffmpeg_inputs = ["-i", MAIN_AUDIO_FILE]
    for meme_path in meme_files:
        ffmpeg_inputs.extend(["-i", meme_path])

    # Build the filter_complex string
    # Example: [1:a]adelay=1000|1000[s1];[2:a]adelay=5000|5000[s2];[0:a][s1][s2]amix=inputs=3:duration=longest

    amix_inputs = ["[0:a]"]  # Start with the main audio stream

    for item in transcript_data:
        if 'meme_sound' in item:
            meme_name = item['meme_sound']
            if meme_name in downloaded_meme_paths:  # Only include if successfully downloaded
                start_time_seconds = time_to_seconds(item['start_time'])
                delay_ms = start_time_seconds * 1000  # Convert seconds to milliseconds

                # Assign a unique stream label for each delayed sound
                stream_label = f"s{input_index}"

                # Add adelay filter for the current meme sound
                filter_complex_parts.append(f"[{input_index}:a]adelay={delay_ms}|{delay_ms}[{stream_label}]")
                amix_inputs.append(f"[{stream_label}]")  # Add to amix inputs
                input_index += 1  # Increment for the next sound effect input

    # Combine all filter parts and the amix command
    if len(amix_inputs) > 1:  # If there are meme sounds to mix
        filter_complex_str = ";".join(filter_complex_parts)
        filter_complex_str += f";{''.join(amix_inputs)}amix=inputs={len(amix_inputs)}:duration=longest"
    else:  # Only main audio, no memes to mix
        print("No meme sounds were successfully downloaded to mix.")
        # If no memes, just copy the main audio to the output file
        ffmpeg_command = ["ffmpeg", "-i", MAIN_AUDIO_FILE, "-c:a", "aac", "-b:a", "192k", "-y", OUTPUT_AUDIO_FILE]
        filter_complex_str = ""  # Ensure it's empty
        print("\n--- FFmpeg Command (No memes to mix) ---")
        print(" ".join(ffmpeg_command))
        print("----------------------------------------\n")

    # Construct the full FFmpeg command if filter_complex_str was built
    if filter_complex_str:
        ffmpeg_command = ["ffmpeg"] + ffmpeg_inputs
        ffmpeg_command.extend(["-filter_complex", filter_complex_str])
        # Output options:
        # -c:a aac for AAC audio codec (good for .mp3)
        # -b:a 192k for bitrate
        # -map_channel 0.0.0 for stereo output if source is stereo
        # -y to overwrite output file without prompt
        ffmpeg_command.extend(["-c:a", "aac", "-b:a", "192k", "-y", OUTPUT_AUDIO_FILE])

        print("\n--- FFmpeg Command ---")
        print(" ".join(ffmpeg_command))
        print("----------------------\n")
    elif len(amix_inputs) == 1:  # Case where only main audio input, handled above
        pass  # Command already set for direct copy
    else:
        print("No valid FFmpeg command could be constructed. Exiting.")
        return

    # Execute FFmpeg command
    try:
        # Use subprocess.run for simpler execution and error handling
        # capture_output=True captures stdout/stderr, text=True decodes as text
        result = subprocess.run(ffmpeg_command, check=True, capture_output=True, text=True)
        print("FFmpeg output:")
        print(result.stdout)
        print(result.stderr)
        print(f"\nSuccessfully created '{OUTPUT_AUDIO_FILE}' with meme sounds!")
    except subprocess.CalledProcessError as e:
        print(f"\nError running FFmpeg:")
        print(f"Command: {' '.join(e.cmd)}")
        print(f"Return Code: {e.returncode}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        print("\nPlease ensure FFmpeg is installed and added to your system's PATH.")
        print("Also check if the meme sound filenames in meme_filename_map are correct on myinstants.com.")
        print("The 'encoding error' might be due to a corrupted or incomplete downloaded meme sound.")
    except FileNotFoundError:
        print("\nError: FFmpeg command not found.")
        print("Please ensure FFmpeg is installed and its executable directory is added to your system's PATH.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
#ff

# Run the audio processing
if __name__ == "__main__":
    process_audio_with_memes()
