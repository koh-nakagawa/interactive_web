# README

## Interactive Web Project  
Audio reactive ripple visualisation for projection onto spider webs  
Audio input controls both synthetic bass output and visual ripple generation in Processing

---

## Features

* Real time audio input capture from a selected microphone
* Extraction of low frequency energy from the incoming sound
* Generation of synthetic bass to avoid acoustic feedback
* Transmission of bass values to Processing via OSC
* Visual ripple animation in Processing that expands outward based on bass strength
* User adjustable threshold allowing calibration for different microphones and noise levels
* Device selection through command line options

---

## System Overview

This project consists of two coordinated components.

### Python Audio Engine  
* Captures microphone input  
* Computes bass amplitude through FFT  
* Outputs synthetic bass (80 Hz sine wave) with amplitude mapped to detected bass  
* Sends OSC messages  
* Allows command line selection of input device, output device, and threshold  

### Processing Visual Engine  
* Receives OSC data  
* Displays expanding ripple circles from the center of the screen  
* Each ripple is created only when bass surpasses the threshold  
* Ripples expand at constant speed and disappear off screen  
* Suitable for projection onto physical spider webs for artistic installation

---

## Requirements

* macOS with Apple Silicon (recommended)
* Python 3 inside a conda environment
* Processing version 4 or later
* PyAudio, NumPy, python OSC  
* USB microphone or internal mic  
* External speaker or internal speaker  

---

## Project Structure

```
interactive_web  
  device.py  
  audio_engine.py  
  requirements.txt  
  processing  
    interactive_web.pde
```

---

## Installation

### Create and activate conda environment

```
conda create -n interactive_web python=3.11
conda activate interactive_web
```

### Install dependencies

```
pip install -r requirements.txt
```

---

## Checking Audio Devices

To list available input and output devices

```
python device.py
```

Example output

```
0  Internal Microphone     IN 1  OUT 0
1  Internal Speakers       IN 0  OUT 2
```

---

## Running the Audio Engine

Syntax

```
python audio_engine.py --input INPUT_INDEX --output OUTPUT_INDEX --threshold THRESHOLD_VALUE
```

Example

```
python audio_engine.py --input 0 --output 1 --threshold 0.002
```

---

## Processing Setup

1. Launch Processing  
2. Open the folder `interactive_web/processing`  
3. Run `interactive_web.pde`

Processing listens for OSC messages on port 5005.

---

## Visual Behaviour

* The screen remains black until bass exceeds the threshold  
* A new white circle appears at the center  
* The circle grows smoothly at a constant speed  
* The circle disappears once outside the visible area  
* Multiple circles can exist simultaneously  

---

## Avoiding Acoustic Feedback

The system uses synthetic bass rather than the microphone signal to prevent feedback.  
Only numerical bass values influence the synthetic output and the visualisation.

---

## Troubleshooting

### No ripples appear  
* Lower the threshold value  
* Confirm that audio_engine.py is running  
* Confirm that OSC port 5005 is not blocked  

### A ripple appears constantly  
* Increase the threshold value  
* Reduce microphone gain in macOS sound settings  

### No audio output  
* Confirm output device index  
* Check macOS audio routing  

---

## License

MIT License
