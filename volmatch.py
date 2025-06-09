import os
from pydub import AudioSegment

# === 設定 ===
INPUT_DIR = "audio_mp3"         # MP3ファイルが格納されているフォルダ
OUTPUT_DIR = "normalized_mp3"   # 正規化済みファイルの出力先
TARGET_dBFS = -14.0             # 約92dB SPLに相当する目標音量（dBFS換算）

# 出力先フォルダを作成（存在しない場合）
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 音量を目標に合わせる関数
def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)

# MP3ファイルを一括処理
for filename in os.listdir(INPUT_DIR):
    if filename.lower().endswith(".mp3"):
        filepath = os.path.join(INPUT_DIR, filename)
        sound = AudioSegment.from_mp3(filepath)
        normalized_sound = match_target_amplitude(sound, TARGET_dBFS)

        output_path = os.path.join(OUTPUT_DIR, filename)
        normalized_sound.export(output_path, format="mp3")
        print(f"✅ Normalized to approx. 92dB SPL: {filename}")

print("🎉 すべてのMP3ファイルの音量を約92dB SPLに正規化しました。")
