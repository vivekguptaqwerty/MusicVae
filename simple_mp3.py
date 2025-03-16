import pandas as pd
import numpy as np
from mido import MidiFile, MidiTrack, Message
import random
from pydub import AudioSegment
import os

# Load preprocessed data
df = pd.read_pickle('music_processed.pkl')

# Function to generate MIDI and convert to MP3
def generate_music(mood, midi_file='temp.mid', mp3_file='output.mp3'):
    # Generate MIDI
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    mood_data = df[df['mood'] == mood].iloc[0]
    energy = mood_data['energy']
    danceability = mood_data['danceability']

    tempo = int(120 + 60 * danceability)
    velocity = int(80 + 40 * energy)
    notes = [60, 62, 64, 65, 67, 69, 71]

    for _ in range(16):
        note = random.choice(notes)
        duration = int(480 * (1 - danceability))
        track.append(Message('note_on', note=note, velocity=velocity, time=0))
        track.append(Message('note_off', note=note, velocity=0, time=duration))

    mid.save(midi_file)

    # Convert MIDI to MP3 using ffmpeg
    soundfont = 'FluidR3_GM.sf2'
    wav_file = 'temp.wav'
    os.system(f'fluidsynth -ni {soundfont} {midi_file} -F {wav_file} -r 44100')
    audio = AudioSegment.from_wav(wav_file)
    audio.export(mp3_file, format='mp3')

    # Clean up temporary files
    os.remove(midi_file)
    os.remove(wav_file)

    print(f"{mood.capitalize()} music saved as {mp3_file}")

# Test with "happy"
generate_music('happy', 'temp.mid', 'happy_music.mp3')