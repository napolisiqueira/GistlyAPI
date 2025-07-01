from flask import Blueprint, request, current_app
from http import HTTPStatus
from make_transcription import get_tw
from src.main import allowed_file
from werkzeug.utils import secure_filename
import os


app = Blueprint("gystly", __name__, url_prefix="/gystli")


@app.route("/upload_video", methods=["POST"])
def upload_video():
    if "video" not in request.files:
        return {"erro": "Nenhum arquivo de vídeo enviado"}, HTTPStatus.NO_CONTENT

    video = request.files["video"]

    if video.filename == "":
        return {"erro": "Nome de arquivo vazio"}, HTTPStatus.BAD_REQUEST

    if not allowed_file(video.filename):
        return {"erro": "Tipo de vídeo não suportado"}, HTTPStatus.UNSUPPORTED_MEDIA_TYPE

    filename = secure_filename(video.filename)
    filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)

    video.save(filepath)

    return get_tw(audio_file_path=filepath, audio_file_name=video.filename), HTTPStatus.OK
