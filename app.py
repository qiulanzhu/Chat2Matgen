from flask import Flask, Response, request, send_from_directory
from flask_cors import CORS  # 引入 CORS
import json
from main import run
from loguru import logger

app = Flask(__name__, static_folder='public')

# 启用跨域支持
CORS(app, resources={r"/*": {"origins": "*"}})  # 允许所有源进行跨域请求

# 首页接口
@app.route("/")
def home():
    return send_from_directory("templates", "index.html")

@app.route('/get_answer', methods=['POST'])
def get_answer():
    query = request.json.get('query', 'hi')
    logger.info(f"query: {query}")

    def generate():
        for content_piece in run(query):
            yield 'data: ' + json.dumps({
                'data': content_piece,
                "status": 1, "message": 'Succeed'}, ensure_ascii=False) + '\n\n'

    return Response(generate(), content_type="text/event-stream")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8200)
