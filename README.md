# Leak Detection Device

*ENGI 120: Introduction to Engineering Design & Communication, Fall 2019*

Bavan Rajan, Marc Shen, Ananya Vaidya, & Claire Xu

## Problem Statement
Each year, Rice University wastes approximately 40 million gallons of water due to pipe leakage, and this costs the university up to $422,400 annually. The task was to design a portable leak-detecting device for sewer grates on Rice's campus. This device would alert Rice's Facilities Engineering & Planning department of water leaks in main pipelines, and would be accurate, durable, and easy to use.

## Components
- Raspberry Pi Model 3A+ (with case)
- Adafruit Mini USB Microphone
- 5k mAh Battery Pack
- SanDisk Ultra 16GB SD Card
- 90-degree USB cable
- Waterproof Polycarbonate Enclosure
- 6.55 cm steel carabiner
- 11.5 cm steel S-hook
- 1.524 meter steel chain
- 0.305 meter chain

## Capabilities
- Receiving and recording sound
  - sound data is saved as amplitude vs. time in a 5 minute .wav file
- Analyzing sound
  - FFT is used to convert data to amplitude vs. frequency
  - analyzes how much data falls within a given frequency range and determines if it meets the threshold set
- Sending a wireless notification to a mobile device
  - Pushbullet is used to communicate betweeen the Raspberry Pi and a mobile device
 
## Prototype Demonstration
https://www.youtube.com/watch?v=T0wH7zHn6ds

## Future Plans
- adjust threshold and frequency range based on testing
- implement methods of detecting other variables (eg. temperature, flow rate, moisture)
- implement better power source 
