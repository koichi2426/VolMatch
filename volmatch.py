import os
from pydub import AudioSegment

# === 設定 ===
INPUT_DIR = "audio_mp3"          # 入力フォルダ
OUTPUT_DIR = "normalized_mp3"    # 出力フォルダ
TARGET_dBFS = -20.0              # 目標音量（通常は -20.0 dBFS）
MIN_dBFS = -92.0                 # 最小音量
MAX_dBFS = 0.0                   # 最大音量（dBFSは基本的に0が最大）

# 出力フォルダがなければ作成
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 音量調整関数（範囲内に収める）
def match_target_amplitude(sound, target_dBFS):
    current_dBFS = sound.dBFS
    change_in_dB = target_dBFS - current_dBFS
    new_sound = sound.apply_gain(change_in_dB)
    
    # 音量チェック
    final_dBFS = new_sound.dBFS
    if final_dBFS > MAX_dBFS:
        new_sound = new_sound.apply_gain(MAX_dBFS - final_dBFS)
    elif final_dBFS < MIN_dBFS:
        new_sound = new_sound.apply_gain(MIN_dBFS - final_dBFS)
    
    return new_sound

# 一括処理
for filename in os.listdir(INPUT_DIR):
    if filename.lower().endswith(".mp3"):
        filepath = os.path.join(INPUT_DIR, filename)
        sound = AudioSegment.from_mp3(filepath)
        normalized = match_target_amplitude(sound, TARGET_dBFS)

        output_path = os.path.join(OUTPUT_DIR, filename)
        normalized.export(output_path, format="mp3")
        print(f"Processed: {filename} → {normalized.dBFS:.2f} dBFS")

print("✅ 全MP3ファイルの音量を -92dB ～ 0dB に収めました。")
