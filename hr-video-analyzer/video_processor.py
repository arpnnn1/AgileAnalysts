import cv2
import os
import json


def extract_frames(video_path, out_folder="frames", step=30):
    """Extract frames from a video every `step` frames and save to out_folder.

    Returns the number of saved frames and the output folder path.
    """
    os.makedirs(out_folder, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    frame_num = 0
    img_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if frame_num % step == 0:  # Grab every `step`th frame
            path = os.path.join(out_folder, f'frame{img_count}.jpg')
            cv2.imwrite(path, frame)
            img_count += 1
        frame_num += 1
    cap.release()
    print(f"Saved {img_count} frames to {out_folder}")
    return img_count, out_folder


def analyze_frames(frames_folder, annotated_folder="annotated", cascade_path=None):
    """Run face detection on all frames in `frames_folder` and save annotated images.

    Uses OpenCV's Haarcascade frontal face detector by default. Returns a dict
    mapping frame filename -> list of detected bounding boxes.
    """
    os.makedirs(annotated_folder, exist_ok=True)
    if cascade_path is None:
        cascade_path = os.path.join(cv2.data.haarcascades, 'haarcascade_frontalface_default.xml')

    detector = cv2.CascadeClassifier(cascade_path)
    results = {}

    # List and sort frames for deterministic ordering
    frames = sorted([f for f in os.listdir(frames_folder) if f.lower().endswith(('.jpg', '.png'))])
    for fname in frames:
        path = os.path.join(frames_folder, fname)
        img = cv2.imread(path)
        if img is None:
            continue
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        bboxes = []
        for (x, y, w, h) in faces:
            bboxes.append({'x': int(x), 'y': int(y), 'w': int(w), 'h': int(h)})
            # draw rectangle on image
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        annotated_path = os.path.join(annotated_folder, f"annot_{fname}")
        cv2.imwrite(annotated_path, img)
        results[fname] = bboxes

    return results


def process_video(video_path, step=30, work_dir="work"):
    """High-level helper: extract frames, analyze them, and write a results.json.

    Returns path to results JSON and dict of results.
    """
    os.makedirs(work_dir, exist_ok=True)
    frames_dir = os.path.join(work_dir, "frames")
    annotated_dir = os.path.join(work_dir, "annotated")

    _, frames_out = extract_frames(video_path, out_folder=frames_dir, step=step)
    results = analyze_frames(frames_out, annotated_folder=annotated_dir)

    results_path = os.path.join(work_dir, "results.json")
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"Wrote results to {results_path}")
    return results_path, results
