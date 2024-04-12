import os
import socket
from src import create_app

if os.getenv("FLASK_DEBUG") == "development":
    app = create_app("config.DevConfig")
else:
    app = create_app("config.ProdConfig")

ip_address = socket.gethostbyname(socket.gethostname())

if __name__ == "__main__":
    app.run(debug=True, host=ip_address)
