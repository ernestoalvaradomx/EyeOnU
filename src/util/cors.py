from flask import Flask
from flask_cors import CORS

class ConfigCORS:
    def __init__(self, app: Flask=None):
        self.app=app

    def configCors(self):
        CORS(self.app, resources={
            r"/*": {
                "origins": ["*"],
                "methods": ["*"],
                "allow_headers": ["Content-Type"]
            }
        })
