import os
import sys
import time
import json

from selenium import webdriver

# local config.py
import config
from game import *


def get_fitness(game):
    return (1 / game.end_distance) + (game.collected_coins / 135) + (game.level * 2)


def main():
    if config.access_path and not os.path.exists(config.access_path):
        print("The driver path in the config doesn't exist")
        print(
            "You can download the chromium drivers from their official"
            "website:"
            "\n\t- Access http://chromedriver.chromium.org/downloads and "
            "download the drivers."
            "\n\t- Place the drivers in the drivers folder or in other place"
            "\n\t- If you are on linux or macOS you might need to give "
            "\n\t  permission to that file, ex: sudo chmod +x chromedriver"
            "\n\t- Edit the 'driver_path' in the config.py file with the path"
            "of the drivers you downloaded"
        )
        sys.exit(1)

    # Create driver with all the arguments
    options = webdriver.EdgeOptions()
    # to leave browser open
    options.add_experimental_option("detach", True)
    options.add_argument("--log-level=%d" % int(config.driver_log_level))
    options.add_argument("--window-size=900,800")
    if config.driver_headless:
        options.add_argument("headless")

    driver = webdriver.Edge(
        config.access_path, service_log_path="driver.log", options=options
    )
    real_url = "file://" + os.path.join(os.getcwd(), config.base_url)
    driver.implicitly_wait(10)

    print(real_url)
    # Go to the url
    driver.get(real_url)

    data = GameData(driver)
    do = GameInput(driver)

    do.up()
    do.left()
    do.down()
    do.right()

    driver.implicitly_wait(10)

#     time.sleep(1)

#     driver.quit()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted by the user.")
        sys.exit()
