# Facial Expression Analysis Model Training Guide

## Overview

This guide explains how to train a model to predict interview evaluation parameters (Confidence, Authenticity, Leadership, Pressure Handling) from facial expressions in video interviews.

## Model Architecture

The model uses:
- **Backbone**: Pre-trained ResNet18 (transfer learning)
- **Output**: 4 regression values (0-1) for each parameter
- **Input**: 224x224 RGB face images

## Training Data Requirements

### Option 1: Use Open-Source Datasets

Recommended datasets for facial expression analysis:

1. **FER2013** (Facial Expression Recognition 2013)
   - 35,887 grayscale images
   - 7 emotion categories
   - Download: https://www.kaggle.com/datasets/msambare/fer2013

2. **AffectNet**
   - Large-scale dataset with 1M+ images
   - 7 basic emotions + valence/arousal
   - Requires registration: http://mohammadmahoor.com/affectnet/

3. **EmotiW** (Emotion Recognition in the Wild)
   - Video-based emotion recognition
   - Good for interview scenarios
   - Download: https://sites.google.com/view/emotiw2019

### Option 2: Create Your Own Dataset

1. **Collect Interview Videos**
   - Record or collect interview videos
   - Ensure diverse candidates and scenarios

2. **Extract Frames**
   - Extract frames from videos
   - Detect and crop faces
   - Save face images

3. **Label the Data**
   - For each face image, label with scores (0-1) for:
     - Confidence
     - Authenticity
     - Leadership
     - Pressure Handling
   - Use multiple annotators for reliability

4. **Create Annotations File**

Create `annotations.json` in your data directory:

```json
[
  {
    "image_path": "images/face_001.jpg",
    "confidence": 0.8,
    "authenticity": 0.7,
    "leadership": 0.75,
    "pressure_handling": 0.65
  },
  {
    "image_path": "images/face_002.jpg",
    "confidence": 0.6,
    "authenticity": 0.8,
    "leadership": 0.5,
    "pressure_handling": 0.7
  }
]
```

## Training Steps

### 1. Prepare Data

```bash
# Create data directory structure
mkdir -p training_data/images
cd training_data

# Add your face images to the images/ folder
# Create annotations.json (see format above)
```

### 2. Create Template (Optional)

```bash
python train_facial_model.py --data_dir ./training_data --create_template
```

This creates a template `annotations.json` file that you can fill in.

### 3. Train the Model

```bash
python train_facial_model.py \
    --data_dir ./training_data \
    --epochs 50 \
    --batch_size 32 \
    --learning_rate 0.001 \
    --model_path facial_expression_model.pth
```

### 4. Use the Trained Model

After training, the model will be saved. Update `facial_expression_analyzer.py` to load it:

```python
analyzer = FacialExpressionAnalyzer(model_path='facial_expression_model.pth')
```

## Training Parameters

- **Epochs**: 50-100 (depending on dataset size)
- **Batch Size**: 32 (adjust based on GPU memory)
- **Learning Rate**: 0.001 (with step decay)
- **Optimizer**: Adam
- **Loss Function**: MSE (Mean Squared Error)

## Data Augmentation

The training script includes:
- Random horizontal flips
- Random rotations (±10 degrees)
- Color jitter (brightness/contrast)

## Evaluation Metrics

Monitor:
- **Training Loss**: Should decrease over epochs
- **Validation Loss**: Should decrease and converge
- **Best Model**: Saved when validation loss is lowest

## Tips for Better Results

1. **More Data**: Collect at least 1000+ labeled images per parameter
2. **Diverse Data**: Include different:
   - Lighting conditions
   - Head poses
   - Facial expressions
   - Demographics
3. **Quality Labels**: Use multiple annotators and average scores
4. **Balanced Dataset**: Ensure balanced distribution of scores
5. **Fine-tuning**: Start with pre-trained weights (already included)

## Using Pre-trained Models

If you have access to pre-trained models from research papers:

1. Download the model weights
2. Adapt the model architecture if needed
3. Fine-tune on your interview dataset

## Troubleshooting

### Out of Memory
- Reduce batch size
- Use smaller image size
- Enable gradient checkpointing

### Poor Performance
- Increase training data
- Check label quality
- Adjust learning rate
- Try different architectures

### No Improvement
- Verify data quality
- Check for data leakage
- Ensure proper train/val split
- Monitor for overfitting

## Next Steps

1. Collect and label training data
2. Train the model
3. Evaluate on test set
4. Deploy the trained model
5. Continuously improve with more data

## References

- ResNet Paper: https://arxiv.org/abs/1512.03385
- FER2013 Dataset: https://www.kaggle.com/datasets/msambare/fer2013
- PyTorch Transfer Learning: https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html

