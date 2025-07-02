import os
from app import create_app
from app.extensions import db

# Create the Flask application
app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Create database tables if they don't exist
        db.create_all()
        
    # Get configuration from environment
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 8080))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print(f"🚀 Starting AI IoT Tank Backend on http://{host}:{port}")
    print(f"🔧 Debug mode: {'ON' if debug else 'OFF'}")
    
    app.run(debug=debug, host=host, port=port)
