# 🛡️ Keystroke Guardian: Behavioral Biometrics & Intruder Snap

> *"Passwords can be stolen. Typing rhythms cannot."*

## 🚀 Overview
**Keystroke Guardian** is a cybersecurity tool that uses **Behavioral Biometrics** to authenticate users based on their unique typing patterns (keystroke dynamics). Unlike traditional passwords, this system analyzes *how* you type, not just *what* you type.

**V2.0 Feature:** If the biometric authentication fails (potential intruder detected), the system triggers an **Active Defense Mechanism** using OpenCV to instantly capture and save a photo of the unauthorized user.

## 🧠 How It Works
1.  **Profiling (Training):** The user types a standard sentence 5 times. The system calculates the average "flight time" (latency between key presses) to create a unique biometric signature.
2.  **Verification:** When a user attempts to login, their current typing speed is compared against the stored profile.
3.  **Active Defense:** If the deviation exceeds the tolerance threshold (25%), the system denies access and silently activates the webcam to capture the intruder's face.

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **Input Handling:** `pynput` (Hardware-level keyboard listening)
* **Computer Vision:** `OpenCV` (Webcam control for evidence capture)
* **Data Storage:** JSON (Lightweight profile storage)

## ⚙️ Installation

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/Keystroke-Guardian.git](https://github.com/YOUR_USERNAME/Keystroke-Guardian.git)
    cd Keystroke-Guardian
    ```

2.  **Install Dependencies:**
    ```bash
    pip install pynput opencv-python
    ```

3.  **Run the Tool:**
    ```bash
    python main.py
    ```

## 📸 Usage
1.  Select **Option 1 (Train Mode)** to create your profile.
2.  Select **Option 2 (Authenticate)** to test the security.
3.  Try typing significantly slower or faster (simulate an attacker) to trigger the **Intruder Trap** and see your photo saved in the project folder!

## ⚖️ Disclaimer
This tool is for educational purposes. The facial capture feature should be used responsibly and ethically.

---
*Developed by [Eda] - Cybersecurity Enthusiast*