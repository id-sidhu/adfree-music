from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pytube import YouTube
import tkinter as tk
import pygetwindow as gw
import keyboard as k
import schedule
import pyautogui
import time
import os

# Global variables for storing the current video URL and driver object
current_video = None
driver = None

def get_active_window():
    """
    Get the currently active window using pygetwindow library.
    
    Returns:
        Active window object
    """
    return gw.getActiveWindow()

# Store the active window to monitor control focus
current_window = get_active_window()

def now_playing():
    """
    Check if a new video is playing, clear the terminal, and display the new video title.
    """
    global current_video
    new_video = driver.current_url  # Get the current URL
    # If the URL has changed, print the new video title
    if new_video != current_video:
        clear_terminal()  # Clear terminal for new video info
        print(f"Now playing: {YouTube(new_video).title}")
        current_video = new_video

def play_song():
    """
    Prompt user to input a song or artist, search it on YouTube, and play the first video result.
    """
    search_query2 = input("Enter song or artist: ").replace(" ", "+")  # Prepare search query
    if not search_query2:  # If no input, default to "latest songs"
        search_query2 = "latest songs"
    print(f"Searching for: {search_query2}")
    driver.get(f'https://www.youtube.com/results?search_query={search_query2}')  # Load YouTube search results

    try:
        # Wait for the first video result to load and click on it
        first_video = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '(//a[@id="video-title"])[1]'))
        )
        first_video.click()

        # Wait for the player to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//ytd-player[@id='ytd-player']"))
        )
        # Store and display the currently playing video
        current_video = driver.current_url
        print(f"Now playing: {YouTube(current_video).title}")
    except Exception as e:
        print(f"Error during search or play: {e}")

def clear_terminal():
    """
    Clear the terminal output based on the operating system.
    """
    if os.name == "nt":
        os.system('cls')  # Clear command for Windows
    else:
        os.system('clear')  # Clear command for Unix-based systems

def get_tkinter_window():
    """
    Get the current active window.
    
    Returns:
        Active window object.
    """
    return gw.getActiveWindow()

def pause():
    """
    Pause or play the YouTube video by simulating a click on the play/pause button.
    """
    # Find and click the play/pause button
    pause_element = driver.find_element(By.XPATH, "//button[@class='ytp-play-button ytp-button']")
    pause_element.click()

def play_next():
    """
    Play the next video in the YouTube playlist by simulating a click on the next button.
    """
    # Find and click the next button
    next_elem = driver.find_element(By.XPATH, '//a[@class="ytp-next-button ytp-button"]')
    next_elem.click()

def incre_vol():
    """
    Increase the system volume using pyautogui.
    """
    if get_active_window() == current_window or get_active_window() == get_tkinter_window:
        pyautogui.press('volumeup')  # Simulate pressing the 'volume up' key

def decre_vol():
    """
    Decrease the system volume using pyautogui.
    """
    if get_active_window() == current_window or get_active_window() == get_tkinter_window:
        pyautogui.press('volumedown')  # Simulate pressing the 'volume down' key

def quit_player():
    """
    Close the YouTube video player (browser) and exit the program.
    """
    driver.close()

def mute():
    """
    Mute or unmute the YouTube video by simulating a click on the mute button.
    """
    mute_elem = driver.find_element(By.XPATH, "//button[@class='ytp-mute-button ytp-button']")
    mute_elem.click()

def setup_driver():
    """
    Set up the ChromeDriver using the Brave browser's binary location and path to ChromeDriver.
    """
    global driver
    brave_path = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"  # Path to Brave browser
    chromedriver_path = "C:\\chromedriver\\chromedriver.exe"  # Path to ChromeDriver
    options = webdriver.ChromeOptions()
    options.binary_location = brave_path  # Set the binary location to Brave
    driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)  # Initialize the driver

def main():
    """
    Main function to set up the driver, GUI, hotkeys, and run the application.
    """
    # Set up the ChromeDriver and YouTube
    setup_driver()
    play_song()

    # Create the Tkinter GUI
    tk_root = tk.Tk()
    
    # Add buttons to the GUI for various functions
    button1 = tk.Button(tk_root, text="Pause/Play", command=pause)
    button2 = tk.Button(tk_root, text="Play Next", command=play_next)
    button3 = tk.Button(tk_root, text="Search", command=play_song)
    button4 = tk.Button(tk_root, text="Mute", command=mute)
    button5 = tk.Button(tk_root, text="Quit", command=quit_player)

    # Pack the buttons into the window
    button1.pack()
    button2.pack()
    button3.pack()
    button4.pack()
    button5.pack()

    # Schedule a task to check what video is now playing every 5 seconds
    schedule.every(5).seconds.do(now_playing)

    # Add hotkeys for controlling video playback
    k.add_hotkey('space', pause)
    k.add_hotkey('shift+n', play_next)
    k.add_hotkey('up', incre_vol)
    k.add_hotkey('down', decre_vol)
    k.add_hotkey('shift+right', play_song)
    k.add_hotkey('shift+m', mute)
    k.add_hotkey('q', quit_player)

    # Start the Tkinter main event loop
    tk_root.mainloop()

    try:
        # Continuously run pending scheduled tasks (e.g., checking video status)
        while True:
            schedule.run_pending()
            time.sleep(1)
    finally:
        # Ensure the driver is closed if the program exits
        if driver:
            driver.close()

# If this script is run directly, call the main function
if __name__ == "__main__":
    main()
