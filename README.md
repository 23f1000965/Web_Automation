# Web Automation Done in a website 
# 🔐 Amazon Gift Card Balance Checker (with Captcha Bypass Support)

This personal project automates the process of checking Amazon gift card balances by:

- Reading card numbers and PINs from a CSV file
- Navigating the gift card balance checker portal
- Automatically recognizing and solving captchas using OCR
- Logging results into organized CSV files for valid, invalid, and expired cards

---

## 🧠 Features

✅ **Selenium-Powered Web Automation**  
✅ **Captcha Handling with EasyOCR (Manual Override Available)**  
✅ **Balance Parsing & Intelligent Logging**  
✅ **Graphical User Interface for Manual Captcha Correction (Tkinter)**  
✅ **Handles Expired Cards, Timeouts, and Session Failures Gracefully**  

---

## 🔧 Technologies Used

- `Selenium` for browser automation
- `EasyOCR` for reading captcha images
- `Tkinter` for GUI-based manual captcha correction
- `PIL` for image manipulation
- `CSV` for input/output data handling
- `ChromeDriver` with `webdriver-manager` for ease of setup

---

## 📂 How it Works

1. **Input as a example**  
   Reads `1.csv` containing gift card numbers and PINs in this format:
1234-5678-9101-2345, PIN1234

2. **Automation**  
Launches Chrome and navigates to the [Amazon Gift Card Balance Checker Portal](https://amazonbal.qwikcilver.com/Welcome.aspx?OrgName=QwikCilver-Amazon).

3. **Captcha Recognition**  
- Captures captcha image
- Tries to decode it using EasyOCR
- If confidence is low or string is malformed, a GUI pops up for manual correction

4. **Balance Check**  
- Submits the form
- Parses balance or handles error messages
- Logs results to:
  - `main.csv`: Valid or Rs. 0.00 balances
  - `np.csv`: Not processed / manually saved
  - Console: Prints detailed logs

5. **Resilience**  
Handles:
- Expired sessions
- TimeoutExceptions
- Invalid sessions
- Network hiccups
- Captcha failures (automatically retries)

---

## 🗃️ Output

### ✅ `main.csv`
Contains successfully checked cards:
Card Number, PIN, Balance 1234567891012345, PIN1234, Rs. 500.00

### 🛑 `np.csv`
Stores entries that were skipped, not processed, or manually handled.

---

## 🧪 Dependencies

```bash
pip install selenium easyocr pillow webdriver-manager
⚠️ FFmpeg must be installed for EasyOCR
Optional: CUDA-enabled GPU for faster OCR

🚀 How to Run
Make sure you have Chrome and Python 3.x

Populate 1.csv with card data

Run the script:
bash
python main.py

**👨‍💻 Project Info**
Personal Project
Bachelor of Science, IIT Madras
Completed: January ,2025
Faculty Advisor: Prof. Anand S

📌 Notes
This script is educational. Do not use it for commercial scraping.
Captcha solving is semi-automatic and meant to assist—not bypass security measures.

🙌 Acknowledgements
EasyOCR

Selenium

ChromeDriver

Tkinter
