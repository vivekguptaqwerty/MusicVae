import streamlit as st
import pandas as pd
from mido import MidiFile, MidiTrack, Message
import random
from pydub import AudioSegment
import os
import platform
import tempfile
from fluidsynth import Synth  # Use pyfluidsynth

# Load preprocessed data
df = pd.read_pickle('music_processed.pkl')

# Function to generate music with structure
def generate_music(mood, midi_file, wav_file, mp3_file):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    # Get mood-based data
    mood_data = df[df['mood'] == mood].iloc[0]
    energy = mood_data['energy']
    danceability = mood_data['danceability']

    # Set base tempo and velocity based on mood
    base_tempo = int(120 + 60 * danceability)
    base_velocity = int(80 + 40 * energy)
    base_velocity = max(0, min(127, base_velocity))
    ticks_per_beat = 480

    # Define note ranges and scales
    notes = [60, 62, 64, 65, 67, 69, 71, 72]
    chord_notes = [60, 64, 67]

    total_beats = 48
    beats_per_section = total_beats // 4

    for beat in range(total_beats):
        if beat < beats_per_section:
            if random.random() < 0.5:
                note = random.choice(notes)
                duration = ticks_per_beat // 2
                velocity = base_velocity
                track.append(Message('note_on', note=note, velocity=velocity, time=0))
                track.append(Message('note_off', note=note, velocity=0, time=duration))

        elif beats_per_section <= beat < 2 * beats_per_section:
            if beat % 2 == 0:
                note = random.choice(notes)
                duration = ticks_per_beat // 4
                velocity = base_velocity
                track.append(Message('note_on', note=note, velocity=velocity, time=0))
                track.append(Message('note_off', note=note, velocity=0, time=duration))
            else:
                chord_note = random.choice(chord_notes)
                duration = ticks_per_beat // 2
                velocity = int(base_velocity * 0.7)
                velocity = max(0, min(127, velocity))
                track.append(Message('note_on', note=chord_note, velocity=velocity, time=0))
                track.append(Message('note_off', note=chord_note, velocity=0, time=duration))

        elif 2 * beats_per_section <= beat < 3 * beats_per_section:
            if random.random() < 0.7:
                note = random.choice(notes)
                duration = ticks_per_beat // 4 if danceability > 0.5 else ticks_per_beat // 2
                velocity = int(base_velocity * (1 + 0.3 * energy))
                velocity = max(0, min(127, velocity))
                track.append(Message('note_on', note=note, velocity=velocity, time=0))
                track.append(Message('note_off', note=note, velocity=0, time=duration))

        else:
            if random.random() < 0.3:
                note = random.choice(notes)
                duration = ticks_per_beat // 2
                velocity = int(base_velocity * (1 - (beat - 3 * beats_per_section) / beats_per_section))
                velocity = max(0, min(127, velocity))
                track.append(Message('note_on', note=note, velocity=velocity, time=0))
                track.append(Message('note_off', note=note, velocity=0, time=duration))

        if beat < total_beats - 1:
            track.append(Message('note_off', note=0, velocity=0, time=ticks_per_beat))

    mid.save(midi_file)

    # Convert MIDI to WAV using pyfluidsynth
    soundfont = 'FluidR3_GM.sf2'
    fs = Synth()
    fs.start()
    sf_id = fs.sfload(soundfont)
    fs.program_select(0, sf_id, 0, 0)
    with open(midi_file, 'rb') as midi_file_handle:
        fs.raw_midi(midi_file_handle.read())
    fs.write_wav(wav_file)
    fs.delete()

    # Convert WAV to MP3
    audio = AudioSegment.from_wav(wav_file)
    if len(audio) < 60000:
        silence = AudioSegment.silent(duration=60000 - len(audio))
        audio = audio + silence
    audio.export(mp3_file, format='mp3')
    os.remove(midi_file)
    os.remove(wav_file)

# Streamlit app
st.title("AI Music Generator 🎵")
st.markdown("Select a mood to generate a short music clip (up to ~1-2 minutes)!")

mood = st.selectbox("Choose a mood:", ["happy", "sad", "neutral"])

if st.button("Generate Music"):
    with st.spinner("Generating your music... (this may take a minute)"):
        # Use temporary directory for files
        with tempfile.TemporaryDirectory() as tmp_dir:
            midi_file = os.path.join(tmp_dir, 'temp.mid')
            wav_file = os.path.join(tmp_dir, 'temp.wav')
            mp3_file = os.path.join(tmp_dir, 'output.mp3')

            # Generate music
            generate_music(mood, midi_file, wav_file, mp3_file)

            # Read the MP3 file for playback
            with open(mp3_file, 'rb') as f:
                st.audio(f.read(), format='audio/mp3')
            st.success(f"{mood.capitalize()} music generated! 🎉")

st.markdown("---")
st.write("Built by Vivek Gupta & Harsh Gupta | Powered by Streamlit")
