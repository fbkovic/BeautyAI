"""
Vercel Handler für FastAPI
"""
from api import app

# Vercel erwartet 'app' als Handler
handler = app

