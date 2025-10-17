import joblib


def compress_simi():
    com_simi = joblib.load("similarity.pkl")
    joblib.dump(com_simi, "compressed_similarity.pkl", compress=5)
