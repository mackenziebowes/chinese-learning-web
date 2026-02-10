class AudioEngine:
    def __init__(self, rate=44100):
        self.rate = rate

    def start_stream(self):
        print("Stream started")
