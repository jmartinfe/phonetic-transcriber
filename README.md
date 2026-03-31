# Text Processing API – Phonetic Transcription

A backend service that processes input text and returns structured phonetic representations, including IPA and a Spanish-readable approximation.

Originally inspired by a mobile app that reached 250,000+ downloads, this project revisits the same idea with a simpler and more maintainable backend-focused approach.

---

## What this does

Given an input sentence, the API:

- Parses the text into individual words  
- Retrieves pronunciation data  
- Returns structured phonetic output (IPA + Spanish-like transcription)  

Example:

Input:
I have a house

Output:
- IPA: aɪ hæv ə haʊs  
- Spanish-like: ai jav a jaus  

---

## What this demonstrates

This project focuses on building a backend service that:

- Processes and transforms input data into structured output  
- Defines clear and predictable API contracts  
- Handles text parsing and domain-specific logic  
- Is designed for extensibility (formatting layer, frontend integration)  

It reflects how I approach building APIs for data processing and automation use cases.

---

## Use cases

This type of service can be adapted for:

- Text processing pipelines  
- Data transformation APIs  
- NLP-related tools  
- Backend services that require structured output from raw input  

---

## Tech Stack

- Python  
- FastAPI  
- Pytest  

Pronunciation data is based on the CMU Pronouncing Dictionary and transformed into multiple output formats.

---

## Design approach

- Clear separation between API layer and processing logic  
- Focus on simple and predictable input/output behavior  
- In-memory data handling for performance and simplicity  
- Incremental development with a working API at each stage  

---

## Status

Work in progress:
- Core API is functional  
- Formatted text universalized for any consumer included
- Frontend is planned next  

---

## Why this exists

This project builds on a previous mobile application I developed early in my career, which unexpectedly reached over 250,000 users.

It is now reimagined as a backend service, focusing on clarity, simplicity and maintainability, while keeping the original goal: making pronunciation more accessible through practical tools.
