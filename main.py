import os
import csv
import time
import base64
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, InvalidSessionIdException, ElementNotInteractableException
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageTk
from selenium.webdriver.chrome.options import Options
import re
import easyocr

# Check for GPU availability
try:
    reader = easyocr.Reader(['en'], gpu=True)
except RuntimeError as e:
    print("Neither CUDA nor MPS are available - defaulting to CPU. Note: This module is much faster with a GPU.")
    reader = easyocr.Reader(['en'], gpu=False)

os.system("cls || clear")

print("Code Checker")

def get_user_input(image_path, initial_string):
    root = tk.Tk()
    root.title("Enter Captcha")

    img = Image.open(image_path)
    img = img.resize((270, 52), Image.Resampling.LANCZOS)
    tk_img = ImageTk.PhotoImage(img)

    image_label = tk.Label(root, image=tk_img)
    image_label.pack()

    string_label = tk.Label(root, text="Edit the string below:")
    string_label.pack()

    user_input_var = tk.StringVar(value=initial_string)

    user_input_entry = tk.Entry(root, width=50, textvariable=user_input_var)
    user_input_entry.pack(pady=10)

    result = {"final_string": None}

    def on_submit():
        user_input = user_input_var.get()
        result["final_string"] = user_input
        root.destroy()
    submit_button = tk.Button(root, text="Submit", command=on_submit)
    submit_button.pack()
    root.mainloop()

    return result["final_string"]

def append_row_to_csv(new_row):
    file_path = "main.csv"
    with open(file_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(new_row)
    ba = ""
    if new_row[2] != "Rs. 0.00":
        ba = "Balance: " + new_row[2]
    else:
        ba = "No Balance"
    print("\tCode checked" + " -- " + ba)

def append_row_to_csv_new(new_row):
    file_path = "np.csv"
    with open(file_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(new_row)
    print("\tCode saved, not checked")

def handle_captcha():
    api = ocrspace.API(api_key='YOUR API KEY', language=ocrspace.Language.English, engine=ocrspace.Engine.ENGINE_2) # type: ignore
    ocr_txt = (api.ocr_file(open('cap.png', 'rb')))
    return ocr_txt

def save_img(image_element):
    image_data = image_element.screenshot_as_base64
    if image_data.startswith('data:image'):
        image_data = image_data.split(',')[1]
    image_bytes = base64.b64decode(image_data)
    with open(f'cap.png', 'wb') as f:
        f.write(image_bytes)

def logout_and_refresh():
    try:
        print("Attempting to log out...")
        wait.until(EC.element_to_be_clickable((By.ID, "ctl00_LeftMenu1_lmbWelcome_hlUnselected"))).click()
        time.sleep(2)
        driver.refresh()
    except Exception as e:
        print(f"Error during logout: {e}")
        driver.refresh()

def getMoni(var1, var2, retry_count=0):
    global driver, wait
    try:
        time.sleep(3)
        wait.until(EC.visibility_of_element_located((By.ID, "xtCardNumber"))).send_keys(var1)
        wait.until(EC.visibility_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_txtctl00_ContentPlaceHolder1_tCardPin"))).send_keys(var2)
        image_element = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_Captcha_CaptchaImage')
        save_img(image_element)

        ocr_txt = reader.readtext('cap.png', detail=0, allowlist='0123456789')
        ocr_txt = re.sub(r"\s+", "", ocr_txt[0], flags=re.UNICODE)

        wait.until(EC.visibility_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_Captcha_CodeNumberTextBox"))).send_keys(ocr_txt)
        wait.until(EC.visibility_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_Logo"))).click()
        captcha_invalid = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_Captcha_CompareValidator1')

        if captcha_invalid.is_displayed() or len(ocr_txt) != 6:
            print("\t" + " -- " + "Invalid Captcha, trying again")
            driver.refresh()
            time.sleep(3)
            getMoni(var1, var2)
            return

        wait.until(EC.visibility_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_EGMSButton1_lbThemeButton"))).click()

        try:
            err = driver.find_element('css selector', '.ErrorMessage')
            error_message_element = driver.find_element(By.CLASS_NAME, 'ErrorMessage')
            error_message = error_message_element.text
            print('\t' + " -- " + error_message)
            wait.until(EC.visibility_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_EGMSHTMLButton1_hlThemeButton"))).click()
            return
        except NoSuchElementException:
            pass

        time.sleep(3)
        wait.until(EC.visibility_of_element_located((By.ID, "ctl00_LeftMenu1_lmbBalEnq_hlUnselected"))).click()

        try:
            bal_element = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_lblBalance")
            bal = bal_element.text
        except NoSuchElementException:
            bal = "Expired"
        new_row = [var1, var2, bal]
        if bal == "Expired":
            print("\tCode checked" + " -- " + bal)
        elif bal == "Rs. 0.00":
            print("\tCode checked" + " -- " + bal)
        else:
            append_row_to_csv(new_row)

        try:
            wait.until(EC.visibility_of_element_located((By.ID, "ctl00_LeftMenu1_lmbWelcome_hlUnselected"))).click()
        except TimeoutException:
            print("\t" + " -- " + "Timeout while waiting for element, refreshing the page")
            if retry_count < 1:
                driver.refresh()
                getMoni(var1, var2, retry_count + 1)
            else:
                logout_and_refresh()
                getMoni(var1, var2)
    except TimeoutException as e:
        print("\t" + " -- " + "TimeoutException: ", e)
        if retry_count < 1:
            driver.refresh()
            getMoni(var1, var2, retry_count + 1)
        else:
            logout_and_refresh()
            getMoni(var1, var2)
    except InvalidSessionIdException as e:
        print("\t" + " -- " + "InvalidSessionIdException: ", e)
        driver = webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))
        driver.get("https://amazonbal.qwikcilver.com/Welcome.aspx?OrgName=QwikCilver-Amazon")
        getMoni(var1, var2)
    except BaseException as error:
        print("\t" + " -- " + "Error: ", error)
        driver.close()
        driver = webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))
        driver.get("https://amazonbal.qwikcilver.com/Welcome.aspx?OrgName=QwikCilver-Amazon")
        getMoni(var1, var2)
        return

options = Options()

options.add_argument("--no-sandbox")

file_path = "1.csv"
with open(file_path, mode='r') as file:
    csv_reader = csv.reader(file)
    driver = webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))
    wait = WebDriverWait(driver, 60)  # Increased timeout period
    driver.get("https://amazonbal.qwikcilver.com/Welcome.aspx?OrgName=QwikCilver-Amazon")
    i = 1

    for row in csv_reader:
        var1, var2 = row
        var1 = var1.replace('-', '')  # Remove dashes
        numeric_string = ''.join(filter(str.isdigit, var1))
        if numeric_string:  # Check if numeric_string is not empty
            var1 = int(numeric_string)
            print(str(i) + ": " + str(var1))
            getMoni(var1, var2)
        else:
            print(f"Skipping invalid entry: {var1}")
        i += 1
    driver.close()
