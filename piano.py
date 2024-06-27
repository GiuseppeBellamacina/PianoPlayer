import pygame
import time
from os import system
import threading

class Note:
    def __init__(self, name):
        self.name = name
        self.load_sound()

    def load_sound(self):
        self.sound = pygame.mixer.Sound("piano_samples/" + self.name + ".mp3")

    def play(self):
        print(self.name)
        self.sound.play()

def read_score(file_path):
    pygame.mixer.init()
    with open(file_path, 'r') as f:
        lines = f.readlines()
    score = []
    for line in lines:
        if ',' not in line:
            continue
        notes, duration = line.strip().split(',')
        notes = [Note(note) for note in notes.split('+')]
        score.append((notes, float(duration)))
    return score

def play_notes(score):
    for notes, duration in score:
        start_time = time.time()
        threads = []
        for note in notes:
            thread = threading.Thread(target=note.play)
            thread.start()
            threads.append(thread)
        elapsed_time = time.time() - start_time
        time.sleep(max(0, duration - elapsed_time))
        for thread in threads:
            thread.join()

if __name__ == '__main__':
    system("cls")
    score = read_score('spartito.txt')
    play_notes(score)
    pygame.mixer.quit()
