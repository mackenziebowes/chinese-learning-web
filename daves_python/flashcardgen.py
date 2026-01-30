import pandas as pd
from gtts import gTTS
import zipfile
import os
import time

# 1. Load your CSV
# Make sure the filename matches your uploaded file
file_path = 'chinese_learned_words.csv'
df = pd.read_csv(file_path)

# 2. Extract phrases from the first column (hanzi)
phrases = df.iloc[:, 0].tolist()

# 3. Create a directory for the mp3s
output_dir = 'chinese_audio'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

print(f"Starting generation of {len(phrases)} files...")

# 4. Generate audio files
for i, phrase in enumerate(phrases):
    # Filename format: 001_phrase.mp3
    filename = f"{i+1:03d}_{phrase}.mp3"
    filepath = os.path.join(output_dir, filename)

    if os.path.exists(filepath): continue

    try:
        tts = gTTS(text=phrase, lang='zh-cn')
        tts.save(filepath)
        print(f"Generated: {filename}")
        # Small delay to avoid hitting rate limits
        time.sleep(0.5) 
    except Exception as e:
        print(f"Error generating {phrase}: {e}")

# 5. Create a ZIP archive
#zip_filename = 'chinese_phrases_audio.zip'
#with zipfile.ZipFile(zip_filename, 'w') as zipf:
#    for root, dirs, files in os.walk(output_dir):
#        for file in files:
#            zipf.write(os.path.join(root, file), file)

print(f"\nSuccess! All files are saved in {filename}")
