"""
SolarVision AI — Flask Web Application
Solar Panel Detection & Change Detection using YOLOv8-OBB
"""

import os
import time
import cv2
import numpy as np
from flask import Flask, render_template, request, jsonify, url_for
from werkzeug.utils import secure_filename
from PIL import Image

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max upload
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'tiff', 'tif', 'bmp', 'webp'}

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.join('static', 'results'), exist_ok=True)

# ---------- MODEL LOADING ----------
model = None
model_available = False

def load_model():
    """Load the YOLOv8 OBB model. Try custom weights first, then fallback to pretrained."""
    global model, model_available
    try:
        from ultralytics import YOLO

        # Try custom trained weights first
        import glob
        weight_files = glob.glob(os.path.join('runs', 'obb', '*', 'weights', 'best.pt'))
        if weight_files:
            # Sort by modification time to get the latest trained model
            custom_weights = max(weight_files, key=os.path.getctime)
            model = YOLO(custom_weights)
            model_available = True
            print(f"✅ Loaded custom model from: {custom_weights}")
        else:
            # Fallback to pretrained OBB model
            model = YOLO("yolov8n-obb.pt")
            model_available = True
            print("⚠️ Custom weights not found. Using pretrained yolov8n-obb.pt")
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        model = None
        model_available = False

# Load on startup
load_model()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ---------- ROUTES ----------

@app.route('/')
def index():
    """Overview page — why solar panel detection matters, how it works."""
    return render_template('index.html')


@app.route('/model')
def model_page():
    """Model detection page — upload and detect solar panels."""
    return render_template('model.html', model_available=model_available)


@app.route('/about')
def about():
    """About page — developer and project information."""
    return render_template('about.html')


@app.route('/detect', methods=['POST'])
def detect():
    """API endpoint: run YOLOv8 OBB detection on uploaded image."""
    if model is None:
        return jsonify({
            'success': False,
            'error': 'Model not loaded. Please ensure ultralytics is installed and restart the server.'
        }), 500

    if 'image' not in request.files:
        return jsonify({'success': False, 'error': 'No image file provided.'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected.'}), 400

    if not allowed_file(file.filename):
        return jsonify({'success': False, 'error': 'Unsupported file type.'}), 400

    try:
        # Save uploaded image
        filename = secure_filename(file.filename)
        timestamp = int(time.time())
        save_name = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], save_name)
        file.save(filepath)

        # Run detection
        start_time = time.time()
        results = model.predict(source=filepath, conf=0.4, iou=0.45, save=False)
        processing_time = round(time.time() - start_time, 2)

        result = results[0]

        # Count detections and get confidence scores
        panel_count = 0
        confidences = []

        # Read original image
        img = cv2.imread(filepath)

        if result.obb is not None and len(result.obb) > 0:
            for obb in result.obb:
                conf = obb.conf[0].item()
                confidences.append(conf)
                panel_count += 1

                # Draw OBB
                corners = obb.xyxyxyxy[0].cpu().numpy().astype(np.int32).reshape((-1, 1, 2))
                cv2.polylines(img, [corners], isClosed=True, color=(0, 255, 0), thickness=2)

                # Draw confidence label
                cx = int(corners[:, 0, 0].mean())
                cy = int(corners[:, 0, 1].mean())
                label = f"{conf:.2f}"
                (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                cv2.rectangle(img, (cx - tw//2 - 4, cy - th - 8), (cx + tw//2 + 4, cy + 2), (0, 255, 0), -1)
                cv2.putText(img, label, (cx - tw//2, cy - 4),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

        avg_confidence = round(np.mean(confidences) * 100, 1) if confidences else 0

        # Save result image
        result_filename = f"result_{save_name}"
        result_path = os.path.join('static', 'results', result_filename)
        cv2.imwrite(result_path, img)

        return jsonify({
            'success': True,
            'result_image': url_for('static', filename=f'results/{result_filename}'),
            'panel_count': panel_count,
            'avg_confidence': avg_confidence,
            'processing_time': processing_time,
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("  ☀️  SolarVision AI — Solar Panel Detection Web App")
    print("=" * 60)
    print(f"  Model loaded: {'✅ Yes' if model_available else '❌ No'}")
    print(f"  Starting server at: http://127.0.0.1:5000")
    print("=" * 60 + "\n")
    app.run(debug=True, use_reloader=False, host='127.0.0.1', port=5000)
