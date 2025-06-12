from apscheduler.schedulers.blocking import BlockingScheduler
import time

# Assuming main.py's post_latest_article is the function to schedule.
# We need to ensure it can be imported and run correctly.
# If main.py is structured as a script, we might need to refactor
# post_latest_article or parts of it into a more import-friendly module/function.

try:
    # Attempt to import from main, assuming it's in the same package
    from .main import post_latest_article
    from . import config # To ensure config is loaded
except ImportError:
    # Fallback for simpler structures or direct execution if PYTHONPATH is tricky
    # This implies that main.py and config.py are directly findable.
    # For robust packaging, the relative imports above are preferred.
    print("Scheduler: Falling back to direct imports (main, config). Ensure PYTHONPATH is set if issues occur.")
    try:
        import main as main_module # Alias to avoid conflict if scheduler itself is main
        post_latest_article = main_module.post_latest_article
        import config
    except ImportError as e:
        print(f"Scheduler: Critical - Could not import 'post_latest_article' from main or config. Error: {e}")
        print("Scheduler: Please ensure 'main.py' and 'config.py' are in the same directory or python path.")
        post_latest_article = None # Set to None to prevent scheduler from running with missing task
        config = None


# Schedule settings (can be moved to config.py later)
POSTING_INTERVAL_HOURS = 4 # Example: post every 4 hours

def scheduled_job():
    """The job that the scheduler will run."""
    print(f"Scheduler: Running scheduled job - {time.strftime('%Y-%m-%d %H:%M:%S')}")
    if post_latest_article:
        try:
            post_latest_article()
            print("Scheduler: 'post_latest_article' executed successfully.")
        except Exception as e:
            print(f"Scheduler: Error during scheduled execution of 'post_latest_article': {e}")
    else:
        print("Scheduler: 'post_latest_article' function not loaded. Cannot run scheduled job.")

if __name__ == '__main__':
    if not post_latest_article or not config:
        print("Scheduler: Exiting. Core components (post_latest_article or config) not loaded.")
    elif not config.X_API_KEY: # Check if API keys are likely missing
        print("Scheduler: WARNING - Twitter API keys not found in config.")
        print("Scheduler: The bot will run, but tweet posting will likely fail.")
        print("Scheduler: Please ensure your .env file is set up correctly in the 'twitter_bot' directory.")
        # Proceed to run the scheduler anyway, as it might be intentional for testing other parts

    if post_latest_article:
        print(f"Scheduler: Starting scheduler to run 'post_latest_article' every {POSTING_INTERVAL_HOURS} hours.")
        print("Scheduler: Press Ctrl+C to exit.")

        scheduler = BlockingScheduler(timezone="UTC") # Or your local timezone

        # Schedule the job
        scheduler.add_job(scheduled_job, 'interval', hours=POSTING_INTERVAL_HOURS)

        # For testing, you might want a shorter interval, e.g., minutes=1
        # scheduler.add_job(scheduled_job, 'interval', minutes=1)

        try:
            scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            print("Scheduler: Shutting down...")
        except Exception as e:
            print(f"Scheduler: An unexpected error occurred: {e}")
    else:
        print("Scheduler: Not starting due to missing 'post_latest_article' function.")
