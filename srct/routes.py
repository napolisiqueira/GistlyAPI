from flask import Blueprint, request, current_app, jsonify
from werkzeug.utils import secure_filename
from http import HTTPStatus
from services import transcribe_and_summarize
from utils import allowed_file
import os

app = Blueprint("gystly", __name__, url_prefix="/gystli")

@app.route("/upload_video", methods=["POST"])
def upload_video():
    if "video" not in request.files:
        return jsonify({"erro": "Nenhum arquivo de vídeo enviado"}), HTTPStatus.BAD_REQUEST

    video = request.files["video"]

    if video.filename == "":
        return jsonify({"erro": "Nome de arquivo vazio"}), HTTPStatus.BAD_REQUEST

    if not allowed_file(video.filename):
        return jsonify({"erro": "Tipo de vídeo não suportado"}), HTTPStatus.UNSUPPORTED_MEDIA_TYPE

    filename = secure_filename(video.filename)
    filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    video.save(filepath)

    result, status = transcribe_and_summarize(filepath, filename)
    return jsonify(result), status
