
from flask import Flask, jsonify, render_template, request
from retriever import search_faq

app = Flask(__name__)


# ==============================
# HALAMAN UTAMA
# ==============================
@app.route("/")
def index():
    page = request.args.get("page", "chat")

    if page not in ("chat", "history"):
        page = "chat"

    return render_template("index.html", page=page)


# ==============================
# CEK STATUS SERVER
# ==============================
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


# ==============================
# API CHATBOT
# ==============================
@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()

    if not message:
        return jsonify({
            "error": "Pertanyaan tidak boleh kosong."
        }), 400

    try:
        result = search_faq(message)

        return jsonify({
            "question": message,
            "answer": result["answer"],
            "results": result.get("results", [])
        })

    except Exception as error:
        app.logger.exception("Terjadi kesalahan pada chatbot")

        return jsonify({
            "error": "Maaf, terjadi kesalahan saat mencari jawaban. Silakan coba lagi."
        }), 500


# ==============================
# JALANKAN SERVER
# ==============================
if __name__ == "__main__":
    app.run(debug=True)
