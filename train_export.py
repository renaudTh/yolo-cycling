# /// script
# requires-python = ">=3.8"
# dependencies = ['ultralytics', 'onnx>=1.12.0', 'onnxslim>=0.1.46', 'onnxruntime']
# ///

from ultralytics import YOLO
from pathlib import Path

def train():
    model = YOLO("yolov8n.pt")
    model.train(
        data="dataset_yolo_v1/frame_plate.yaml",
        epochs=50,
        imgsz=640,
        batch=16,
        name="yolo_frame_plate",
        project="runs/train",
        verbose=True
    )

def export_onnx(model_path: Path):
    model = YOLO(model_path)
    model.export(format="onnx", opset=12)