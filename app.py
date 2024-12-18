from flask import Flask, Response, request, send_from_directory
import json
from api.openai_api import llm_chat_stream  # Assuming this is your streaming function

app = Flask(__name__)

# 首页接口
@app.route("/")
def home():
    return send_from_directory("templates", "index.html")

@app.route('/get_answer', methods=['POST'])
def get_answer():
    query = request.json.get('query', 'hi')

    def generate():
        for content_piece in llm_chat_stream(prompt=query):
            yield 'data: ' + json.dumps({
                'data': content_piece,
                "status": 1, "message": 'Succeed'}, ensure_ascii=False) + '\n\n'

    return Response(generate(), content_type="text/event-stream")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8200)
