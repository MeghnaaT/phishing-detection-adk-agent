# Phishing Detection AI Agent (ADK + Gemini)

## Overview
This project implements a single AI agent using Google Agent Development Kit (ADK) and Gemini, deployed on Cloud Run.

The agent performs one clearly defined task: **classifying input text as Safe, Suspicious, or Phishing**.

---

## Features
- Text classification using Gemini (gemini-2.0-flash)
- HTTP API endpoint for real-time inference
- Cloud-native deployment on Google Cloud Run
- Lightweight, single-agent architecture

---

## How It Works
1. User sends text input via HTTP POST request
2. The agent processes the input using Gemini
3. The response classifies the message risk level

---

## API Usage

```bash
curl -X POST <YOUR_CLOUD_RUN_URL>/run \
-H "Content-Type: application/json" \
-d '{
  "app_name": "zoo_guide",
  "user_id": "test-user",
  "session_id": "test-session",
  "input": "Click this link to reset your password"
}'
## Example Output
This looks like a phishing attempt.

## Tech Stack
Google ADK (Agent Development Kit)
Gemini (gemini-2.0-flash)
Google Cloud Run

## Future Improvements
URL scanning support
Email phishing detection integration
Browser extension for real-time alerts
Dashboard for monitoring threats

## Live Demo: https://zoo-tour-guide-25684765582.europe-west1.run.app/dev-ui/?app=cyber_log_check&session=98a338e9-3def-4aee-a088-931156b143e2

Author: Meghna Tiwari

