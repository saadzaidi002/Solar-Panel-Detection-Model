"""
Solar Panel Model Training Script
Downloads the Roboflow solar panel dataset and trains YOLOv8-OBB on it.
"""
import os
import sys

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["PYTHONIOENCODING"] = "utf-8"

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

print("=" * 60)
print("  Solar Panel Model - Training Pipeline")
print("=" * 60)

# Step 1: Using local dataset
print("\n[1/3] Using local solar panel dataset...")
data_yaml_path = os.path.abspath("dataset/data.yaml")
print(f"  Using dataset config at: {data_yaml_path}")

# Step 2: Train YOLOv8 OBB model
print("\n[2/3] Training YOLOv8n-OBB model (50 epochs)...")
print("  This will take some time depending on your hardware.\n")

from ultralytics import YOLO

model = YOLO("yolov8n-obb.pt")
model.train(
    data=data_yaml_path,
    epochs=50,
    imgsz=640,
    batch=8,
    patience=10,
    verbose=True,
)

# Step 3: Verify
weights_path = os.path.join("runs", "obb", "train", "weights", "best.pt")
if os.path.exists(weights_path):
    print(f"\n[3/3] Training complete! Weights saved to: {weights_path}")
    print("  Restart the web app to use the trained model.")
else:
    # Check other possible paths
    for root, dirs, files in os.walk("runs"):
        if "best.pt" in files:
            found = os.path.join(root, "best.pt")
            print(f"\n[3/3] Training complete! Weights saved to: {found}")
            break
    else:
        print("\n[3/3] Training finished but best.pt not found in expected location.")
        print("  Check the 'runs/' directory for your weights.")

print("\n" + "=" * 60)
print("  Training pipeline finished!")
print("=" * 60)
