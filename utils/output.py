def print_wrapped(text, lang):
    words = text.split()
    for i in range(0, len(words), 10):
        print(f"\n🗣️ [{lang}] {' '.join(words[i:i + 10])}")
