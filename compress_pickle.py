import joblib

def create_compress_file():
    data = joblib.load("data_dict")
    joblib.dump(data, "data_dict_compressed.pkl", compress=3)