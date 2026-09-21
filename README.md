# Fast Share 🚀

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
git clone https://github.com/YOUR_USERNAME/Fast-Share.git
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

This project is licensed under the **MIT License**. See the [License](License) file for details.

---

## 👤 Author

**Md Rakibur Rahman Rafi**

---
Preview Images:

<!-- First Row (4 Images) -->
<div>
  <img src="https://github.com/user-attachments/assets/540b13fe-0222-4d8d-b4d9-91fe983b2f06" width="200" />
  <img src="https://github.com/user-attachments/assets/ba124bf0-c53d-424a-9ae1-21b1254db24f" width="200" />
  <img src="https://github.com/user-attachments/assets/4f9cbd7a-13c9-4c60-917b-d25f23f762b1" width="200" />
  <img src="https://github.com/user-attachments/assets/48337455-d249-4ba3-85db-ed82a0121704" width="200" />
</div>

<br />

<!-- Second Row (3 Images) -->
<div>
  <img src="https://github.com/user-attachments/assets/e7351ee4-9a98-4f8c-859b-46858ac4575d" width="200" />
  <img src="https://github.com/user-attachments/assets/c2cc7791-0b3e-4e27-b2a9-905c57d6bec3" width="200" />
  <img src="https://github.com/user-attachments/assets/8ae23b04-9194-4100-9b20-c0efe7ea96d0" width="200" />
</div>





