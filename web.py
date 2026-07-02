import os

from flask import Flask, jsonify, render_template, request

app = Flask(__name__, static_folder="static", template_folder="templates")


def get_answer(question: str):
    from rag import answer_question

    return answer_question(question)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat")
def chat():
    return render_template("chat.html")


@app.route("/history")
def history():
    return render_template("history.html")


@app.route("/health")
def health():
    return jsonify({"status": "ok", "message": "CyberSec RAG Assistant is running"})


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(force=True)
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "Question cannot be empty."}), 400

    try:
        response = get_answer(question)
        return jsonify({
            "answer": response.answer,
            "sources": [
                {"filename": source.filename, "page": source.page}
                for source in response.sources
            ],
        })

    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(debug=False, host="0.0.0.0", port=port, use_reloader=False)
