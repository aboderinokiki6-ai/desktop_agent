 🧠 LLM Desktop Automation Agent (Agentic AI Proof of Work)

## Overview

This project is a *real-world agentic AI system** that uses a **Large Language Model (LLM)** combined with **local tools** to autonomously automate desktop tasks on **Windows**.

The agent monitors the **Downloads folder**, reasons about newly downloaded files using an LLM (Gemini), and takes actions such as:
- Categorizing files
- Renaming files intelligently
- Moving files into structured folders
- Logging every action with reasoning

This demonstrates true **agentic behavior**:

goal interpretation → decision making → tool usage → execution → logging

---

## Why This Is Agentic AI (Not Just a Script)

Unlike traditional automation scripts with fixed rules, this system:
- Uses an **LLM as the decision engine**
- Dynamically decides what action to take
- Calls **tools** to interact with the real file system
- Explains *why* each action was taken
- Maintains a full execution log

This matches modern **tool-using AI agents** used in real production systems.

---

## Real-World Automation Use Case

### What the agent does:
- Watches the **Downloads** folder in real time
- When a new file appears, the agent:
  1. Extracts file metadata (name, extension, size)
  2. Sends context to the LLM
  3. Receives a decision (move / rename / skip)
  4. Executes the action using file-system tools
  5. Logs the action with timestamp and reasoning

### Example transformations

| Before | After |
|------|------|
| `cvfinalfinal(1).pdf` | `Documents/CV_Aboderin_Okiki.pdf` |
| `IMG_20260202_083012.jpg` | `Pictures/Receipt_Jumia_2026-02-02.jpg` |
| `setup(3).exe` | `Installers/VSCodeSetup.exe` |

---

## Project Structure
desktop_agent/
│
├── main.py # Entry point (watches Downloads folder)
├── agent.py # Core agent logic (LLM decisions + tools)
├── llm_gemini.py # Gemini LLM integration
├── tools.py # File-system tools
├── config.py # Configuration (folders, DRY_RUN)
├── outputs/
│ └── activity_log.md
└── README.md


---

## Technology Stack

- Python 3.9+
- Gemini LLM (via API)
- watchdog (file system monitoring)
- Standard Python libraries (os, shutil, datetime, etc.)

---

## Installation (Windows)

### Install dependencies
```bat
pip install google-generativeai watchdog
