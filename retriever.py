
from pathlib import Path
import re

import joblib
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


# ==================================================
# 1. KONFIGURASI LOKASI PROYEK
# ==================================================

ROOT_DIR = Path(__file__).resolve().parent

MODEL_DIR = ROOT_DIR / "models"
ARTIFACT_DIR = ROOT_DIR / "artifacts"
DATA_DIR = ROOT_DIR / "data"


# ==================================================
# 2. MEMUAT MODEL DAN DATA
# ==================================================

vectorizer = joblib.load(
    MODEL_DIR / "tfidf_vectorizer.joblib"
)

tfidf_matrix = joblib.load(
    MODEL_DIR / "tfidf_matrix.joblib"
)

metadata = joblib.load(
    ARTIFACT_DIR / "tfidf_metadata.joblib"
)

train_data = pd.read_csv(
    DATA_DIR / "processed" / "train_queries.csv"
)

faq_data = pd.read_csv(
    DATA_DIR / "raw" / "faq_academic.csv"
)


# ==================================================
# 3. VALIDASI DATA
# ==================================================

if len(train_data) != tfidf_matrix.shape[0]:
    raise ValueError(
        "Jumlah data training tidak cocok dengan matriks TF-IDF."
    )

if train_data["faq_id"].astype(str).tolist() != [
    str(item) for item in metadata["faq_ids"]
]:
    raise ValueError(
        "Urutan FAQ tidak cocok dengan metadata model."
    )

faq_data["faq_id"] = faq_data["faq_id"].astype(str)


# ==================================================
# 4. PREPROCESSING PERTANYAAN
# ==================================================

def preprocess(text):
    """Membersihkan teks sebelum pencarian FAQ."""

    text = str(text).lower().strip()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text


# ==================================================
# 5. PENCARIAN FAQ
# ==================================================

def search_faq(question, top_k=3):
    """Mengambil FAQ berdasarkan kemiripan cosine similarity."""

    question = preprocess(question)

    if not question:
        return {
            "answer": None,
            "results": []
        }

    query_vector = vectorizer.transform([question])

    # Pertanyaan tanpa kata yang dikenali model
    if query_vector.nnz == 0:
        return {
            "answer": (
                "Maaf, pertanyaan belum dapat dipahami. "
                "Coba gunakan kata-kata yang berkaitan dengan "
                "layanan akademik."
            ),
            "results": []
        }

    scores = cosine_similarity(
        query_vector,
        tfidf_matrix
    ).ravel()

    # Ambang awal agar hasil yang terlalu lemah ditolak
    MIN_SCORE = 0.20

    if scores.max() < MIN_SCORE:
        return {
            "answer": (
                "Maaf, saya belum menemukan jawaban yang cukup relevan. "
                "Coba tuliskan pertanyaan akademik dengan lebih jelas."
            ),
            "results": []
        }

    ranked_indices = scores.argsort()[::-1]

    results = []
    seen_faq_ids = set()

    for idx in ranked_indices:
        score = float(scores[idx])

        # Berhenti jika hasil berikutnya terlalu lemah
        if score < MIN_SCORE:
            break

        faq_id = str(train_data.iloc[idx]["faq_id"])

        # Hindari FAQ yang sama muncul berulang kali
        if faq_id in seen_faq_ids:
            continue

        faq_match = faq_data[
            faq_data["faq_id"] == faq_id
        ]

        if faq_match.empty:
            continue

        faq = faq_match.iloc[0]

        results.append({
            "faq_id": faq_id,
            "question": str(faq["question"]),
            "answer": str(faq["answer"]),
            "category": str(faq["category"]),
            "score": round(score, 4)
        })

        seen_faq_ids.add(faq_id)

        if len(results) >= max(1, int(top_k)):
            break

    if not results:
        return {
            "answer": (
                "Maaf, saya belum menemukan jawaban yang relevan."
            ),
            "results": []
        }

    return {
        "answer": results[0]["answer"],
        "results": results
    }
