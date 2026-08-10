# GirlMath
[🌐 View on Devpost](https://devpost.com/software/girlmath-b5y7ao) • [🎥 Watch the Demo](https://www.youtube.com/watch?v=r2qMN9JFBvw)         

<img width="395" height="748" alt="image" src="https://github.com/user-attachments/assets/166c88da-5844-4edb-9dd9-44145663ee94" />
<img width="394" height="747" alt="image" src="https://github.com/user-attachments/assets/79eb2890-9af4-429d-87a7-d36a0de1806a" />

GirlMath is a mobile app built at ElleHacks 2026 to help girls build confidence in math and STEM through reflection, progress tracking, and personalized AI guidance.

The app allows users to complete regular confidence check-ins, write journal entries about their experiences with STEM, and visualize their progress over time. An AI mentor can use this history to provide guidance based on patterns in the user’s past reflections and check-ins.

This repository contains the Python backend for GirlMath. The mobile frontend is available at https://github.com/nomix21/ellehacks26. 

Features

* Journal & reflection tracking – Store and retrieve journal entries about a user’s experiences learning STEM.
* Confidence check-ins – Record questionnaire responses to track changes in confidence, motivation, and learning experiences over time.
* Personalized AI mentor – Uses Google Gemini to provide guidance based on the user’s current concern and, with permission, patterns from previous journal entries and check-ins.
* AI-generated journal themes – Generates short themes from journal entries to summarize important moments and patterns.
* Progress visualization data – Stores and connects user progress data used by the frontend’s star and constellation visualizations.

Stack

Backend

* Python
* FastAPI
* MongoDB
* Google Gemini API
  
Frontend

* React Native
* Expo
* TypeScript

Architecture

The backend is separated into several layers:

girlmath/
├── ai/          # Gemini integration and AI processing
├── api/         # FastAPI endpoints
├── db/          # MongoDB connection and data access
├── entities/    # Application data models
└── use_case/    # Application logic

User journals and questionnaire responses are persisted in MongoDB and can be retrieved by the application when needed. The AI layer can combine a user’s current message with selected historical data to generate more personalized guidance while allowing the user to control whether their journal or questionnaire history is included.

Frontend

The GirlMath mobile interface was built separately using React Native, Expo, and TypeScript.

Project Status

GirlMath was developed as a hackathon project for ElleHacks 2026. The original hosted backend and database are no longer active, so the application is not currently available as a live deployment.
