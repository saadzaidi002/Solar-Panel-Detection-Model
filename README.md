<div align="center">
  <h1>☀️ Solar Panel Detection Model (YOLOv8-OBB)</h1>
  <p>An automated, high-accuracy deep learning system to detect solar panels in aerial imagery.</p>

  <a href="https://huggingface.co/spaces/smsaad001/solarpanel">
    <img src="https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Live%20Demo-blue?style=for-the-badge&logo=huggingface" alt="Live Demo">
  </a>
  <a href="https://colab.research.google.com/">
    <img src="https://img.shields.io/badge/Google%20Colab-Training%20Ready-F9AB00?style=for-the-badge&logo=googlecolab" alt="Google Colab">
  </a>
  <img src="https://img.shields.io/badge/YOLOv8-Ultralytics-00ffff?style=for-the-badge&logo=yolo" alt="YOLOv8">
</div>

<br/>

## 🚀 Try it Live
The model is deployed and fully interactive online! You can upload your own aerial images and see the detections in real-time.
👉 **[Click here to try the Live Demo on Hugging Face Spaces](https://huggingface.co/spaces/smsaad001/solarpanel)**

---

## 📊 Results & Performance
Our model was trained on a custom dataset using Google Colab's T4 GPUs, achieving extremely high confidence scores even in dense urban environments.

*Here are some real-time detection results from the live web app:*

<div align="center">
  <img src="./Result%201.png" alt="Detection Result 1" width="45%">
  <img src="./Result%202.png" alt="Detection Result 2" width="45%">
  <br/>
  <img src="./Result%203.png" alt="Detection Result 3" width="45%">
</div>

### 🎥 Live Video Demonstration
Check out the model detecting solar panels in real-time below:

<video src="./Solarpanel%20-%20a%20Hugging%20Face%20Space%20by%20smsaad001%20-%20Google%20Chrome%202026-07-11%2003-50-10.mp4" controls="controls" width="100%"></video>

---

## 🛠️ Project Features
- **State-of-the-art Detection:** Utilizes Ultralytics YOLOv8-OBB (Oriented Bounding Boxes) for precise detection of angled solar panels.
- **GPU Optimized:** Full training pipeline optimized for Google Colab.
- **Live Web Interface:** Fully integrated with Gradio for instant web-based inference.
- **Automated Deployment:** Code is structured to deploy seamlessly to Hugging Face Spaces with a single click.

---

## 💻 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/smsaad001/Solar-Panel-Detection-Model.git
   cd Solar-Panel-Detection-Model
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install ultralytics gradio opencv-python-headless
   ```

3. **Run the local Web App:**
   ```bash
   python app.py
   ```
   *The app will be available at `http://localhost:7860`*

---

## 🧠 How to Train the Model Yourself

Don't have a powerful GPU? No problem. This repository includes everything you need to train the model for free on Google Colab.

1. Download the `colab_upload.zip` file from this repository.
2. Extract it locally.
3. Upload `Solar_Panel_Training.ipynb` to [Google Colab](https://colab.research.google.com/).
4. Make sure your runtime is set to **T4 GPU**.
5. Drag and drop the `dataset.zip` into the Colab files panel.
6. Run all cells! The notebook will automatically unzip the dataset, train the YOLOv8 model, and even push the final app directly to your Hugging Face Space.

---

## 📂 Repository Structure
- `dataset/`: Training, validation, and testing images (YAML configurations included).
- `Solar_Panel_Training.ipynb`: The complete Colab pipeline for training and Hugging Face deployment.
- `app.py` & `templates/`: Local Flask/Gradio web interfaces.
- `colab_upload.zip`: The bundled training environment ready for Google Colab.
- `best.pt`: The highly optimized, pre-trained YOLOv8 weights (Stored on Hugging Face).

<div align="center">
  <i>Developed by smsaad001</i>
</div>
