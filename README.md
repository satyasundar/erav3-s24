# Telegram Agent Project

## Overview

The Telegram Agent project is a multi-component system designed to process and summarize links shared in Telegram groups. It consists of a backend server and a Chrome extension that work together to extract, summarize, and manage Telegram links.

## Features

- **Chrome Extension**: Scrapes messages from Telegram Web and sends them to the backend for processing.
- **Backend Server**: Processes the scraped messages, extracts links, summarizes them using an LLM, generates a PDF report, and optionally emails the report.
- **PDF Generation**: Creates a detailed PDF report of the summarized links.
- **Email Integration**: Sends the generated PDF report via email.

## Project Structure

```
README.md
backend/
    agent.py
    main.py
    requirements.txt
    telegram_links_summary.pdf
    utils.py
chrome-extension/
    content.js
    icon.png
    manifest.json
    popup.html
    popup.js
    styles.css
```

### Backend

- **`agent.py`**: Implements the main logic for processing prompts, extracting links, summarizing them, generating PDFs, and sending emails.
- **`main.py`**: Defines the FastAPI server and its endpoints.
- **`utils.py`**: Contains utility functions for link extraction, summarization, PDF generation, and email sending.
- **`requirements.txt`**: Lists the Python dependencies for the backend.

### Chrome Extension

- **`popup.html`**: The user interface for the extension.
- **`popup.js`**: Handles user interactions and communicates with the backend.
- **`content.js`**: Scrapes Telegram messages from the web interface.
- **`styles.css`**: Styles for the extension's popup UI.
- **`manifest.json`**: Defines the extension's metadata and permissions.

## Installation

### Backend

1. Clone the repository.
2. Navigate to the `backend/` directory.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the root directory and add your environment variables (e.g., `GEMINI_API_KEY`).
5. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

### Chrome Extension

1. Navigate to `chrome-extension/`.
2. Open Chrome and go to `chrome://extensions/`.
3. Enable "Developer mode".
4. Click "Load unpacked" and select the `chrome-extension/` folder.

## Usage

1. Open Telegram Web in Chrome.
2. Use the Chrome extension to scrape messages and send them to the backend.
3. The backend processes the messages and generates a PDF report.
4. Optionally, the PDF can be emailed to a specified address.

## Dependencies

### Backend

- `fastapi`
- `uvicorn`
- `openai`
- `fpdf`
- `smtplib`
- `python-dotenv`

### Chrome Extension

- Chrome browser with permissions for scripting and accessing Telegram Web.

## Environment Variables

Create a `.env` file in the root directory with the following variables:

- `GEMINI_API_KEY`: API key for the LLM.

## License

This project is licensed under the MIT License.
