import cv2
import numpy as np
from retinaface import RetinaFace
from insightface.app import FaceAnalysis
from deep_sort_realtime.deepsort_tracker import DeepSort

# إعداد كشف الوجوه
detector = RetinaFace(quality='normal')
# إعداد التعرف على الوجوه
face_app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
face_app.prepare(ctx_id=0, nms=0.4)

# إعداد تتبع الأشخاص
deepsort = DeepSort(max_age=30)

# قاعدة بيانات مؤقتة للأشخاص (ID -> embedding)
person_db = {}

def process_frame(frame):
    # 1. كشف الوجوه
    faces = detector.predict(frame)
    embeddings = []
    for face in faces:
        x1, y1, x2, y2 = face['bbox']
        face_img = frame[int(y1):int(y2), int(x1):int(x2)]
        # استخراج embedding
        face_emb = face_app.get(face_img)[0].embedding
        embeddings.append((face_emb, (x1, y1, x2, y2)))
    
    # 2. تتبع الأشخاص عبر DeepSort
    bboxes = [bbox for _, bbox in embeddings]
    tracks = deepsort.update_tracks(bboxes, frame=frame)
    
    # 3. مقارنة بالـ DB لتحديد ID لكل شخص
    results = []
    for track, (emb, bbox) in zip(tracks, embeddings):
        track_id = track.track_id
        # حفظ أو تحديث الشخص الجديد
        person_db[track_id] = emb
        results.append({'id': track_id, 'bbox': bbox})
    
    return results
from streams.models import Person  # افترض أنك أنشأت نموذج Person

def save_person(track_id, embedding):
    # تحقق إذا موجود مسبقاً
    if not Person.objects.filter(track_id=track_id).exists():
        Person.objects.create(track_id=track_id, embedding=embedding.tolist())
