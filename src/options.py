"""Shared configuration for talking to the CodeProject.AI Server."""

from pathlib import Path

# Repository root (one level above src/)
REPO_DIR = Path(__file__).resolve().parent.parent


class Options:

    serverPort = 32168
    serverHost = "localhost"
    serverUrl  = f"http://{serverHost}:{serverPort}/v1/"

    # Latest camera frame, read by Node-RED to show on the dashboard
    framePath = REPO_DIR / "img.jpg"

    def endpoint(self, route) -> str:
        return self.serverUrl + route
