# Twitter News Bot (Moria Project)

This project is a Python-based Twitter bot designed to share news and interact with users, focusing on topics like data, data quality, data resiliency, and data foundations for AI projects.

## Features (Planned & In-Progress)

*   Posts content from specified sources (initially RSS feeds).
*   Automated posting via a scheduler.
*   (Future) Interaction with users via mentions/DMs.
*   (Future) More advanced content generation/curation.

## Project Structure

```
twitter_bot/
├── main.py             # Manual trigger for posting, can be used for testing.
├── config.py           # Handles loading of API keys and configurations.
├── twitter_client.py   # Manages all interactions with the X/Twitter API.
├── content_manager.py  # Fetches, processes, and selects content.
├── scheduler.py        # Runs the bot on a schedule (main entry point for automated operation).
├── requirements.txt    # Project dependencies.
├── .env_example        # Example for environment variable configuration.
├── .env                # Local environment variables (ignored by Git).
└── README.md           # This file.
```

## Setup Instructions

1.  **Clone the Repository (if applicable)**
    ```bash
    # git clone <repository_url>
    # cd twitter_bot_directory_or_project_root
    ```
    (If working locally, ensure you are in the `twitter_bot` directory or its parent)

2.  **Create a Virtual Environment**
    It's highly recommended to use a virtual environment to manage project dependencies.
    ```bash
    python -m venv venv
    ```
    Activate the virtual environment:
    *   On Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    *   On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

3.  **Install Dependencies**
    With the virtual environment activated, install the required packages:
    ```bash
    pip install -r twitter_bot/requirements.txt
    ```
    (If you are already inside the `twitter_bot` directory, just use `pip install -r requirements.txt`)

4.  **Configure Environment Variables**
    *   Copy the example environment file:
        ```bash
        cp twitter_bot/.env_example twitter_bot/.env
        ```
        (Adjust paths if you are in a different working directory)
    *   Edit the newly created `twitter_bot/.env` file and fill in your X/Twitter API credentials:
        ```
        X_API_KEY="YOUR_X_API_KEY"
        X_API_SECRET_KEY="YOUR_X_API_SECRET_KEY"
        X_ACCESS_TOKEN="YOUR_X_ACCESS_TOKEN"
        X_ACCESS_TOKEN_SECRET="YOUR_X_ACCESS_TOKEN_SECRET"
        BOT_LOG_LEVEL="INFO"
        ```
    *   You may also want to update the `DEFAULT_RSS_FEEDS` list in `twitter_bot/content_manager.py` with your preferred news sources.

## Running the Bot

*   **To run the bot continuously with the scheduler:**
    Ensure your virtual environment is active and you are in the parent directory of `twitter_bot` or have `twitter_bot` in your `PYTHONPATH`.
    ```bash
    python -m twitter_bot.scheduler
    ```
    Or, if you are inside the `twitter_bot` directory:
    ```bash
    python scheduler.py
    ```
    The bot will then post at the interval defined in `scheduler.py`. Press `Ctrl+C` to stop.

*   **To perform a single test post (manual trigger):**
    This will fetch the latest article from the configured RSS feeds and attempt to post it once.
    Ensure your virtual environment is active.
    ```bash
    python -m twitter_bot.main
    ```
    Or, if you are inside the `twitter_bot` directory:
    ```bash
    python main.py
    ```

## Development Notes
*   The bot currently posts the first article fetched from the combined RSS feeds.
*   Error handling is basic; more robust logging and error management can be added.
*   Remember to add new dependencies to `requirements.txt`:
    ```bash
    pip freeze > twitter_bot/requirements.txt
    ```
    (Or manually edit the file)
