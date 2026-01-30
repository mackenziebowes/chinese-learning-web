import pandas as pd
import tkinter as tk
from tkinter import font
import pygame
import os
import random

class ChineseFlashcards:
    def __init__(self, root):
        self.root = root
        self.root.title("Chinese Audio Flashcards")
        self.root.geometry("600x400")
        self.root.configure(bg="#f0f0f0")

        # Initialize Pygame Mixer for audio
        pygame.mixer.init()

        # Load Data
        self.df = pd.read_csv('chinese_learned_words.csv')
        self.original_data = self.df.values.tolist()
        self.data = list(self.original_data)
        
        self.current_index = 0
        self.is_side_b = False

        # Setup UI Elements
        self.card_font_large = font.Font(family="Arial", size=48, weight="bold")
        self.card_font_small = font.Font(family="Arial", size=18)
        
        self.card_frame = tk.Frame(root, bg="white", highlightbackground="black", highlightthickness=2)
        self.card_frame.pack(expand=True, fill="both", padx=40, pady=40)

        self.label_main = tk.Label(self.card_frame, text="", font=self.card_font_large, bg="white")
        self.label_main.pack(expand=True)

        self.label_sub = tk.Label(self.card_frame, text="", font=self.card_font_small, bg="white", fg="#555")
        self.label_sub.pack(pady=10)

        #self.btn_audio = tk.Button(root, text="🔊 Play Sound", command=self.play_audio)
        self.is_muted = False
        self.dark_mode = False

        # Color Palettes
        self.colors = {
            "light": {"bg": "#f0f0f0", "card": "white", "text": "black", "sub": "#555"},
            "dark": {"bg": "#121212", "card": "#1e1e1e", "text": "#e0e0e0", "sub": "#bbbbbb"}
        }
        
        # Key Bindings
        self.root.bind("<space>", lambda e: self.flip_card())
        self.root.bind("<Down>", lambda e: self.next_card())
        self.root.bind("<Up>", lambda e: self.prev_card())
        self.root.bind("<Return>", lambda e: self.play_audio())
        self.root.bind(",", lambda e: self.play_audio())
        self.root.bind("<Right>", lambda e: self.play_audio())
        self.root.bind("<Left>", lambda e: self.flip_card())
        self.root.bind("r", lambda e: self.shuffle_cards())
        self.root.bind("R", lambda e: self.shuffle_cards())
        self.root.bind("m", lambda e: self.toggle_mute())
        self.root.bind("M", lambda e: self.toggle_mute())
        self.root.bind("d", lambda e: self.toggle_dark_mode())
        self.root.bind("D", lambda e: self.toggle_dark_mode())

        self.update_card()

    def update_card(self):
        hanzi, pinyin, english = self.data[self.current_index]
        theme = self.colors["dark"] if self.dark_mode else self.colors["light"]
        
        if not self.is_side_b:
            # Side A: Just the Chinese Phrase
            self.label_main.config(text=hanzi, fg=theme["text"])
            self.label_sub.config(text="[Press Space to Reveal]")
            #self.btn_audio.pack_forget() # Hide audio button on Side A
        else:
            # Side B: Pinyin + English
            pinyin_color = "#ff6b6b" if self.dark_mode else "#d9534f"
            self.label_main.config(text=pinyin, fg=pinyin_color)
            self.label_sub.config(text=english)
            #self.btn_audio.pack(pady=10) # Show audio button on Side B

    def flip_card(self):
        self.is_side_b = not self.is_side_b
        self.update_card()
        if self.is_side_b:
            if self.is_muted == False:
                self.play_audio()

    def next_card(self):
        self.current_index = (self.current_index + 1) % len(self.data)
        self.is_side_b = False
        self.update_card()

    def prev_card(self):
        self.current_index = (self.current_index - 1) % len(self.data)
        self.is_side_b = False
        self.update_card()

    def shuffle_cards(self):
        random.shuffle(self.data)
        self.current_index = 0
        self.is_side_b = False
        self.update_card()
        print("Deck Shuffled!")

    def play_audio(self):
        #if self.is_muted:
        #    return

        hanzi = self.data[self.current_index][0]
        
        # Find the file in chinese_audio folder
        # Scheme: 001_phrase.mp3
        # Note: We search for the phrase because the index changes when shuffled
        found_file = None
        for file in os.listdir("chinese_audio"):
            if file.endswith(f"_{hanzi}.mp3"):
                found_file = os.path.join("chinese_audio", file)
                break
        
        if found_file:
            pygame.mixer.music.load(found_file)
            pygame.mixer.music.play()
        else:
            print(f"Audio file for {hanzi} not found.")

    def toggle_mute(self):
        self.is_muted = not self.is_muted
        status = "MUTED" if self.is_muted else "UNMUTED"
        print(f"Volume Status: {status}")
        
        # Optional: update the audio button text to show status
        #if self.is_muted:
            #self.btn_audio.config(text="🔇 Muted", fg="red")
        #else:
            #self.btn_audio.config(text="🔊 Play Sound", fg="black")

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        theme = self.colors["dark"] if self.dark_mode else self.colors["light"]
        
        # Update Main Window and Frame
        self.root.config(bg=theme["bg"])
        self.card_frame.config(bg=theme["card"])
        
        # Update Labels
        self.label_main.config(bg=theme["card"], fg=theme["text"])
        self.label_sub.config(bg=theme["card"], fg=theme["sub"])
        
        # Update Button
        #self.btn_audio.config(bg=theme["bg"], fg=theme["text"])
        
        # Refresh current card to ensure specific colors (like Pinyin red) stay visible
        self.update_card()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChineseFlashcards(root)
    root.mainloop()
