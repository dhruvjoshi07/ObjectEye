# predict.py

import torch
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image
import numpy as np
import json
import os

# Load ImageNet class names
classes_file = os.path.join(os.path.dirname(__file__), 'imagenet_classes.json')
with open(classes_file, 'r') as f:
    class_names = json.load(f)

# Load pre-trained ResNet50 model
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# Using weights argument as pretrained=True is deprecated in torchvision
weights = models.ResNet50_Weights.DEFAULT
model = models.resnet50(weights=weights).to(device)
model.eval()

# Image preprocessing
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

def predict_image(image_path):
    """
    Predict object in image
    Returns: (object_name, confidence_score)
    """
    try:
        # Load and transform image
        image = Image.open(image_path).convert('RGB')
        image_tensor = transform(image).unsqueeze(0).to(device)
        
        # Get prediction
        with torch.no_grad():
            output = model(image_tensor)
        
        # Get top prediction
        probabilities = torch.nn.functional.softmax(output, dim=1)
        top_prob, top_class = torch.topk(probabilities, 1)
        
        predicted_class = top_class.item()
        confidence = float(top_prob[0][0].item()) * 100
        object_name = class_names[str(predicted_class)]
        
        return {
            "object": object_name,
            "confidence": round(confidence, 2),
            "status": "success"
        }
    
    except Exception as e:
        return {
            "error": str(e),
            "status": "error"
        }

def get_top_3_predictions(image_path):
    """Get top 3 predictions with confidence scores"""
    try:
        image = Image.open(image_path).convert('RGB')
        image_tensor = transform(image).unsqueeze(0).to(device)
        
        with torch.no_grad():
            output = model(image_tensor)
        
        probabilities = torch.nn.functional.softmax(output, dim=1)
        top_probs, top_classes = torch.topk(probabilities, 3)
        
        results = []
        for i in range(3):
            class_idx = top_classes[0][i].item()
            confidence = float(top_probs[0][i].item()) * 100
            object_name = class_names[str(class_idx)]
            results.append({
                "rank": i + 1,
                "object": object_name,
                "confidence": round(confidence, 2)
            })
        
        return results
    
    except Exception as e:
        return {"error": str(e)}
