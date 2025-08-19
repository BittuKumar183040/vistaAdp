#! .\venv\Scripts\python.exe

import argparse
import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
import random         
from datetime import datetime
import time

load_dotenv()

LAT=25.569
LON=85.093

userId = os.getenv("USERID")
password = os.getenv("PASSWORD")

def punchIn(page):
  print("Submitting Punch In Request")
  page.wait_for_load_state("networkidle")
  page.get_by_role("button", name="Punch In").click()
  current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  time.sleep(3)
  print(f"Punched In ✅ at {current_date}")

def punchOut(page):
  page.wait_for_load_state("networkidle")
  page.get_by_role("button", name="Punch Out").click()
  current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  time.sleep(3)
  print(f"Punched Out ✅ at {current_date}")

parser = argparse.ArgumentParser()
parser.add_argument("--punch", choices=["in", "out"], required=True, help="Specify punch action: in or out")
args = parser.parse_args()

with sync_playwright() as p:
  browser = p.chromium.launch(headless=True)
  context = browser.new_context()
  context.grant_permissions(["geolocation"])
  
  latitude = str(LAT) + str(int(round(random.random(), 3) * 1000))
  longitude = str(LON) + str(int(round(random.random(), 3) * 1000))

  print(f"Latitude: {latitude}, Longitude: {longitude}")

  context.set_geolocation({"latitude": float(latitude), "longitude": float(longitude)})

  page = context.new_page()
  
  page.goto("https://online.apac.adp.com/signin/v1/?APPID=ADPVISTA-SG&productId=ff803a24-0ee0-47fc-e053-f282530bfabe&returnURL=https://www.vista.adp.com/sg/&callingAppId=ADPVISTA&TARGET=-SM-https://www.vista.adp.com/securtime/in/")

  idField = "#input"
  passwordField = "#input[type='password']"
  verifyBtn = "#verifUseridBtn"
  signBtn = "#signBtn"

  page.wait_for_selector(idField)
  page.fill(idField, userId)
  page.click(verifyBtn)
  print(f'User Logging In - ', idField)
  
  page.wait_for_selector(passwordField)
  page.fill(passwordField, password)

  page.click(signBtn)
  print('User Successfully Logged In')

  if args.punch == "in":
      punchIn(page)
  elif args.punch == "out":
      punchOut(page)
  
  # page.pause()

  browser.close()
