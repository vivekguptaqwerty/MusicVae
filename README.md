# AI Music Generator 🎵

A Python-based project to generate instrumental music based on user-selected moods using machine learning and MIDI synthesis. This project analyzes music data, maps it to moods, and creates a short instrumental track (~1-2 minutes) that reflects the chosen mood (happy, sad, or neutral). Built with Streamlit for an interactive web interface, it allows users to select a mood and instantly hear the generated music.

## Project Overview

This project leverages a music dataset (`tcc_ceds_music.csv`) to extract features like `energy`, `danceability`, and `sadness`. These features are used to classify songs into moods (`happy`, `sad`, `neutral`). Using `mido`, the project generates MIDI files with structured sections (intro, verse, chorus, outro), which are then converted to MP3 using `fluidsynth` and `pydub`. The final output is presented via a Streamlit web app.

### Features
- **Mood-Based Music Generation**: Generate music for "happy," "sad," or "neutral" moods.
- **Structured Songs**: Each track includes an intro, verse, chorus, and outro.
- **Dynamic Parameters**: Tempo, note duration, and velocity are adjusted based on mood features.
- **Interactive Interface**: Streamlit app for easy user interaction.
- **MP3 Output**: Music is converted to MP3 for universal playback.

## Tech Stack
- **Python 3.12**: Core programming language.
- **Libraries**:
  - `pandas`: Data processing.
  - `mido`: MIDI file generation.
  - `fluidsynth`: MIDI to WAV conversion.
  - `pydub`: WAV to MP3 conversion and audio processing.
  - `streamlit`: Web app interface.
- **Dependencies**:
  - FluidSynth executable (for MIDI synthesis).
  - SoundFont (`FluidR3_GM.sf2`) for instrument sounds.

## Prerequisites

Before running the project, ensure you have the following installed:

1. **Python 3.12**:
   - Download and install from [python.org](https://www.python.org/downloads/).
   - Verify: `python --version`

2. **FluidSynth**:
   - Download the Windows binary from [FluidSynth GitHub Releases](https://github.com/FluidSynth/fluidsynth/releases).
   - Extract to `C:\FluidSynth` and add `C:\FluidSynth\bin` to your system PATH.
   - Verify: `fluidsynth --version`

3. **SoundFont**:
   - Download `FluidR3_GM.sf2` (or any General MIDI soundfont) from [here](https://github.com/FluidSynth/fluidsynth/wiki/SoundFont).
   - Place it in `C:/Users/vivek gupta/OneDrive/Desktop/musicVae/FluidR3_GM.sf2`.

4. **FFmpeg** (optional, for `pydub`):
   - Download from [FFmpeg official site](https://ffmpeg.org/download.html).
   - Add to PATH or place `ffmpeg.exe` in `C:\Windows\System32`.
   - Verify: `ffmpeg -version`

## Installation

1. **Clone the Repository** (if applicable):
   ```bash
   git clone <your-repo-url>
   cd musicVae
