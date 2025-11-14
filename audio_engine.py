import argparse
import pyaudio
import numpy as np
from pythonosc.udp_client import SimpleUDPClient
import math

# ===== 引数パーサ =====
parser = argparse.ArgumentParser(description="Audio engine (synthetic bass + OSC)")
parser.add_argument("--input", type=int, required=True, help="Input device index")
parser.add_argument("--output", type=int, required=True, help="Output device index")
parser.add_argument("--threshold", type=float, default=0.001, help="Bass threshold for ripple trigger")
args = parser.parse_args()

INPUT_DEVICE_INDEX = args.input
OUTPUT_DEVICE_INDEX = args.output
THRESHOLD = args.threshold  # ← 追加

# ===== OSC =====
OSC_IP = "127.0.0.1"
OSC_PORT = 5005
osc = SimpleUDPClient(OSC_IP, OSC_PORT)

# ===== AUDIO =====
CHUNK = 1024
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100
BASS_MAX_FREQ = 200
SYNTH_FREQ = 80

p = pyaudio.PyAudio()

stream_in = p.open(
    format=FORMAT,
    channels=1,
    rate=RATE,
    input=True,
    input_device_index=INPUT_DEVICE_INDEX,
    frames_per_buffer=CHUNK
)

stream_out = p.open(
    format=FORMAT,
    channels=1,
    rate=RATE,
    output=True,
    output_device_index=OUTPUT_DEVICE_INDEX,
    frames_per_buffer=CHUNK
)

# ===== bass抽出 =====
def extract_bass(data):
    fft = np.fft.rfft(data)
    freqs = np.fft.rfftfreq(len(data), 1.0 / RATE)
    bass_power = np.sum(np.abs(fft[freqs < BASS_MAX_FREQ]))
    return float(bass_power / 10000.0)

# ===== サイン波 =====
phase = 0.0
phase_step = 2.0 * math.pi * SYNTH_FREQ / RATE

print("=== Audio Engine (SYNTH BASS MODE) ===")
print(f"Input device:  {INPUT_DEVICE_INDEX}")
print(f"Output device: {OUTPUT_DEVICE_INDEX}")
print(f"Threshold: {THRESHOLD}")
print("======================================")

# 初期 threshold を Processing に送る
osc.send_message("/threshold", THRESHOLD)

# ===== loop =====
while True:
    input_data = stream_in.read(CHUNK, exception_on_overflow=False)
    audio_np = np.frombuffer(input_data, dtype=np.float32)

    bass = extract_bass(audio_np)
    print("bass:", bass)

    # 合成低音
    t = np.arange(CHUNK)
    wave = np.sin(phase + phase_step * t).astype(np.float32)
    phase += phase_step * CHUNK

    volume = min(bass * 50.0, 1.0)
    out_chunk = (wave * volume).astype(np.float32)
    stream_out.write(out_chunk.tobytes())

    # ===== OSC送信 =====
    osc.send_message("/bass", bass)
    # thresholdも常に送ってOK（Processing側でいつでも反映できる）
    osc.send_message("/threshold", THRESHOLD)
