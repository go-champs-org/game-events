import logging


# Setup logging configuration and create a global logger
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(), logging.FileHandler("app.log")],
    )


# Create a logger instance
setup_logging()  # Call this to initialize the configuration
logger = logging.getLogger(__name__)
