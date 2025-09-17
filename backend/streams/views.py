from django.shortcuts import render, redirect, get_object_or_404
from django.http import StreamingHttpResponse
from .models import VideoStream, Camera
from .forms import VideoStreamForm
import cv2
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort

# تحميل نموذج YOLO مرة واحدة
yolo_model = YOLO("yolov8n.pt")  # نسخة Nano للسرعة

# تهيئة متتبع DeepSORT
tracker = DeepSort(max_age=30)

# قائمة كل الفيديوهات / البثوث
def stream_list(request):
    streams = VideoStream.objects.all().order_by('-uploaded_at')
    return render(request, "streams/list.html", {"streams": streams})

# رفع فيديو جديد
def upload_stream(request):
    if request.method == "POST":
        form = VideoStreamForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("stream_list")
    else:
        form = VideoStreamForm()
    return render(request, "streams/upload_video.html", {"form": form})

# تشغيل فيديو محدد مع كشف وتتبع الكائنات
def stream_detail(request, pk):
    stream = get_object_or_404(VideoStream, pk=pk)
    return render(request, "streams/stream_detail.html", {"stream": stream})

def video_feed(request, pk):
    stream = get_object_or_404(VideoStream, pk=pk)
    source = stream.camera.rtsp_url if stream.is_live else stream.uploaded_file.path
    cap = cv2.VideoCapture(source)

    def gen():
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = yolo_model.predict(source=rgb_frame, conf=0.5, verbose=False)

            detections = []
            for r in results:
                for box in r.boxes.xyxy:
                    x1, y1, x2, y2 = map(int, box)
                    detections.append(((x1, y1, x2, y2), 1.0, "person"))

            tracks = tracker.update_tracks(detections, frame=frame)
            for t in tracks:
                x1, y1, x2, y2 = map(int, t.to_xyxy())
                track_id = t.track_id
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f'ID:{track_id}', (x1, y1-5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)

            ret, jpeg = cv2.imencode('.jpg', frame)
            frame_bytes = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    return StreamingHttpResponse(gen(), content_type='multipart/x-mixed-replace; boundary=frame')
