import sys
import os
import glob
import subprocess
import numpy as np
import pandas as pd
import pyaudio
import parselmouth
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QWidget
from PyQt6.QtCore import QTimer, Qt
import pyqtgraph as pg

# --- CONFIG ---
RATE = 44100
CHUNK = 2048 
AUDIO_FOLDER = "chinese_audio"

class MandarinToneMaster(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mandarin Tone Master v1.1")
        self.setFixedSize(1000, 650)
        self.setStyleSheet("background-color: #121212;")

        # 1. Data & State
        self.load_data()
        self.current_idx = 0
        self.is_recording = False
        self.pitch_history = []
        
        # 2. Audio Engine
        self.pa = pyaudio.PyAudio()

        # 3. UI Setup
        self.init_ui()
        self.update_display()

        # 4. Logic Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.process_audio_step)

    def load_data(self):
        try:
            self.df = pd.read_csv('chinese_learned_words.csv')
            self.phrases = self.df.to_dict('records')
        except Exception as e:
            print(f"CSV Load Error: {e}")
            self.phrases = [{"Chinese": "你好", "Pinyin": "Nǐ hǎo", "English": "Hello"}]

    def init_ui(self):
        central = QWidget()
        layout = QVBoxLayout()

        # Text Labels
        self.lbl_chinese = QLabel()
        self.lbl_chinese.setStyleSheet("font-size: 70px; color: white; font-family: 'Arial Unicode MS'; margin-top: 10px;")
        
        self.lbl_pinyin = QLabel()
        self.lbl_pinyin.setStyleSheet("font-size: 28px; color: #4CAF50; font-weight: bold;")
        
        self.lbl_english = QLabel()
        self.lbl_english.setStyleSheet("font-size: 20px; color: #888; font-style: italic;")

        for lbl in [self.lbl_chinese, self.lbl_pinyin, self.lbl_english]:
            layout.addWidget(lbl, alignment=Qt.AlignmentFlag.AlignCenter)

        # Graph Area
        self.graph = pg.PlotWidget()
        self.graph.setBackground('#121212')
        self.graph.setYRange(75, 450)
        self.graph.getAxis('left').setLabel('Pitch (Hz)', color='#666')
        self.graph.showGrid(x=True, y=True, alpha=0.2)
        
        # Reference Line (Native Speaker)
        self.ref_curve = self.graph.plot(pen=pg.mkPen(color=(100, 100, 100), width=3, style=Qt.PenStyle.DashLine))
        
        # User Line (Live)
        self.user_curve = self.graph.plot(pen=pg.mkPen(color='#00FFFF', width=5))
        
        layout.addWidget(self.graph)

        # Feedback/Status Bar
        self.lbl_feedback = QLabel("Hold [SPACE] to speak")
        self.lbl_feedback.setStyleSheet("font-size: 22px; color: #555; padding: 10px;")
        layout.addWidget(self.lbl_feedback, alignment=Qt.AlignmentFlag.AlignCenter)

        self.inst = QLabel("[↑/↓] Prev/Next  |  [ENTER] Replay  |  [R] Shuffle")
        self.inst.setStyleSheet("color: #444; font-size: 14px; margin-bottom: 10px;")
        layout.addWidget(self.inst, alignment=Qt.AlignmentFlag.AlignCenter)

        central.setLayout(layout)
        self.setCentralWidget(central)

    def get_reference_pitch(self, filepath):
        try:
            sound = parselmouth.Sound(filepath)
            pitch = sound.to_pitch()
            pitch_values = pitch.selected_array['frequency']
            voiced = pitch_values[pitch_values > 0]
            if len(voiced) < 5: return np.zeros(100)
            
            resampled = np.interp(np.linspace(0, len(voiced), 100), 
                                 np.arange(len(voiced)), 
                                 voiced)
            return resampled
        except:
            return np.zeros(100)

    def play_audio_file(self):
        item = self.phrases[self.current_idx]
        pattern = os.path.join(AUDIO_FOLDER, f"*_{item['Chinese']}.mp3")
        files = glob.glob(pattern)
        if files:
            subprocess.Popen(["afplay", files[0]])

    def update_display(self):
        item = self.phrases[self.current_idx]
        self.lbl_chinese.setText(item['Chinese'])
        self.lbl_pinyin.setText(item['Pinyin'])
        self.lbl_english.setText(item.get('English', ''))
        self.lbl_feedback.setText("Ready: Hold Space to Match Tone")
        self.lbl_feedback.setStyleSheet("color: #555; font-size: 22px;")
        self.user_curve.setData([])
        
        # Load Reference Ghost Line
        pattern = os.path.join(AUDIO_FOLDER, f"*_{item['Chinese']}.mp3")
        files = glob.glob(pattern)
        if files:
            ref_data = self.get_reference_pitch(files[0])
            self.ref_curve.setData(ref_data)
            self.play_audio_file()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Space and not self.is_recording:
            self.start_recording()
        elif event.key() == Qt.Key.Key_Down:
            self.current_idx = (self.current_idx + 1) % len(self.phrases)
            self.update_display()
        elif event.key() == Qt.Key.Key_Up:
            self.current_idx = (self.current_idx - 1) % len(self.phrases)
            self.update_display()
        elif event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.play_audio_file()
        elif event.key() == Qt.Key.Key_R:
            import random
            random.shuffle(self.phrases)
            self.current_idx = 0
            self.update_display()

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key.Key_Space:
            self.stop_recording()

    def start_recording(self):
        self.is_recording = True
        self.pitch_history = []
        self.lbl_feedback.setText("Listening...")
        self.lbl_feedback.setStyleSheet("color: #00FFFF; font-size: 22px;")
        self.stream = self.pa.open(format=pyaudio.paInt16, channels=1, rate=RATE,
                                  input=True, frames_per_buffer=CHUNK)
        self.timer.start(30)

    def stop_recording(self):
        self.is_recording = False
        self.timer.stop()
        if hasattr(self, 'stream'):
            self.stream.stop_stream()
            self.stream.close()
        self.calculate_score()

    def process_audio_step(self):
        if not self.is_recording: return
        try:
            data = self.stream.read(CHUNK, exception_on_overflow=False)
            samples = np.frombuffer(data, dtype=np.int16)
            sound = parselmouth.Sound(samples.astype(float), sampling_frequency=RATE)
            pitch = sound.to_pitch()
            pitch_values = pitch.selected_array['frequency']
            
            valid = pitch_values[pitch_values > 0]
            if len(valid) > 0:
                val = np.mean(valid)
                self.pitch_history.append(val)
                self.user_curve.setData(self.pitch_history[-100:])
        except:
            pass

    def calculate_score(self):
        ref_data = self.ref_curve.getData()[1]
        user_data = np.array(self.pitch_history)

        if len(user_data) < 10:
            self.lbl_feedback.setText("Try again: Speak longer!")
            self.lbl_feedback.setStyleSheet("color: #FFA500; font-size: 22px;")
            return

        user_resampled = np.interp(np.linspace(0, len(user_data), 100), 
                                   np.arange(len(user_data)), 
                                   user_data)

        ref_norm = ref_data - np.mean(ref_data)
        user_norm = user_resampled - np.mean(user_resampled)
        error = np.mean(np.abs(ref_norm - user_norm))

        if error < 20:
            self.lbl_feedback.setText(f"EXCELLENT! (Score: {max(0, 100-int(error))})")
            self.lbl_feedback.setStyleSheet("color: #00FF00; font-size: 26px; font-weight: bold;")
        elif error < 40:
            self.lbl_feedback.setText(f"GOOD PASS (Score: {max(0, 100-int(error))})")
            self.lbl_feedback.setStyleSheet("color: #ADFF2F; font-size: 22px;")
        else:
            self.lbl_feedback.setText(f"TONE OFF (Error: {int(error)}) - Try Again")
            self.lbl_feedback.setStyleSheet("color: #FF4444; font-size: 22px;")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MandarinToneMaster()
    window.show()
    sys.exit(app.exec())
