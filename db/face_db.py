import faiss
import os

face_path = 'face.idx'


def load_index():
    if os.path.exists(face_path):
        return faiss.read_index(face_path)
    index = faiss.IndexFlatL2(128)
    faiss.write_index(index, face_path)
    return index
