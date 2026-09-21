import sys
import os
import socket
import threading
import tempfile
import tkinter as tk
from tkinter import filedialog
from flask import Flask, jsonify, request, send_from_directory, render_template_string, redirect
from werkzeug.utils import secure_filename
import webview

app = Flask(__name__)

def get_base_path():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

# Temp folders for holding files before approval
TEMP_SEND_DIR = os.path.join(tempfile.gettempdir(), "FastShareSendCache")
TEMP_INCOMING_DIR = os.path.join(tempfile.gettempdir(), "FastShareIncomingCache")
os.makedirs(TEMP_SEND_DIR, exist_ok=True)
os.makedirs(TEMP_INCOMING_DIR, exist_ok=True)

DEFAULT_DEST = os.path.join(os.path.expanduser("~"), "Desktop", "ReceivedFiles")
os.makedirs(DEFAULT_DEST, exist_ok=True)

APP_STATE = {
    "mode": "HOME",
    "destination": DEFAULT_DEST,
    "server_url": "",
    "selected_files": [],      # PC -> Mobile send queue
    "incoming_requests": []    # Mobile -> PC staging queue awaiting approval
}

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

# --- MOBILE HTML TEMPLATES ---

HTML_MOBILE_SEND = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fast Share - Send Files</title>
    <style>
        body { background: #0f172a; color: #f8fafc; font-family: -apple-system, sans-serif; padding: 20px; text-align: center; }
        .card { background: #1e293b; border-radius: 12px; padding: 20px; max-width: 400px; margin: 20px auto; box-shadow: 0 10px 25px rgba(0,0,0,0.3); }
        .drop-zone { border: 2px dashed #2563eb; padding: 30px 15px; border-radius: 8px; margin-bottom: 15px; cursor: pointer; background: rgba(37,99,235,0.05); }
        .btn { background: #2563eb; color: white; border: none; padding: 14px; width: 100%; border-radius: 8px; font-weight: bold; font-size: 1rem; cursor: pointer; }
        .btn:disabled { opacity: 0.5; }
        .file-list { margin-bottom: 15px; text-align: left; font-size: 0.85rem; max-height: 150px; overflow-y: auto; }
        .file-item { padding: 6px 10px; background: rgba(255,255,255,0.05); margin-bottom: 4px; border-radius: 4px; }
        .status-msg { font-size: 0.85rem; color: #38bdf8; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="card">
        <h3 style="margin-bottom:10px;">📤 Fast Share to PC</h3>
        <p style="color:#94a3b8; margin-bottom:15px; font-size:0.85rem;">Select files to send for PC verification.</p>
        <div class="drop-zone" onclick="document.getElementById('fileInput').click()">
            <div style="font-size: 2.5rem;">📁</div>
            <div style="margin-top:8px; font-weight:bold;">Tap to Select Files</div>
            <input type="file" id="fileInput" multiple style="display:none;" onchange="updateList(event)">
        </div>
        <div id="fileNames" class="file-list"></div>
        <button class="btn" id="sendBtn" disabled onclick="upload()">🚀 Send to PC Host</button>
        <div id="status" class="status-msg"></div>
    </div>

    <script>
        let selectedFiles = [];
        function updateList(e) {
            selectedFiles = Array.from(e.target.files);
            document.getElementById('sendBtn').disabled = selectedFiles.length === 0;
            document.getElementById('fileNames').innerHTML = selectedFiles.map(f => `<div class="file-item">• ${f.name} (${(f.size/1024/1024).toFixed(2)} MB)</div>`).join('');
            document.getElementById('status').innerText = '';
        }
        async function upload() {
            const btn = document.getElementById('sendBtn');
            const status = document.getElementById('status');
            btn.innerText = "Sending to PC...";
            btn.disabled = true;

            const formData = new FormData();
            selectedFiles.forEach(f => formData.append('files', f));
            
            try {
                const res = await fetch('/api/upload', { method: 'POST', body: formData });
                if(res.ok) {
                    status.innerText = 'Sent! Waiting for PC host to review and accept...';
                    selectedFiles = [];
                    document.getElementById('fileNames').innerHTML = '';
                    btn.innerText = "🚀 Send More Files";
                } else {
                    alert('Upload failed or host PC is not accepting files.');
                    btn.disabled = false;
                    btn.innerText = "🚀 Send to PC Host";
                }
            } catch(e) {
                alert('Connection error during upload.');
                btn.disabled = false;
                btn.innerText = "🚀 Send to PC Host";
            }
        }

        async function monitorMode() {
            try {
                const res = await fetch('/api/status');
                const data = await res.json();
                if (data.mode !== 'RECEIVE') {
                    window.location.href = '/connect';
                }
            } catch(e) {}
        }
        setInterval(monitorMode, 1500);
    </script>
</body>
</html>
"""

HTML_MOBILE_RECEIVE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fast Share - Receive Files</title>
    <style>
        body { background: #0f172a; color: #f8fafc; font-family: -apple-system, sans-serif; padding: 20px; text-align: center; }
        .card { background: #1e293b; border-radius: 12px; padding: 20px; max-width: 400px; margin: 20px auto; box-shadow: 0 10px 25px rgba(0,0,0,0.3); }
        .file-item { background: rgba(255,255,255,0.05); padding: 10px; border-radius: 6px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; text-align: left; }
        .dl-btn { background: #16a34a; color: white; padding: 8px 14px; border-radius: 6px; text-decoration: none; font-size: 0.85rem; font-weight: bold; }
    </style>
</head>
<body>
    <div class="card">
        <h3 style="margin-bottom:10px;">📥 Shared Files from PC</h3>
        <p style="color:#94a3b8; margin-bottom: 15px; font-size:0.85rem;">Live view of files shared by the Host PC.</p>
        <div id="fileContainer">Loading files...</div>
    </div>

    <script>
        async function loadFiles() {
            try {
                const statusRes = await fetch('/api/status');
                const statusData = await statusRes.json();
                if (statusData.mode !== 'SEND') {
                    window.location.href = '/connect';
                    return;
                }

                const res = await fetch('/api/send-files-list');
                if(!res.ok) {
                    window.location.href = '/connect';
                    return;
                }
                const data = await res.json();
                const container = document.getElementById('fileContainer');
                
                if(!data.files || data.files.length === 0) {
                    container.innerHTML = '<p style="color:#94a3b8; padding:20px;">No files shared by PC yet.</p>';
                    return;
                }
                
                container.innerHTML = data.files.map((f, idx) => `
                    <div class="file-item">
                        <div style="overflow:hidden; text-overflow:ellipsis; white-space:nowrap; max-width:200px;">
                            <div><strong>${f.name}</strong></div>
                            <div style="font-size:0.75rem; color:#94a3b8;">${(f.size/1024/1024).toFixed(2)} MB</div>
                        </div>
                        <a class="dl-btn" href="/download/${idx}" download>Download</a>
                    </div>
                `).join('');
            } catch(e) {}
        }
        loadFiles();
        setInterval(loadFiles, 2000);
    </script>
</body>
</html>
"""

HTML_MOBILE_WAIT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fast Share - Waiting</title>
    <style>
        body { background: #0f172a; color: #f8fafc; font-family: -apple-system, sans-serif; padding: 20px; text-align: center; }
        .card { background: #1e293b; border-radius: 12px; padding: 30px 20px; max-width: 400px; margin: 40px auto; box-shadow: 0 10px 25px rgba(0,0,0,0.3); }
        .spinner { border: 4px solid rgba(255,255,255,0.1); width: 40px; height: 40px; border-radius: 50%; border-left-color: #2563eb; animation: spin 1s linear infinite; margin: 20px auto; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
</head>
<body>
    <div class="card">
        <h3>⏳ Connected via Fast Share</h3>
        <div class="spinner"></div>
        <p style="color:#94a3b8; margin-top: 15px; font-size:0.9rem;">Waiting for host PC to select a mode...</p>
    </div>

    <script>
        async function checkState() {
            try {
                const res = await fetch('/api/status');
                const data = await res.json();
                if (data.mode === 'SEND') {
                    window.location.href = '/receive';
                } else if (data.mode === 'RECEIVE') {
                    window.location.href = '/send';
                }
            } catch(e) {}
        }
        setInterval(checkState, 1500);
    </script>
</body>
</html>
"""

# --- ROUTING ---

@app.route('/')
def pc_controller():
    html_path = os.path.join(get_base_path(), 'index.html')
    if os.path.exists(html_path):
        with open(html_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "<h3>Error: index.html not found on server</h3>", 404

@app.route('/connect')
def mobile_connect():
    if APP_STATE["mode"] == "SEND":
        return redirect('/receive')
    elif APP_STATE["mode"] == "RECEIVE":
        return redirect('/send')
    else:
        return render_template_string(HTML_MOBILE_WAIT)

@app.route('/send')
def route_send():
    if APP_STATE["mode"] != "RECEIVE":
        return redirect('/connect')
    return render_template_string(HTML_MOBILE_SEND)

@app.route('/receive')
def route_receive():
    if APP_STATE["mode"] != "SEND":
        return redirect('/connect')
    return render_template_string(HTML_MOBILE_RECEIVE)

# --- STATE APIS ---

@app.route('/api/status', methods=['GET'])
def get_status():
    host_ip = get_local_ip()
    port = 5000
    APP_STATE["server_url"] = f"http://{host_ip}:{port}/connect"
    return jsonify(APP_STATE)

@app.route('/api/set-mode', methods=['POST'])
def set_mode():
    data = request.json or {}
    new_mode = data.get('mode', 'HOME')
    APP_STATE['mode'] = new_mode
    if new_mode == 'HOME':
        APP_STATE['selected_files'] = []
        APP_STATE['incoming_requests'] = []
    return jsonify({"status": "success", "mode": APP_STATE['mode']})

@app.route('/api/select-send-files', methods=['POST'])
def select_send_files():
    data = request.json or {}
    select_type = data.get('type', 'files')
    
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    
    selected = []
    if select_type == 'folder':
        folder = filedialog.askdirectory(title="Select Folder to Send")
        if folder:
            for dirpath, _, filenames in os.walk(folder):
                for f in filenames:
                    selected.append(os.path.join(dirpath, f))
    else:
        files = filedialog.askopenfilenames(title="Select Files to Send")
        if files:
            selected = list(files)
            
    root.destroy()
    
    formatted_files = []
    for f_path in selected:
        if os.path.isfile(f_path):
            formatted_files.append({
                "path": f_path,
                "name": os.path.basename(f_path),
                "size": os.path.getsize(f_path)
            })
            
    APP_STATE['selected_files'].extend(formatted_files)
    return jsonify({"files": APP_STATE['selected_files']})

@app.route('/api/add-dropped-files', methods=['POST'])
def add_dropped_files():
    if 'files' not in request.files:
        return jsonify({"error": "No files"}), 400
        
    files = request.files.getlist('files')
    for file in files:
        if file.filename == '':
            continue
        filename = secure_filename(file.filename)
        save_path = os.path.join(TEMP_SEND_DIR, filename)
        file.save(save_path)
        
        APP_STATE['selected_files'].append({
            "path": save_path,
            "name": filename,
            "size": os.path.getsize(save_path)
        })
        
    return jsonify({"files": APP_STATE['selected_files']})

@app.route('/api/set-destination', methods=['POST'])
def set_destination():
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    selected_dir = filedialog.askdirectory(title="Select Destination Folder for Received Files")
    root.destroy()
    
    if selected_dir:
        APP_STATE["destination"] = selected_dir
    return jsonify({"destination": APP_STATE["destination"]})

# --- FILE TRANSFER & APPROVAL APIS ---

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if APP_STATE["mode"] != "RECEIVE":
        return jsonify({"error": "PC is not currently accepting incoming uploads."}), 403

    if 'files' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    files = request.files.getlist('files')
    staged = []

    for file in files:
        if file.filename == '':
            continue
        filename = secure_filename(file.filename)
        temp_path = os.path.join(TEMP_INCOMING_DIR, filename)
        file.save(temp_path)

        req_info = {
            "id": len(APP_STATE["incoming_requests"]),
            "name": filename,
            "size": os.path.getsize(temp_path),
            "temp_path": temp_path,
            "ext": os.path.splitext(filename)[1].lower()
        }
        APP_STATE["incoming_requests"].append(req_info)
        staged.append(filename)

    return jsonify({"message": "Files submitted to host PC for review", "files": staged})

@app.route('/api/respond-incoming', methods=['POST'])
def respond_incoming():
    data = request.json or {}
    req_id = data.get('id')
    action = data.get('action') # 'accept' or 'reject'

    found = None
    for item in APP_STATE["incoming_requests"]:
        if item["id"] == req_id:
            found = item
            break

    if not found:
        return jsonify({"error": "Item not found"}), 404

    if action == 'accept':
        dest_dir = APP_STATE["destination"]
        os.makedirs(dest_dir, exist_ok=True)
        final_path = os.path.join(dest_dir, found["name"])

        base, ext = os.path.splitext(found["name"])
        counter = 1
        while os.path.exists(final_path):
            final_path = os.path.join(dest_dir, f"{base}_{counter}{ext}")
            counter += 1

        os.replace(found["temp_path"], final_path)
    elif action == 'reject':
        if os.path.exists(found["temp_path"]):
            os.remove(found["temp_path"])

    APP_STATE["incoming_requests"] = [i for i in APP_STATE["incoming_requests"] if i["id"] != req_id]
    return jsonify({"status": "success", "incoming_requests": APP_STATE["incoming_requests"]})

@app.route('/api/send-files-list', methods=['GET'])
def get_send_files():
    if APP_STATE["mode"] != "SEND":
        return jsonify({"error": "PC is not currently sharing files."}), 403
    return jsonify({"files": APP_STATE['selected_files']})

@app.route('/download/<int:file_idx>', methods=['GET'])
def download_file(file_idx):
    if APP_STATE["mode"] != "SEND":
        return "Session Closed", 403

    if file_idx < 0 or file_idx >= len(APP_STATE['selected_files']):
        return "File not found", 404
        
    file_info = APP_STATE['selected_files'][file_idx]
    file_path = file_info['path']
    directory = os.path.dirname(file_path)
    filename = os.path.basename(file_path)
    
    return send_from_directory(directory, filename, as_attachment=True)

@app.route('/api/stop', methods=['POST'])
def stop_server():
    os._exit(0)

def start_flask():
    PORT = 5000
    host_ip = get_local_ip()
    APP_STATE["server_url"] = f"http://{host_ip}:{PORT}/connect"
    app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False)

if __name__ == '__main__':
    threading.Thread(target=start_flask, daemon=True).start()
    webview.create_window("Fast Share", "http://127.0.0.1:5000", width=500, height=720, resizable=False)
    webview.start()
