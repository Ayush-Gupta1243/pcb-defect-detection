from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import numpy as np
import cv2
import time
from pathlib import Path
from src.simplified_inspector import EnsembleInspector

app = FastAPI()

inspector = EnsembleInspector(
    patchcore_path="./models/phase1/simple_anomaly_detector.pkl",
    yolo_path="./models/phase2/yolov8_pcb_best.pt"
)

@app.get("/webcam", response_class=HTMLResponse)
async def webcam_page():
    html_path = Path(__file__).parent / "webcam_interface.html"
    return html_path.read_text(encoding="utf-8")
@app.post("/inspect")
async def inspect(file: UploadFile = File(...)):
    start = time.time()
    contents = await file.read()
    img_array = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    
    result = inspector.inspect(img)
    result["latency_ms"] = round((time.time() - start) * 1000)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8082)