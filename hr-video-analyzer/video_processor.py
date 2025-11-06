import os
import json

# OpenCV is required for video processing
try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    cv2 = None
    print("ERROR: OpenCV (cv2) is required but not installed.")
    print("Install with: pip install opencv-python")

# Optional imports for transcription and evaluation
try:
    import audio_transcriber
    import candidate_evaluator
    TRANSCRIPTION_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Transcription features not available: {e}")
    TRANSCRIPTION_AVAILABLE = False
    audio_transcriber = None
    candidate_evaluator = None

# Import facial expression analyzer
try:
    import facial_expression_analyzer
    FACIAL_ANALYSIS_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Facial expression analysis module not available: {e}")
    FACIAL_ANALYSIS_AVAILABLE = False
    facial_expression_analyzer = None


def extract_frames(video_path, out_folder="frames", step=30):
    """Extract frames from a video every `step` frames and save to out_folder.

    Returns the number of saved frames and the output folder path.
    """
    if not CV2_AVAILABLE:
        raise ImportError("OpenCV (cv2) is required for video processing. Install with: pip install opencv-python")
    
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
    if not CV2_AVAILABLE:
        raise ImportError("OpenCV (cv2) is required for face detection. Install with: pip install opencv-python")
    
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


def process_video(video_path, step=30, work_dir="work", transcribe_audio=True):
    """High-level helper: extract frames, analyze them, transcribe audio, and evaluate candidate.

    Returns path to results JSON and dict of results.
    """
    os.makedirs(work_dir, exist_ok=True)
    frames_dir = os.path.join(work_dir, "frames")
    annotated_dir = os.path.join(work_dir, "annotated")

    # Extract frames and analyze
    _, frames_out = extract_frames(video_path, out_folder=frames_dir, step=step)
    frame_results = analyze_frames(frames_out, annotated_folder=annotated_dir)
    
    # Initialize results dict
    results = {
        "frame_analysis": frame_results,
        "transcription": None,
        "evaluation": None,
        "facial_expression_analysis": None
    }
    
    # Analyze facial expressions for interview parameters
    if FACIAL_ANALYSIS_AVAILABLE:
        try:
            print("Analyzing facial expressions...")
            analyzer = facial_expression_analyzer.FacialExpressionAnalyzer()
            facial_analysis = analyzer.analyze_video_frames(frames_out)
            results["facial_expression_analysis"] = facial_analysis
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"Warning: Facial expression analysis failed: {e}")
            print(f"Error details: {error_details}")
            results["facial_analysis_error"] = str(e)
            # Don't fail the entire video processing if facial analysis fails
            results["facial_expression_analysis"] = None
    
    # Transcribe audio and evaluate candidate
    if transcribe_audio:
        if not TRANSCRIPTION_AVAILABLE:
            results["transcription_error"] = "Transcription dependencies not installed. Please install: pip install openai-whisper ffmpeg-python torch"
            results["evaluation_error"] = "Evaluation requires transcription"
        else:
            try:
                print("Transcribing audio from video...")
                transcriber = audio_transcriber.AudioTranscriber(model_size="base")
                transcription = transcriber.transcribe(video_path)
                results["transcription"] = transcription
                
                # Evaluate candidate based on transcribed text
                if transcription.get("text"):
                    print("Evaluating candidate...")
                    evaluator = candidate_evaluator.CandidateEvaluator()
                    evaluation = evaluator.evaluate(transcription["text"])
                    results["evaluation"] = evaluation
            except Exception as e:
                import traceback
                error_details = traceback.format_exc()
                print(f"Warning: Transcription/evaluation failed: {e}")
                print(f"Error details: {error_details}")
                results["transcription_error"] = str(e)
                results["evaluation_error"] = str(e)

    results_path = os.path.join(work_dir, "results.json")
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"Wrote results to {results_path}")
    return results_path, results
