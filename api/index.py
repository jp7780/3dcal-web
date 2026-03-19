from app import app

# Export the Flask app for Vercel
handler = app

# Also export as 'app' for compatibility
app = app
