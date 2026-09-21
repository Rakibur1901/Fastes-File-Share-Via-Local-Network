# Fast Share 🚀

**Fast Share** is a lightweight, cross-platform local file transfer application built with Python, Flask, and PyWebView. It allows fast, secure, and seamless file sharing between your PC and mobile devices over your local Wi-Fi network—no mobile app installation required!

**Developed by:** Md Rakibur Rahman Rafi

---

## 🔑 Key Features

* **Two-Way Transfer Modes:**
  * **Send Mode (PC ➔ Mobile):** Share single files or entire folders from your computer. Mobile users simply scan the QR code to view and download files directly in their web browser.
  * **Receive Mode (Mobile ➔ PC):** Send files directly from any phone or tablet straight to your PC.
* **Host Verification & Safety:** Incoming files from mobile devices require approval on the PC—allowing you to review file names and sizes before accepting or rejecting them.
* **Drag-and-Drop Support:** Drag files or folders directly into the PC app window to queue them instantly for sharing.
* **Custom Save Folder:** Easily select or change the destination directory on your PC for received transfers.
* **Zero Mobile Setup:** Mobile devices only need a web browser and a camera (to scan the QR code) connected to the same Wi-Fi network.

---

## 🛠️ How It Works

1. **Launch Fast Share:** Run `FastShare.exe` on your PC.
2. **Connect Mobile Device:** Scan the generated **QR Code** using your phone's camera to open the connection link.
3. **Choose Mode:**
   * **To Send Files to Mobile:** Click **Send to Mobile / Device**, select or drag & drop files/folders, and tap download on your phone.
   * **To Receive Files from Mobile:** Click **Receive from Mobile / Device**, upload files from your phone, and approve or reject incoming requests on your PC.

---

## 💻 Building from Source

### Prerequisites
* Python 3.8+
* `pip install flask pywebview qrcode`
* `pip install pyinstaller`

### Build Executable
Run the included build script:
```cmd
build.bat
