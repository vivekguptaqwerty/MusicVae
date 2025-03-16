import streamlit as st
import pandas as pd
from mido import MidiFile, MidiTrack, Message
import random
from pydub import AudioSegment
import subprocess
import os

# Load preprocessed data
df = pd.read_pickle('C:/Users/vivek gupta/OneDrive/Desktop/musicVae/music_processed.pkl')

# Function to generate music with structure
def generate_music(mood, midi_file='C:/Users/vivek gupta/OneDrive/Desktop/musicVae/temp.mid', 
                   mp3_file='C:/Users/vivek gupta/OneDrive/Desktop/musicVae/output.mp3'):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    # Get mood-based data
    mood_data = df[df['mood'] == mood].iloc[0]
    energy = mood_data['energy']
    danceability = mood_data['danceability']

    # Set base tempo and velocity based on mood
    base_tempo = int(120 + 60 * danceability)  # BPM: 120-180
    base_velocity = int(80 + 40 * energy)  # Volume: 80-120
    base_velocity = max(0, min(127, base_velocity))  # Clamp to valid range
    ticks_per_beat = 480  # Standard MIDI resolution

    # Define note ranges and scales (C major for simplicity)
    notes = [60, 62, 64, 65, 67, 69, 71, 72]  # C4 to C5
    chord_notes = [60, 64, 67]  # C major chord

    # Song structure: Intro (8 beats), Verse (16 beats), Chorus (16 beats), Outro (8 beats)
    total_beats = 48  # ~1-2 minutes depending on tempo
    beats_per_section = total_beats // 4

    for beat in range(total_beats):
        # Intro: Sparse melody
        if beat < beats_per_section:
            if random.random() < 0.5:  # 50% chance to play a note
                note = random.choice(notes)
                duration = ticks_per_beat // 2  # Half-beat notes
                velocity = base_velocity
                track.append(Message('note_on', note=note, velocity=velocity, time=0))
                track.append(Message('note_off', note=note, velocity=0, time=duration))

        # Verse: Melody with some chords
        elif beats_per_section <= beat < 2 * beats_per_section:
            if beat % 2 == 0:  # Every other beat
                note = random.choice(notes)
                duration = ticks_per_beat // 4  # Quarter-beat notes for busier feel
                velocity = base_velocity
                track.append(Message('note_on', note=note, velocity=velocity, time=0))
                track.append(Message('note_off', note=note, velocity=0, time=duration))
            else:
                chord_note = random.choice(chord_notes)
                duration = ticks_per_beat // 2
                velocity = int(base_velocity * 0.7)
                velocity = max(0, min(127, velocity))  # Clamp
                track.append(Message('note_on', note=chord_note, velocity=velocity, time=0))
                track.append(Message('note_off', note=chord_note, velocity=0, time=duration))

        # Chorus: Fuller sound with higher energy
        elif 2 * beats_per_section <= beat < 3 * beats_per_section:
            if random.random() < 0.7:  # 70% chance to play a note
                note = random.choice(notes)
                duration = ticks_per_beat // 4 if danceability > 0.5 else ticks_per_beat // 2
                velocity = int(base_velocity * (1 + 0.3 * energy))  # Boost for energy
                velocity = max(0, min(127, velocity))  # Clamp to valid range
                track.append(Message('note_on', note=note, velocity=velocity, time=0))
                track.append(Message('note_off', note=note, velocity=0, time=duration))

        # Outro: Fade out
        else:
            if random.random() < 0.3:  # 30% chance to play a note
                note = random.choice(notes)
                duration = ticks_per_beat // 2
                velocity = int(base_velocity * (1 - (beat - 3 * beats_per_section) / beats_per_section))
                velocity = max(0, min(127, velocity))  # Clamp to valid range
                track.append(Message('note_on', note=note, velocity=velocity, time=0))
                track.append(Message('note_off', note=note, velocity=0, time=duration))

        # Add time between notes
        if beat < total_beats - 1:
            track.append(Message('note_off', note=0, velocity=0, time=ticks_per_beat))

    mid.save(midi_file)

    # Convert MIDI to WAV using fluidsynth
    soundfont = 'C:/Users/vivek gupta/OneDrive/Desktop/musicVae/FluidR3_GM.sf2'
    wav_file = 'C:/Users/vivek gupta/OneDrive/Desktop/musicVae/temp.wav'
    cmd = [
        'fluidsynth',
        '-a', 'dsound',
        '-ni',
        soundfont,
        midi_file,
        '-F', wav_file,
        '-r', '44100'
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("FluidSynth Output:", result.stdout)
        print("FluidSynth Errors (if any):", result.stderr)
    except subprocess.CalledProcessError as e:
        print("FluidSynth failed:", e)
        print("Output:", e.output)
        raise

    # Convert WAV to MP3
    audio = AudioSegment.from_wav(wav_file)
    # Adjust length if needed (optional)
    if len(audio) < 60000:  # Less than 1 minute, extend with silence
        silence = AudioSegment.silent(duration=60000 - len(audio))
        audio = audio + silence
    audio.export(mp3_file, format='mp3')
    os.remove(midi_file)
    os.remove(wav_file)

# Streamlit app
st.title("AI Music Generator 🎵")
st.markdown("Select a mood to generate a short music clip (up to ~1-2 minutes)!")

# Mood selection
mood = st.selectbox("Choose a mood:", ["happy", "sad", "neutral"])

# Generate button
if st.button("Generate Music"):
    with st.spinner("Generating your music... (this may take a minute)"):
        generate_music(mood, 
                       'C:/Users/vivek gupta/OneDrive/Desktop/musicVae/temp.mid', 
                       'C:/Users/vivek gupta/OneDrive/Desktop/musicVae/output.mp3')
        st.audio('C:/Users/vivek gupta/OneDrive/Desktop/musicVae/output.mp3', format='audio/mp3')
        st.success(f"{mood.capitalize()} music generated! 🎉")

# Footer
st.markdown("---")
st.write("Built by Vivek Gupta | Powered by Streamlit")