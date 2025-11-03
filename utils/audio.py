import sounddevice as sd
import logging

CHANNELS = 1
BLOCKSIZE = 16000
DTYPE = "int16"

def init_audio_device(sample_rate):
    device_index = sd.default.device[0]
    device_info = sd.query_devices(device_index)
    logging.info(f"🎧 Using default microphone: {device_info['name']} @ {sample_rate} Hz")
    return device_index

def setup_audio_stream(sample_rate: int):
    device_index = init_audio_device(sample_rate)
    logging.info("🎤 Listening... Press Ctrl+C to stop.\n")

    return sd.RawInputStream(
        samplerate=sample_rate,
        blocksize=BLOCKSIZE,
        device=device_index,
        dtype=DTYPE,
        channels=CHANNELS,
    )
