from dotenv import load_dotenv
import os
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'ganyaniq')

# API
API_HOST = os.environ.get('API_HOST', '0.0.0.0')
API_PORT = int(os.environ.get('API_PORT', '8001'))

# Data paths
DATA_DIR = ROOT_DIR / 'data'
DATA_DIR.mkdir(exist_ok=True)
