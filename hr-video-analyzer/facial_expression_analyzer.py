"""
Facial Expression Analyzer for Interview Evaluation
Analyzes facial expressions to predict: Confidence, Authenticity, Leadership, Pressure Handling
"""

import os
import json
from typing import Dict, List, Tuple

# Try to import required libraries (optional)
try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    cv2 = None
    print("Warning: OpenCV not available. Facial expression analysis disabled.")

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    np = None
    print("Warning: NumPy not available. Facial expression analysis disabled.")

# Try to import deep learning libraries (optional)
try:
    import torch
    import torch.nn as nn
    from torchvision import transforms
    from PIL import Image
    import torchvision.models as models
    DL_AVAILABLE = True
except ImportError:
    DL_AVAILABLE = False
    torch = None
    nn = None
    transforms = None
    Image = None
    models = None
    print("Warning: PyTorch/torchvision not available. Using rule-based fallback.")


# Only define model class if PyTorch is available
if DL_AVAILABLE:
    class FacialExpressionModel(nn.Module):
        """
        CNN model for predicting interview parameters from facial expressions.
        Uses transfer learning with a pre-trained ResNet backbone.
        """
        def __init__(self, num_outputs=4):
            super(FacialExpressionModel, self).__init__()
            # Use pre-trained ResNet18 as backbone
            try:
                # Try new PyTorch API first
                resnet = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
            except:
                try:
                    # Fallback to old API
                    resnet = models.resnet18(pretrained=True)
                except:
                    # If both fail, use untrained model
                    resnet = models.resnet18(pretrained=False)
            # Remove the final fully connected layer
            self.features = nn.Sequential(*list(resnet.children())[:-1])
            # Add custom head for our 4 parameters
            self.fc = nn.Sequential(
                nn.Linear(512, 256),
                nn.ReLU(),
                nn.Dropout(0.5),
                nn.Linear(256, 128),
                nn.ReLU(),
                nn.Dropout(0.3),
                nn.Linear(128, num_outputs),
                nn.Sigmoid()  # Output values between 0 and 1
            )
        
        def forward(self, x):
            x = self.features(x)
            x = x.view(x.size(0), -1)
            x = self.fc(x)
            return x
else:
    # Dummy class if PyTorch not available
    class FacialExpressionModel:
        def __init__(self, *args, **kwargs):
            pass


