//   function drawImageToCanvas(imageDataUrl, canvas) {
//     const img = new Image();
//     img.onload = () => {
//       const ratio = img.width / img.height;
//       const maxWidth = dropArea.clientWidth;
//       canvas.width = maxWidth;
//       canvas.height = maxWidth / ratio;
//       ctx.clearRect(0, 0, canvas.width, canvas.height);
//       ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
//     };
//     img.onerror = () =>
//       console.error("Erreur lors du chargement de l'image");
//     img.src = dataUrl;
//   }
const RESIZE = 640;

function loadImage(file, rescaled = false) {
  return new Promise((resolve, reject) => {
    const image = new Image();
    image.onload = () => {
      if (rescaled) {
        const canvas = document.createElement("canvas");
        canvas.width = RESIZE;
        canvas.height = RESIZE;
        const ctx = canvas.getContext("2d");
        ctx.drawImage(image, 0, 0, RESIZE, RESIZE);
        resolve(canvas.toDataURL());
      } else {
        resolve(URL.createObjectURL(file));
      }
    };
    image.onerror = reject;
    image.src = URL.createObjectURL(file);
  });
}

function draw(canvas, dataUrl, detections) {
  const img = new Image();
  img.onload = () => {
    canvas.width = img.naturalWidth;
    canvas.height = img.naturalHeight;
    const ctx = canvas.getContext("2d");
    ctx.drawImage(img, 0, 0);
    const scaleX = canvas.width / RESIZE;
    const scaleY = canvas.height / RESIZE;

    ctx.strokeStyle = "lime";
    ctx.lineWidth = 2;
    ctx.font = "14px sans-serif";
    ctx.fillStyle = "lime";

    detections.forEach((det) => {
      let [x1, y1, x2, y2] = det.bbox;
      x1 *= scaleX;
      y1 *= scaleY;
      x2 *= scaleX;
      y2 *= scaleY;

      ctx.strokeRect(x1, y1, x2 - x1, y2 - y1);
      ctx.fillText(`${det.classId} ${det.score.toFixed(2)}`, x1, y1 - 5);
    });
  };
  img.onerror = () => console.error("Erreur lors du chargement de l'image");
  img.src = dataUrl;
}
function parseResult(output) {
  const detections = [];
  const data = output.data;
  const dims = output.dims;

  for (let i = 0; i < dims[2]; i++) {
    const x = data[0 * dims[2] + i];
    const y = data[1 * dims[2] + i];
    const w = data[2 * dims[2] + i];
    const h = data[3 * dims[2] + i];
    const score = data[4 * dims[2] + i];
    if (score < 0.5) continue;

    const x1 = x - w / 2;
    const y1 = y - h / 2;
    const x2 = x + w / 2;
    const y2 = y + h / 2;

    detections.push({
      bbox: [x1, y1, x2, y2],
      score: score,
      classId: "frame_plate",
    });
  }

  return detections;
}
function computeIoU(boxA, boxB) {
  const [x1A, y1A, x2A, y2A] = boxA;
  const [x1B, y1B, x2B, y2B] = boxB;

  const xLeft = Math.max(x1A, x1B);
  const yTop = Math.max(y1A, y1B);
  const xRight = Math.min(x2A, x2B);
  const yBottom = Math.min(y2A, y2B);

  if (xRight < xLeft || yBottom < yTop) return 0.0;

  const interArea = (xRight - xLeft) * (yBottom - yTop);
  const boxAArea = (x2A - x1A) * (y2A - y1A);
  const boxBArea = (x2B - x1B) * (y2B - y1B);
  return interArea / (boxAArea + boxBArea - interArea);
}
function nonMaxSuppression(detections, iouThreshold = 0.5) {
  const keep = [];
  detections.sort((a, b) => b.score - a.score);
  while (detections.length > 0) {
    const current = detections.shift();
    keep.push(current);

    detections = detections.filter((det) => {
      const iou = computeIoU(current.bbox, det.bbox);
      return iou < iouThreshold;
    });
  }

  return keep;
}
