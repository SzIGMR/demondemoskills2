"""Minimal FastAPI application exposing configuration management.

The application provides endpoints to read and update the configuration managed
by :mod:`di_core.config`.  A small HTML page is served at the root path to allow
editing the configuration in a browser.

Run with::

    uvicorn di_core.web:app --reload
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from di_core.config import config_manager


app = FastAPI(title="di.core config")


@app.get("/config")
def get_config():
    """Return the current configuration as JSON."""

    return config_manager.config


@app.post("/config")
def update_config(data: dict):
    """Update the configuration with the provided data."""

    return config_manager.update(data)


@app.get("/", response_class=HTMLResponse)
def index():
    """Very small HTML UI for editing the configuration."""

    return """
    <html>
      <body>
        <h1>Configuration</h1>
        <form id="form">
          <textarea id="cfg" rows="20" cols="80"></textarea><br/>
          <button type="submit">Save</button>
        </form>
        <script>
          async function load() {
            const data = await fetch('/config').then(r => r.json());
            document.getElementById('cfg').value = JSON.stringify(data, null, 2);
          }
          load();
          document.getElementById('form').onsubmit = async (e) => {
            e.preventDefault();
            const data = JSON.parse(document.getElementById('cfg').value);
            await fetch('/config', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data)});
            alert('saved');
          };
        </script>
      </body>
    </html>
    """

