"""
Training Script for Facial Expression Analysis Model
Trains a model to predict: Confidence, Authenticity, Leadership, Pressure Handling
from facial expressions in interview videos.

This script uses open-source datasets and transfer learning to train the model.
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
import numpy as np
import os
import json
from facial_expression_analyzer import FacialExpressionModel
import argparse


class InterviewExpressionDataset(Dataset):
    """
    Dataset for training facial expression analysis model.
    Expects images in folders organized by parameter scores.
    """
    def __init__(self, data_dir, transform=None):
        self.data_dir = data_dir
        self.transform = transform
        self.samples = []
        
        # Load annotations (JSON file with image paths and scores)
        annotations_path = os.path.join(data_dir, 'annotations.json')
        if os.path.exists(annotations_path):
            with open(annotations_path, 'r') as f:
                annotations = json.load(f)
                for ann in annotations:
                    img_path = os.path.join(data_dir, ann['image_path'])
                    if os.path.exists(img_path):
                        self.samples.append({
                            'image': img_path,
                            'confidence': ann['confidence'],
                            'authenticity': ann['authenticity'],
                            'leadership': ann['leadership'],
                            'pressure_handling': ann['pressure_handling']
                        })
    
    def __len__(self):
        return len(self.samples)
    
    def __getitem__(self, idx):
        sample = self.samples[idx]
        image = Image.open(sample['image']).convert('RGB')
        
        if self.transform:
            image = self.transform(image)
        
        labels = torch.tensor([
            sample['confidence'],
            sample['authenticity'],
            sample['leadership'],
            sample['pressure_handling']
        ], dtype=torch.float32)
        
        return image, labels


def create_sample_annotations(data_dir, output_file='annotations.json'):
    """
    Create a sample annotations file structure.
    This is a template - you'll need to label your training data.
    """
    annotations = []
    
    # Example structure - replace with your actual labeled data
    # For each image, you need to provide scores (0-1) for each parameter
    sample_structure = {
        'image_path': 'images/sample1.jpg',
        'confidence': 0.8,
        'authenticity': 0.7,
        'leadership': 0.75,
        'pressure_handling': 0.65
    }
    
    annotations_path = os.path.join(data_dir, output_file)
    with open(annotations_path, 'w') as f:
        json.dump(annotations, f, indent=2)
    
    print(f"Created sample annotations file at {annotations_path}")
    print("Please add your labeled training data to this file.")


def train_model(data_dir, epochs=50, batch_size=32, learning_rate=0.001, model_save_path='facial_expression_model.pth'):
    """
    Train the facial expression analysis model.
    
    Args:
        data_dir: Directory containing training data and annotations.json
        epochs: Number of training epochs
        batch_size: Batch size for training
        learning_rate: Learning rate for optimizer
        model_save_path: Path to save trained model
    """
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    # Data transforms
    train_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(10),
        transforms.ColorJitter(brightness=0.2, contrast=0.2),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                           std=[0.229, 0.224, 0.225])
    ])
    
    # Create dataset and dataloader
    dataset = InterviewExpressionDataset(data_dir, transform=train_transform)
    
    if len(dataset) == 0:
        print("Error: No training data found!")
        print("Please create annotations.json with your labeled data.")
        return
    
    # Split into train and validation (80/20)
    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size
    train_dataset, val_dataset = torch.utils.data.random_split(
        dataset, [train_size, val_size]
    )
    
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
    
    # Initialize model
    model = FacialExpressionModel(num_outputs=4)
    model.to(device)
    
    # Loss and optimizer
    criterion = nn.MSELoss()  # Mean Squared Error for regression
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.1)
    
    # Training loop
    best_val_loss = float('inf')
    
    for epoch in range(epochs):
        # Training phase
        model.train()
        train_loss = 0.0
        for images, labels in train_loader:
            images = images.to(device)
            labels = labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
        
        # Validation phase
        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for images, labels in val_loader:
                images = images.to(device)
                labels = labels.to(device)
                
                outputs = model(images)
                loss = criterion(outputs, labels)
                val_loss += loss.item()
        
        train_loss /= len(train_loader)
        val_loss /= len(val_loader)
        
        print(f'Epoch [{epoch+1}/{epochs}], Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}')
        
        # Save best model
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            torch.save(model.state_dict(), model_save_path)
            print(f'Model saved to {model_save_path}')
        
        scheduler.step()
    
    print(f"Training complete! Best validation loss: {best_val_loss:.4f}")
    print(f"Model saved to: {model_save_path}")


def main():
    parser = argparse.ArgumentParser(description='Train Facial Expression Analysis Model')
    parser.add_argument('--data_dir', type=str, required=True,
                       help='Directory containing training data and annotations.json')
    parser.add_argument('--epochs', type=int, default=50,
                       help='Number of training epochs')
    parser.add_argument('--batch_size', type=int, default=32,
                       help='Batch size for training')
    parser.add_argument('--learning_rate', type=float, default=0.001,
                       help='Learning rate')
    parser.add_argument('--model_path', type=str, default='facial_expression_model.pth',
                       help='Path to save trained model')
    parser.add_argument('--create_template', action='store_true',
                       help='Create a template annotations.json file')
    
    args = parser.parse_args()
    
    if args.create_template:
        create_sample_annotations(args.data_dir)
        return
    
    train_model(
        args.data_dir,
        epochs=args.epochs,
        batch_size=args.batch_size,
        learning_rate=args.learning_rate,
        model_save_path=args.model_path
    )


if __name__ == '__main__':
    main()

