# Where our index.html is located at
from selenium import webdriver
base_url = "index.html"

# Driver
# - Access path for Driver
access_path = "C:/Users/After/Desktop/All-Data/WorldsHardestGameAI/web_driver/msedgedriver.exe"

# You can download the chromium drivers from their official website:
# - Access http://chromedriver.chromium.org/downloads and
#   download the drivers.
# - Place the drivers in the drivers folder or in other place
# - If you are on linux or macOS you might need to give
#   permission to that file, ex: sudo chmod +x chromedriver
# - Edit the 'driver_path' in the config.py file with the path
#   of the drivers you downloaded
driver_path = webdriver.Edge(access_path)

# If we want to see the NN running,
# it's better to set the "driver_headless" to False,
# in order to show the window with the website.
driver_headless = False
driver_log_level = 3
