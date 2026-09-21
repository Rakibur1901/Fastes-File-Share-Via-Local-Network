```markdown
# Fast Share 🚀

<p align="center">
  <img src="app_icon.png" width="128" height="128" alt="Fast Share Icon">
</p>

<p align="center">
  <strong>Fast, secure, and seamless cross-platform file sharing over your local Wi-Fi network.</strong>
</p>

<p align="center">
  <a href="License"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.8+-green.svg" alt="Python Version"></a>
  <a href="build.bat"><img src="https://img.shields.io/badge/Platform-Windows-0078D6.svg" alt="Platform"></a>
</p>

---

## 📖 Overview

**Fast Share** is a lightweight desktop utility built using **Python**, **Flask**, and **pywebview**. It allows you to transfer files and folders between your PC and mobile devices instantly without uploading your data to third-party cloud servers or installing apps on your phone.

---

## ✨ Key Features

* 📤 **Send Mode (PC ➔ Mobile):** Share single files or entire folders from your computer. Mobile devices scan a QR code to download items straight through their web browser.
* 📥 **Receive Mode (Mobile ➔ PC):** Transfer files from any smartphone or tablet directly to your computer.
* 🛡️ **Host Verification & Approval:** Incoming files require manual approval on the PC—giving you total control over what gets saved.
* 🎯 **Drag-and-Drop:** Drag files or folders into the application window for quick sharing.
* 📂 **Custom Storage Directory:** Configure your preferred output location for received files.
* 📱 **Zero Mobile Setup:** No app required on mobile devices—just scan the QR code using any camera or browser.

---

## 📁 Repository Structure


```

├── .github/workflows/   # CI/CD workflows (Pylint analysis)
├── .gitignore           # Python & IDE exclusion rules
├── License              # MIT Open Source License
├── README.md            # Project documentation
├── app.py               # Main Flask backend & PyWebView app entry point
├── app_icon.ico         # Executable icon file (Windows)
├── app_icon.jpg         # Application graphic
├── app_icon.png         # High-resolution PNG logo
├── build.bat            # One-click PyInstaller build script
├── index.html           # Main PC GUI interface
├── mobile_receive.html  # Web view for receiving files on mobile
├── mobile_send.html     # Web view for uploading files from mobile
├── mobile_wait.html     # Waiting state interface for mobile client
└── upload.html          # File upload staging view

```

---

## 🚀 Getting Started

### Prerequisites

* **Python 3.8 or higher**
* Active local network (Wi-Fi or LAN connection)

### Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/Fast-Share.git](https://github.com/YOUR_USERNAME/Fast-Share.git)
   cd Fast-Share

```

2. **Install required dependencies:**
```bash
pip install flask pywebview qrcode pyinstaller

```


3. **Run the application:**
```bash
python app.py

```



---

## 🔨 Building the `.exe` Executable

To compile the application into a standalone Windows executable:

1. Double-click `build.bat` or run it from the Command Prompt:
```cmd
build.bat

```


2. Once the process completes, locate the compiled executable inside the `dist/FastShare/` directory.

---

## 🛠️ How It Works

1. **Launch App:** Open `FastShare.exe` on your PC.
2. **Connect Mobile Device:** Scan the generated **QR Code** using your phone's camera to join the local web session.
3. **Select Mode:**
* **To Send:** Choose **Send Mode**, queue your files/folders, and tap download on your phone.
* **To Receive:** Choose **Receive Mode**, select files on your phone, and approve incoming transfer prompts on your PC.



---

## 📜 License

This project is licensed under the **MIT License**. See the [License](https://www.google.com/search?q=License&utm_source=gemini) file for details.

---

## 👤 Author

**Md Rakibur Rahman Rafi**

---
