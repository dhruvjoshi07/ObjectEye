# app.py

from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
from predict import predict_image, get_top_3_predictions
from PIL import Image

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Create uploads folder if not exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Upload image and get prediction"""
    
    # Check if file is in request
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    
    # Check if file is selected
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    # Check if file is allowed
    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed. Use: PNG, JPG, JPEG, GIF, WEBP"}), 400
    
    try:
        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Validate image
        try:
            img = Image.open(filepath)
            img.verify()
        except:
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({"error": "Invalid image file"}), 400
        
        # Get prediction
        result = predict_image(filepath)
        
        # Clean up
        if os.path.exists(filepath):
            os.remove(filepath)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/predict-top3', methods=['POST'])
def predict_top3():
    """Get top 3 predictions"""
    
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file"}), 400
    
    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Validate image
        try:
            img = Image.open(filepath)
            img.verify()
        except:
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({"error": "Invalid image file"}), 400
        
        # Get top 3 predictions
        results = get_top_3_predictions(filepath)
        
        # Clean up
        if os.path.exists(filepath):
            os.remove(filepath)
        
        return jsonify({"predictions": results})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({"status": "OK"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
