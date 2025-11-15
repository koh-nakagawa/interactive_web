import argparse
import pyaudio
import numpy as np
from pythonosc.udp_client import SimpleUDPClient
import math

# ====== 引数パーサ ======
parser = argparse.ArgumentParser(description="Audio engine (synthetic bass + OSC)")
parser.add_argument("--input", type=int, required=True, help="Input device index")
parser.add_argument("--output", type=int, required=True, help="Output device index")
parser.add_argument("--threshold", type=float, default=0.001, help="Bass threshold for ripple trigger")
parser.add_argument("--freq", type=float, default=80.0, help="Synthetic bass frequency in Hz")
parser.add_argument("--gain", type=float, default=1.0, help="Output gain multiplier")   # ← 追加
args = parser.parse_args()

INPUT_DEVICE_INDEX = args.input
OUTPUT_DEVICE_INDEX = args.output
THRESHOLD = args.threshold
SYNTH_FREQ = args.freq
GAIN = args.gain   # ← 音量調整

# ====== OSC設定 ======
OSC_IP = "127.0.0.1"
OSC_PORT = 5005
osc = SimpleUDPClient(OSC_IP, OSC_PORT)

# ====== オーディオ設定 ======
CHUNK = 1024
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100
BASS_MAX_FREQ = 200

p = pyaudio.PyAudio()

# ====== 入力デバイス情報 ======
input_info = p.get_device_info_by_index(INPUT_DEVICE_INDEX)
input_channels = max(1, int(input_info["maxInputChannels"]))

# ====== 出力デバイス情報 ======
output_info = p.get_device_info_by_index(OUTPUT_DEVICE_INDEX)
output_channels = max(1, int(output_info["maxOutputChannels"]))

# ====== 入力 ======
stream_in = p.open(
    format=FORMAT,
    channels=input_channels,
    rate=RATE,
    input=True,
    input_device_index=INPUT_DEVICE_INDEX,
    frames_per_buffer=CHUNK
)

# ====== 出力 ======
stream_out = p.open(
    format=FORMAT,
    channels=output_channels,
    rate=RATE,
    output=True,
    output_device_index=OUTPUT_DEVICE_INDEX,
    frames_per_buffer=CHUNK
)

# ===== 低音抽出 =====
def extract_bass(data):
    fft = np.fft.rfft(data)
    freqs = np.fft.rfftfreq(len(data), 1.0 / RATE)
    bass_power = np.sum(np.abs(fft[freqs < BASS_MAX_FREQ]))
    return float(bass_power / 10000.0)

# ===== 合成サイン波 =====
phase = 0.0
phase_step = 2.0 * math.pi * SYNTH_FREQ / RATE

print("=== Audio Engine (SYNTH BASS MODE) ===")
print(f"Input device:  {INPUT_DEVICE_INDEX} ({input_channels} ch)")
print(f"Output device: {OUTPUT_DEVICE_INDEX} ({output_channels} ch)")
print(f"Threshold:     {THRESHOLD}")
print(f"Synth freq:    {SYNTH_FREQ} Hz")
print(f"Gain:          {GAIN} x")
print("======================================")

osc.send_message("/threshold", THRESHOLD)

# ===== メインループ =====
while True:
    input_data = stream_in.read(CHUNK, exception_on_overflow=False)
    audio_np = np.frombuffer(input_data, dtype=np.float32)

    bass = extract_bass(audio_np)
    print("bass:", bass)

    # ---- 合成低音 ----
    t = np.arange(CHUNK)
    wave = np.sin(phase + phase_step * t).astype(np.float32)
    phase += phase_step * CHUNK

    # ---- 音量 ----
    volume = min(bass * 50.0 * GAIN, 1.0)   # ← gain が効く
    out_chunk = (wave * volume).astype(np.float32)

    stream_out.write(out_chunk.tobytes())

    osc.send_message("/bass", bass)
    osc.send_message("/threshold", THRESHOLD)
