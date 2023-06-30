import os

env_path = os.path.join(os.path.dirname(__file__), os.getenv('ENV_FILE') or ".env_development")
data_path = "L:\Escuela\Tesis\pythonProject\datasets"

VERSION = os.environ.get("VERSION")

APP_HOST = os.environ.get("HOST")
APP_PORT = os.environ.get("PORT")
APP_DEBUG = bool(os.environ.get("DEBUG"))
