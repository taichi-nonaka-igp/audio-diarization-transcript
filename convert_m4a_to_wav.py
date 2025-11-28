import sys
from pathlib import Path

from pydub import AudioSegment


def m4a_to_wav(input_path, output_path=None):
    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(f"入力ファイルが見つかりません: {input_path}")

    # 出力パスが指定されていない場合、同じ場所に.wavを作成
    if output_path is None:
        output_path = input_path.with_suffix(".wav")

    # m4a読み込み → wav保存
    audio = AudioSegment.from_file(input_path, format="m4a")
    audio.export(output_path, format="wav")
    print(f"変換完了: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使い方: python convert_m4a_to_wav.py <input.m4a> [output.wav]")
        sys.exit(1)

    m4a_file = sys.argv[1]
    wav_file = sys.argv[2] if len(sys.argv) > 2 else None
    m4a_to_wav(m4a_file, wav_file)
