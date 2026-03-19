import os
import sys
 
# Adicionar o diretório atual ao path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
 
from app import app
 
# Export the Flask app for Vercel
# Vercel entrypo