class FacialExpressionAnalyzer:
    """
    Analyzes facial expressions from video frames to evaluate interview parameters.
    """
    
    def __init__(self, model_path=None):
        self.model_path = model_path
        self.model = None
        
        if not CV2_AVAILABLE or cv2 is None:
            raise ImportError("OpenCV (cv2) is required for facial expression analysis. Install with: pip install opencv-python")
        
        if not NUMPY_AVAILABLE or np is None:
            raise ImportError("NumPy is required for facial expression analysis. Install with: pip install numpy")
        
        if DL_AVAILABLE and torch is not None:
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        else:
            self.device = None
            
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        # Image preprocessing for model (only if DL available)
        if DL_AVAILABLE:
            self.transform = transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                                   std=[0.229, 0.224, 0.225])
            ])
        else:
            self.transform = None
        
        # Initialize model if DL is available
        if DL_AVAILABLE and torch is not None:
            try:
                self.model = FacialExpressionModel(num_outputs=4)
                if model_path and os.path.exists(model_path):
                    try:
                        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
                        print(f"Loaded model from {model_path}")
                    except Exception as e:
                        print(f"Could not load model: {e}, using untrained model")
                self.model.to(self.device)
                self.model.eval()
            except Exception as e:
                print(f"Could not initialize model: {e}, using rule-based fallback")
                self.model = None
        else:
            self.model = None
            print("Using rule-based fallback for facial expression analysis")
    
    def detect_faces(self, frame) -> List[Tuple[int, int, int, int]]:
        """
        Detect faces in a frame.
        Returns list of (x, y, w, h) bounding boxes.
        """
        if not CV2_AVAILABLE:
            return []
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray, 
            scaleFactor=1.1, 
            minNeighbors=5, 
            minSize=(30, 30)
        )
        return faces.tolist()
    
    def extract_face_region(self, frame, bbox: Tuple[int, int, int, int]):
        """Extract and preprocess face region from frame."""
        if not CV2_AVAILABLE:
            return None
        x, y, w, h = bbox
        face = frame[y:y+h, x:x+w]
        return face
    
    def analyze_expression_ml(self, face_image) -> Dict[str, float]:
        """
        Analyze facial expression using ML model.
        Returns scores for: confidence, authenticity, leadership, pressure_handling
        """
        if not DL_AVAILABLE or self.model is None or self.transform is None:
            return self.analyze_expression_rule_based(face_image)
        
        try:
            # Convert BGR to RGB
            face_rgb = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
            face_pil = Image.fromarray(face_rgb)
            
            # Preprocess
            input_tensor = self.transform(face_pil).unsqueeze(0).to(self.device)
            
            # Predict
            with torch.no_grad():
                predictions = self.model(input_tensor)
                scores = predictions[0].cpu().numpy()
            
            return {
                'confidence': float(scores[0]),
                'authenticity': float(scores[1]),
                'leadership': float(scores[2]),
                'pressure_handling': float(scores[3])
            }
        except Exception as e:
            print(f"ML analysis error: {e}")
            import traceback
            traceback.print_exc()
            return self.analyze_expression_rule_based(face_image)
    
    def analyze_expression_rule_based(self, face_image) -> Dict[str, float]:
        """
        Rule-based fallback for facial expression analysis.
        Analyzes basic facial features to estimate parameters.
        """
        if face_image is None or not CV2_AVAILABLE or not NUMPY_AVAILABLE:
            # Return default scores if analysis not possible
            return {
                'confidence': 0.5,
                'authenticity': 0.5,
                'leadership': 0.5,
                'pressure_handling': 0.5
            }
        
        gray = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape
        
        # Analyze basic facial features
        # Eye region analysis (top 40% of face)
        eye_region = gray[0:int(h*0.4), :]
        eye_brightness = np.mean(eye_region) / 255.0
        
        # Mouth region analysis (bottom 30% of face)
        mouth_region = gray[int(h*0.7):, :]
        mouth_brightness = np.mean(mouth_region) / 255.0
        
        # Overall face symmetry (simplified)
        left_half = gray[:, :w//2]
        right_half = gray[:, w//2:]
        symmetry = 1.0 - abs(np.mean(left_half) - np.mean(right_half)) / 255.0
        
        # Head pose estimation (simplified - based on face position)
        face_center_x = w / 2
        center_offset = abs(face_center_x - w/2) / (w/2)
        head_straight = 1.0 - min(center_offset, 1.0)
        
        # Calculate parameter scores based on heuristics
        # These are placeholder calculations - should be replaced with trained model
        confidence = min(0.7, (eye_brightness * 0.5 + head_straight * 0.5))
        authenticity = min(0.75, (symmetry * 0.6 + head_straight * 0.4))
        leadership = min(0.65, (eye_brightness * 0.4 + head_straight * 0.6))
        pressure_handling = min(0.7, (symmetry * 0.5 + eye_brightness * 0.3 + head_straight * 0.2))
        
        return {
            'confidence': confidence,
            'authenticity': authenticity,
            'leadership': leadership,
            'pressure_handling': pressure_handling
        }
    
    def analyze_video_frames(self, frames_dir: str) -> Dict:
        """
        Analyze all frames in a directory and aggregate results.
        
        Args:
            frames_dir: Directory containing frame images
            
        Returns:
            Dictionary with aggregated scores and per-frame analysis
        """
        frame_files = sorted([
            f for f in os.listdir(frames_dir) 
            if f.lower().endswith(('.jpg', '.png', '.jpeg'))
        ])
        
        if not frame_files:
            return {
                'error': 'No frames found',
                'scores': {}
            }
        
        all_scores = {
            'confidence': [],
            'authenticity': [],
            'leadership': [],
            'pressure_handling': []
        }
        
        frame_analyses = []
        
        for frame_file in frame_files:
            frame_path = os.path.join(frames_dir, frame_file)
            if not CV2_AVAILABLE:
                continue
            frame = cv2.imread(frame_path)
            
            if frame is None:
                continue
            
            # Detect faces
            faces = self.detect_faces(frame)
            
            if not faces:
                continue
            
            # Analyze the largest face (assuming it's the candidate)
            largest_face = max(faces, key=lambda f: f[2] * f[3])
            face_region = self.extract_face_region(frame, largest_face)
            
            # Analyze expression
            scores = self.analyze_expression_ml(face_region)
            
            # Aggregate scores
            for key in all_scores:
                all_scores[key].append(scores[key])
            
            frame_analyses.append({
                'frame': frame_file,
                'face_bbox': largest_face,
                'scores': scores
            })
        
        if not all_scores['confidence']:
            return {
                'error': 'No faces detected in frames',
                'scores': {}
            }
        
        # Calculate average scores
        avg_scores = {
            'confidence': np.mean(all_scores['confidence']),
            'authenticity': np.mean(all_scores['authenticity']),
            'leadership': np.mean(all_scores['leadership']),
            'pressure_handling': np.mean(all_scores['pressure_handling'])
        }
        
        # Calculate overall score
        overall_score = np.mean(list(avg_scores.values()))
        
        return {
            'scores': {k: round(float(v), 3) for k, v in avg_scores.items()},
            'overall_score': round(float(overall_score), 3),
            'frame_count': len(frame_analyses),
            'frames_analyzed': len(frame_files),
            'frame_analyses': frame_analyses
        }


def download_pretrained_model(model_url: str, save_path: str):
    """
    Download a pre-trained model from a URL.
    This would typically download from a model repository.
    """
    try:
        import urllib.request
        print(f"Downloading model from {model_url}...")
        urllib.request.urlretrieve(model_url, save_path)
        print(f"Model saved to {save_path}")
        return True
    except Exception as e:
        print(f"Could not download model: {e}")
        return False

