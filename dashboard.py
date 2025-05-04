#! .\venv\Scripts\python.exe

import argparse
import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
import random         

load_dotenv()

LAT=12.912
LON=77.644

userId = os.getenv("USERID")
password = os.getenv("PASSWORD")

def punchIn(page):
  page.get_by_role("button", name="Punch In").click()

  # change this to wait for the punch in button to detect popup showed.
  # page.wait_for_selector("div[class='vdl-modal__footer']")
  print("Punched In ✅")

def punchOut(page):
  page.get_by_role("button", name="Punch Out").click()
  page.locator("text='submission successfully'").wait_for()
  print("Punched Out ✅")
  
with sync_playwright() as p:
  browser = p.chromium.launch(headless=False)
  context = browser.new_context()
  context.grant_permissions(["geolocation"])
  
  latitude = str(LAT) + str(int(round(random.random(), 3) * 1000))
  longitude = str(LON) + str(int(round(random.random(), 3) * 1000))

  print(f"Latitude: {latitude}, Longitude: {longitude}")

  context.set_geolocation({"latitude": float(latitude), "longitude": float(longitude)})

  page = context.new_page()
  
  page.goto("https://www.vista.adp.com/IN")

  idField = "#input"
  passwordField = "#input[type='password']"
  verifyBtn = "#verifUseridBtn"
  signBtn = "#signBtn"

  page.wait_for_selector(idField)
  page.fill(idField, userId)
  page.click(verifyBtn)

  page.wait_for_selector(passwordField)
  page.fill(passwordField, password)
  page.click(signBtn)

  # dashboard page
  page.wait_for_selector("div[class='vdl-modal__footer']")
  page.locator("button", has_text="Try Later").click()

  # expanding the sidebar
  page.locator("sfc-shell-app-bar sdf-icon-button").click()

  page.get_by_role("link", name="Me").click()

  with page.expect_popup() as new_page_info:
    page.get_by_role("link", name="Time & Attendance").click()
  new_page = new_page_info.value
  new_page.wait_for_load_state("networkidle")

  # punchIn(new_page)
  # punchOut(new_page)
  
  page.pause()

  browser.close()