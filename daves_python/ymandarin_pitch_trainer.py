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

class MandarinTrainer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mandarin Tone Master (M3 Edition)")
        self.setFixedSize(1000, 600)
        self.setStyleSheet("background-color: #121212;")

        # 1. Load Data
        self.load_data()
        self.current_idx = 0
        
        # 2. Audio Setup
        self.pa = pyaudio.PyAudio()
        self.is_recording = False
        self.pitch_history = [0] * 100

        # 3. UI
        self.init_ui()

        # 4. Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.process_audio_step)
        
        # Initial Display
        self.update_display()

    def load_data(self):
        try:
            self.df = pd.read_csv('phrases.csv')
            self.phrases = self.df.to_dict('records')
        except:
            self.phrases = [{"Chinese": "你好", "Pinyin": "Nǐ hǎo", "English": "Hello"}]

    def init_ui(self):
        central = QWidget()
        layout = QVBoxLayout()

        self.lbl_chinese = QLabel()
        self.lbl_chinese.setStyleSheet("font-size: 60px; color: #FFFFFF; font-family: 'Arial Unicode MS'; margin-top: 10px;")
        self.lbl_pinyin = QLabel()
        self.lbl_pinyin.setStyleSheet("font-size: 28px; color: #4CAF50;")
        self.lbl_english = QLabel()
        self.lbl_english.setStyleSheet("font-size: 20px; color: #AAAAAA; font-style: italic;")

        for lbl in [self.lbl_chinese, self.lbl_pinyin, self.lbl_english]:
            layout.addWidget(lbl, alignment=Qt.AlignmentFlag.AlignCenter)

        # Graph
        self.graph = pg.PlotWidget()
        self.graph.setBackground('#121212')
        self.graph.setYRange(75, 400) 
        self.graph.getAxis('left').setLabel('Pitch (Hz)')
        
        # Reference Line (Ghost Line)
        self.ref_curve = self.graph.plot(pen=pg.mkPen(color=(150, 150, 150), width=2, style=Qt.PenStyle.DashLine))
        
        # Your Live Line
        self.curve = self.graph.plot(pen=pg.mkPen(color='#00FFFF', width=4))
        
        layout.addWidget(self.graph)
        
        self.inst = QLabel("SPACE: Hold to Speak | DOWN: Next | R: Shuffle")
        self.inst.setStyleSheet("color: #555; font-size: 14px;")
        layout.addWidget(self.inst, alignment=Qt.AlignmentFlag.AlignCenter)

        central.setLayout(layout)
        self.setCentralWidget(central)

    def get_reference_pitch(self, filepath):
        """Analyzes the MP3 and extracts the pitch contour."""
        try:
            sound = parselmouth.Sound(filepath)
            pitch = sound.to_pitch()
            pitch_values = pitch.selected_array['frequency']
            # Remove zeros for interpolation
            valid_indices = np.where(pitch_values > 0)[0]
            if len(valid_indices) == 0: return [0] * 100
            
            # Extract just the section where there is voice
            cropped_pitch = pitch_values[valid_indices[0]:valid_indices[-1]]
            # Smooth/Interpolate to 100 points
            resampled = np.interp(np.linspace(0, len(cropped_pitch), 100), 
                                 np.arange(len(cropped_pitch)), 
                                 cropped_pitch)
            return resampled
        except Exception as e:
            print(f"Ref Pitch Error: {e}")
            return [0] * 100

    def update_display(self):
        item = self.phrases[self.current_idx]
        self.lbl_chinese.setText(item['Chinese'])
        self.lbl_pinyin.setText(item['Pinyin'])
        self.lbl_english.setText(item.get('English', ''))
        
        # Handle Audio and Ghost Line
        pattern = os.path.join(AUDIO_FOLDER, f"*_{item['Chinese']}.mp3")
        files = glob.glob(pattern)
        if files:
            # Show the grey reference line
            ref_data = self.get_reference_pitch(files[0])
            self.ref_curve.setData(ref_data)
            # Play via macOS system command
            subprocess.Popen(["afplay", files[0]])

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Space and not self.is_recording:
            self.start_recording()
        elif event.key() == Qt.Key.Key_Down:
            self.current_idx = (self.current_idx + 1) % len(self.phrases)
            self.update_display()
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
        self.pitch_history = [] # Fresh start
        self.stream = self.pa.open(format=pyaudio.paInt16, channels=1, rate=RATE,
                                  input=True, frames_per_buffer=CHUNK)
        self.timer.start(30)

    def stop_recording(self):
        self.is_recording = False
        self.timer.stop()
        if hasattr(self, 'stream'):
            self.stream.stop_stream()
            self.stream.close()

    def process_audio_step(self):
        if not self.is_recording: return
        try:
            data = self.stream.read(CHUNK, exception_on_overflow=False)
            samples = np.frombuffer(data, dtype=np.int16)
            sound = parselmouth.Sound(samples.astype(float), sampling_frequency=RATE)
            pitch = sound.to_pitch()
            pitch_values = pitch.selected_array['frequency']
            
            valid = pitch_values[pitch_values > 0]
            val = np.mean(valid) if len(valid) > 0 else 0
            
            if val > 0: # Only record actual speaking
                self.pitch_history.append(val)
                # Display only the most recent chunk of speech
                display_data = self.pitch_history[-100:]
                self.curve.setData(display_data)
        except:
            pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MandarinTrainer()
    window.show()
    sys.exit(app.exec())
