"""Simple FastAPI app for viewing detection results."""
from __future__ import annotations

import base64

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, Response

from di_base_client.client import DiBaseClient
from di_core.config import config_manager


dbase = DiBaseClient(path=config_manager.config.database.path)
app = FastAPI(title="di.core results")


@app.get("/screws")
def get_screws():
    """Return stored screw positions."""
    return dbase.get("screws", {})


@app.get("/image")
def get_image():
    """Return the stored camera image or 404 if missing."""
    entry = dbase.get("camera_image")
    if not entry:
        return Response(status_code=404)
    data = base64.b64decode(entry.get("data", ""))
    fmt = entry.get("format", "png")
    return Response(content=data, media_type=f"image/{fmt}")


@app.get("/", response_class=HTMLResponse)
def index():
    """Display the image with simple screw annotations."""
    return """
    <html>
      <body>
        <h1>Detection Viewer</h1>
        <canvas id=\"canvas\"></canvas>
        <pre id=\"coords\"></pre>
        <script>
          async function load() {
            const imgResp = await fetch('/image');
            if (!imgResp.ok) {
              document.body.innerHTML += '<p>No image available</p>';
              return;
            }
            const blob = await imgResp.blob();
            const img = await createImageBitmap(blob);
            const canvas = document.getElementById('canvas');
            canvas.width = img.width;
            canvas.height = img.height;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(img, 0, 0);
            const screws = await fetch('/screws').then(r => r.json());
            document.getElementById('coords').textContent = JSON.stringify(screws, null, 2);
            ctx.fillStyle = 'red';
            ctx.strokeStyle = 'red';
            for (const id in screws) {
              const s = screws[id];
              const x = s.x; const y = s.y;
              ctx.beginPath();
              ctx.arc(x, y, 5, 0, 2*Math.PI);
              ctx.fill();
              ctx.fillText(id, x + 6, y + 6);
            }
          }
          load();
        </script>
      </body>
    </html>
    """
