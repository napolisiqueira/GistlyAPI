from flask import Flask
from routes import app as gystly_blueprint
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

# Cria a pasta de uploads se não existir
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

app.register_blueprint(gystly_blueprint)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
