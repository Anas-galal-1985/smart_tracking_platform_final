# wanted/utils.py
from deepface import DeepFace
import numpy as np

def extract_face_embedding(image_path):
    # استخراج بصمة الوجه
    embedding = DeepFace.represent(img_path=image_path, model_name='Facenet', enforce_detection=True)
    return embedding[0]["embedding"]  # قائمة الأرقام
