import uvicorn
import signal
import sys
import logging
from .main import app

def main():
    config = uvicorn.Config(
        app, 
        host="0.0.0.0", 
        port=8099, 
        log_level="info",
        access_log=False
    )
    server = uvicorn.Server(config)

    # Signal handler for graceful shutdown (Criteriu #5)
    def handle_signal(sig, frame):
        logging.info(f"Received signal {sig}, shutting down...")
        server.should_exit = True

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    server.run()

if __name__ == "__main__":
    main()
