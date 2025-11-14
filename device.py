import pyaudio

def list_devices():
    p = pyaudio.PyAudio()
    count = p.get_device_count()

    print("=== Available Audio Devices ===")
    for i in range(count):
        info = p.get_device_info_by_index(i)
        print(f"{i}: {info['name']} | IN: {info['maxInputChannels']} | OUT: {info['maxOutputChannels']}")
    print("===============================")

if __name__ == "__main__":
    list_devices()
