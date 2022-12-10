""" 
Author: Frank Merriman

A bot for 'Kimcartoon' that automatically navigates from video to video in an "autoplay" manner.
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from pathlib import Path
import time


next_button_class_name = "nexxt"
video_frame_id = "player_container"
video_iframe_css = "#player_container > iframe"
countdown_timer_class = "jw-text-countdown"


def main():

    chrome_options = Options()

    # Add option to allow driver to detach once script is done. 
    # This prevents the browser from closing at EOF
    chrome_options.add_experimental_option("detach", True)

    # Add argument to load ublock origin for chrome.
    # I copied the extension into the project dir
    extension = Path("1.45.2_0_ublock").resolve() # Resolve means the absolute path is used (so it works no matter where this file is run)
    chrome_options.add_argument("load-extension=" + str(extension)) # Cast to string as WindowsPath is not supported

    # Disable Chrome's annoying "Automation software is running" banner
    # From: https://stackoverflow.com/a/57384517
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    # Set driver to Chrome since thats what Nick uses
    driver = webdriver.Chrome(options=chrome_options)

    # Open the browser at the most recent episode watched
    current_episode_url = get_current_episode_url()
    driver.get(current_episode_url)


    # Main loop
    while True:
        # Wait to ensure page has loaded
        time.sleep(3)

        # Update history
        set_current_episode_url(driver.current_url)

        # Play episode
        play_episode(driver)

        # Watch video in fullscreen
        watch_episode(driver)

        # Navigate to next episode
        next_episode(driver)

        

        

def play_episode(driver):
    """
    Access the html and plays the episode
    """
    play_button = driver.find_element(By.ID, video_frame_id)
    play_button.click()

def watch_episode(driver):
    """
    Access the iframe, fullscreen video and wait until finished
    then exit iframe
    """

    # Swap to inner iframe
    iframe = driver.find_element(By.CSS_SELECTOR, video_iframe_css)
    driver.switch_to.frame(iframe)

    # Send fullscreen hotkey
    play_button = driver.find_element(By.ID, video_frame_id)
    play_button.send_keys("f")

    # Sleep longer before first poll 
    # This avoids triggering the default value for
    # time remain - 00:00, which would cause the
    # episode to be skipped
    time.sleep(5)

    # Loop this check for the episode being over
    playing = True
    while playing == True:

        # Sleep before next poll
        time.sleep(1)

        # Get progress through episode
        time_remain = driver.find_element(By.CLASS_NAME, countdown_timer_class).get_attribute("innerHTML")

        # If at end of episode, exit iframe
        if time_remain == "00:00":
            playing = False

    
    # Wait 1 second
    time.sleep(1)

    # Send fullscreen hotkey (to exit fullscreen)
    play_button = driver.find_element(By.ID, video_frame_id)
    play_button.send_keys("f")

    # Reset driver back to main page
    driver.switch_to.parent_frame()

    return


def next_episode(driver):
    """
    Accesses the html and selects the element
    that navigates to the next episode
    """

    next_button = driver.find_element(By.CLASS_NAME, next_button_class_name)
    next_button.click()

    return


def set_current_episode_url(url_str):
    """
    Save the last episode watched into history
    """
    with open("history.txt", "w") as f:
        f.write(url_str)
    
    return

def get_current_episode_url():
    """
    Loads the last episode watched from history
    and returns it as a string
    """
    with open("history.txt", "r") as f:
        url = f.readline()

    return url

if __name__ == "__main__":
    main()

