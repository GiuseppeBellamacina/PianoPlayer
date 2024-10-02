import pygame
import asyncio
from os import system, name

class Note():
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration
        self.sounds = []
        self.load_sound()
    
    def load_sound(self):
        notes = self.name.split('+')
        for note in notes:
            sound = f'{note}.mp3'
            self.sounds.append(pygame.mixer.Sound(f'piano_samples/{sound}'))
    
    async def play(self):
        print(self.name)
        for i, sound in enumerate(self.sounds):
            pygame.mixer.Channel(i).play(sound)
        await asyncio.sleep(self.duration)
        for i, sound in enumerate(self.sounds):
            pygame.mixer.Channel(i).stop()

def read_score(file_path: str) -> list[Note]:
    pygame.mixer.init()
    with open(file_path, 'r') as f:
        lines = f.readlines()
    score = []
    for line in lines:
        if ',' not in line:
            continue
        notes, duration = line.strip().split(',')
        note = Note(notes, float(duration))
        score.append(note)
    return score

def play_notes(score: list[Note]):
    for notes in score:
        asyncio.run(notes.play())

if __name__ == '__main__':
    system('clear') if name == 'posix' else system('cls')
    score = read_score('lalaland.txt')
    play_notes(score)
    pygame.mixer.quit()
