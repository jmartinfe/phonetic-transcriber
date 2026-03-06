# English Phonetic Transcriber for Spanish Speakers

A transcriber that converts English text into a phonetic approximation designed to be read using Spanish pronunciation rules, allowing Spanish speakers to reproduce the original English pronunciation more easily.

The tool also provides IPA transcription and a text-to-speech playback option.

## Example

Input:

I have a house

IPA:

aɪ hæv ə haʊs

Spanish-like transcription:

ai jav a jaus

## Purpose

This project is intended as an informal aid for English learners who are native Spanish speakers or who know enough Spanish to read text using Spanish pronunciation rules.

The goal is pragmatic rather than academic. The transcriptions are designed to help users approximate English pronunciation quickly and intuitively rather than provide linguistically perfect phonetic analysis.

## Tech Stack

* Python
* FastAPI
* Pytest

Pronunciations are derived from the CMU Pronouncing Dictionary and converted from ARPAbet to IPA and a Spanish-readable transcription.

## Design Principles

* Maintain a clean and solid architecture while keeping the stack simple and appropriate for the size of the project
* Avoid unnecessary complexity
* Keep the user experience as simple as possible (no accounts, no extra clicks, no advertisements)
* The literal transcription is the core feature; everything else revolves around it
* Clearly separate the service layer, API layer, and frontend
* No database is used since the resources are small enough to be managed in memory
* Data files are loaded at startup into optimized in-memory structures

## Roadmap

* Define transcription rules
* Implement data loading and transcription services
* Expose the API endpoint
* Implement and connect the frontend

## Why this exists

This repository is a new version of an Android app I created early in my career while learning mobile development.

At the time I built it mostly as a personal experiment and did not expect it to reach many users. Surprisingly, the app eventually reached more than 250,000 downloads before it was retired from the store.

That experience suggested that many people were looking for a simple way to approximate English pronunciation using Spanish spelling.

This project revisits the same idea in a simpler and more open form: a small web tool with a clear architecture and an openly available implementation.

If you find it useful or have suggestions to improve it, feedback is always welcome.

[jmartinfe@gmail.com](mailto:jmartinfe@gmail.com)
