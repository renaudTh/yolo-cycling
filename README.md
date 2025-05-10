# Cycling frame plate

This project is a complete pipeline for detecting and processing cycling frame plates in images. It includes:

1. **Image Scraping**: A Python script (`download_images.py`) that uses Scrapy to scrape cycling event images from a professional photograph website.
2. **Dataset Preparation**: A script (`split_dataset.py`) to split annotated (with imgLabel) datasets into training and validation sets for YOLO model training.
3. **Model Training and Export**: A script (`train_export.py`) to train a YOLOv8 model on the prepared dataset and export it to ONNX format.
4. **Inference**: A JavaScript-based web interface (`index.html` and `inference.js`) for running inference on uploaded images using the trained ONNX model.

