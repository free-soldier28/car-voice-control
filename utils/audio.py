import sounddevice as sd
import logging

def init_audio_device(sample_rate):
    device_index = sd.default.device[0]
    device_info = sd.query_devices(device_index)
    logging.info(f"🎧 Using default microphone: {device_info['name']} @ {sample_rate} Hz")
    return device_index
