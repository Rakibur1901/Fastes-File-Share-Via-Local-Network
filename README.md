# ⚡ Local File Flow

> Fast, secure, and seamless cross-device file sharing over your local Wi-Fi network.

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/framework-Flask%20%7C%20PyWebView-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)

**Local File Flow** is a lightweight desktop controller built with Python, Flask, and PyWebView. It allows you to quickly send and receive files between your PC and mobile devices without relying on third-party cloud services or internet connections.

---

## 🔥 Key Features

- **📱 QR Code Auto-Routing**: Scan a single QR code on mobile to connect instantly. Switching modes on your PC automatically routes mobile clients to the `/send` or `/receive` interface.
- **🛡️ Staging & Verification Queue**: Incoming files from mobile devices land in a temporary staging area first. Review filenames, extensions, and file sizes before accepting or rejecting them.
- **🔄 Auto-Reset on Stop**: Returning to the PC home view automatically redirects mobile devices back to the `/connect` waiting screen.
- **📁 Folder & Batch Selection**: Share individual files or entire directory trees directly from your desktop.

---

## 🛠️ Installation & Prerequisites

### Prerequisites
- Python **3.8** or higher
- All devices must be connected to the **same local Wi-Fi network**.

### Required Packages
Install dependencies via `pip`:

```bash
pip install flask pywebview werkzeug
```

---

## 🚀 Getting Started

1. **Clone the repository**:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/lan-file-flow.git](https://github.com/YOUR_USERNAME/lan-file-flow.git)
   cd lan-file-flow
   ```

2. **Run the application**:
   ```bash
   python app.py
   ```

3. **Connect your mobile device**:
   * A desktop window will display a generated QR code.
   * Scan the QR code using your phone camera or mobile browser.
   * Toggle between **Send** and **Receive** modes on your PC to start transferring.

---

## 📂 Project Structure

```text
lan-file-flow/
├── app.py           # Flask backend & PyWebView GUI manager
├── index.html       # PC Controller frontend user interface
├── README.md        # Project documentation
└── LICENSE          # MIT License
```

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/YOUR_USERNAME/lan-file-flow/issues).

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.
