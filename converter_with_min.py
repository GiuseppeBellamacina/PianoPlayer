import mido

def midi_to_note_name(midi_number):
    sharp_notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    flat_notes = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
    
    octave = (midi_number // 12) - 1
    note_index = midi_number % 12

    note = sharp_notes[note_index]
    if note in ['C#', 'D#', 'F#', 'G#', 'A#']:
        note = flat_notes[note_index]
    
    return f"{note}{octave}"

def midi_to_text(midi_file):
    mid = mido.MidiFile(midi_file)
    note_events = []
    
    current_time = 0
    active_notes = set()
    min_duration = 0.2

    for msg in mid:
        current_time += msg.time

        rounded_time = round(current_time, 2)

        if msg.type == 'note_on' and msg.velocity > 0:
            note_name = midi_to_note_name(msg.note)
            active_notes.add(note_name)
        elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
            if active_notes and rounded_time >= min_duration:
                note_name = '+'.join(active_notes)
                note_events.append(f"{note_name},{rounded_time}")
                active_notes.clear()
            current_time = 0
        elif msg.type == 'note_on' and msg.velocity == 0:
            if rounded_time >= min_duration:
                note_events.append(f"Rest,{rounded_time}")
            current_time = 0

    return '\n'.join(note_events)

def write_score(file_path: str, text: str):
    with open(file_path, 'w') as f:
        f.write(text)

midi_file = 'chiaro_di_luna.mid'
output_text = midi_to_text('./midi/'+ midi_file)
write_score('./scores/' + midi_file.replace('.mid', '.txt'), output_text)