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
            if note != 'Rest':
                sound = f'{note}.mp3'
                self.sounds.append(pygame.mixer.Sound(f'piano_samples/{sound}'))
            else:
                self.sounds.append(None)
    
    async def play(self):
        print(self.name)
        playing_channels = []
        for i, sound in enumerate(self.sounds):
            if sound:
                channel = pygame.mixer.find_channel()
                if channel:
                    channel.play(sound)
                    playing_channels.append(channel)
        
        await asyncio.sleep(self.duration)
        
        for channel in playing_channels:
            channel.stop()

def read_score(file_path: str) -> list[Note]:
    pygame.mixer.init(channels=16)
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

async def play_notes(score: list[Note]):
    for notes in score:
        await notes.play()

if __name__ == '__main__':
    system('clear') if name == 'posix' else system('cls')
    score = read_score('output.txt')
    asyncio.run(play_notes(score))
    pygame.mixer.quit()
