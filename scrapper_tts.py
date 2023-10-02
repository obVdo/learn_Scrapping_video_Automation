from selenium.webdriver.common.by import By
from PIL import Image
import io
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from gtts import gTTS
import os

def zoom_in(driver, scale_factor=2):
    # Use execute_script to set the CSS transform property to scale the webpage
    driver.execute_script(f"document.body.style.MozTransform = 'scale({scale_factor})';")

def get_reddit_comments_range_with_screenshots(url, total_comments=20):
    screenshot_dir = "comment_screenshots"  # Directory to save comment screenshots
    output_file = "reddit_comments.txt"  # Output text file for comments
    aud_dir = "output_audio"  # Directory to save comment audio files

    os.makedirs(screenshot_dir, exist_ok=True)
    os.makedirs(aud_dir, exist_ok=True)

    # Specify the path to your Firefox profile directory (modify as needed)
    path_to_default_profile = r'path/to/your/firefox/profile'

    firefox_options = webdriver.FirefoxOptions()
    firefox_options.profile = path_to_default_profile
    driver = webdriver.Firefox(options=firefox_options)

    desired_dpi = 300
    zoom_factor = 4.0
    driver.get(url)
    time.sleep(5)
    post_title_element = driver.find_element(By.XPATH, "/html/body/shreddit-app/div/main/shreddit-post/h1")
    post_title = post_title_element.text.strip()
    title_tts = gTTS(post_title, lang="en")
    title_audio_filename = f"{aud_dir}/comment_0.mp3"
    title_tts.save(title_audio_filename)
    tit_screenshot = post_title_element.screenshot_as_png
    tit_screenshot = Image.open(io.BytesIO(tit_screenshot))
    tit_screenshot.save(f"{screenshot_dir}/comment_0.png", "PNG")
    first_comment_element = driver.find_elements(
        By.XPATH,
        "/html/body/shreddit-app/div/main/faceplate-batch/faceplate-tracker/shreddit-comment-tree/shreddit-comment[1]/div[2]/div/p",
    )
    first_comment_text = " ".join(
        map(lambda element: element.text.strip(), first_comment_element)
    )

    # Find the element you want to remove by its XPath
    element_to_remove_xpath = "/html/body/shreddit-app/reddit-header-large/reddit-header-action-items/header/nav"
    # Execute JavaScript to remove the element from the DOM
    driver.execute_script(
        f'document.evaluate("{element_to_remove_xpath}", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.remove();'
    )

    driver.implicitly_wait(15)

    # Zoom in
    zoom_in(driver)

    try:
        comments = []
        comment_number = 1
        # Loop through the comment range and collect the comment text and take screenshots
        while comment_number < total_comments:
            comment_xpath = f"/html/body/shreddit-app/div/main/faceplate-batch/faceplate-tracker/shreddit-comment-tree/shreddit-comment[{comment_number}]"
            try:
                comment_element = driver.find_element(By.XPATH, comment_xpath)

                time.sleep(5)

                comment_element2 = driver.find_elements(
                    By.XPATH, f"{comment_xpath}/div[2]/div/p"
                )
                comment_text = ""
                for element in comment_element2:
                    # Get the text of each paragraph and concatenate it
                    paragraph_text = element.text.strip()
                    comment_text += paragraph_text + " "
                if comment_number == 1:
                    comment_text = first_comment_text
                if (
                    comment_text.strip()
                ):  # Check if comment_text is not empty or whitespace-only
                    # Generate audio from comment_text using gTTS
                    tts = gTTS(
                        comment_text, lang="en"
                    )  # Replace "en" with the desired language code
                    audio_filename = f"{aud_dir}/comment_{comment_number}.mp3"

                    # Save the generated audio as an audio file
                    tts.save(audio_filename)

                # Capture a screenshot of the specific comment element
                screenshot = comment_element.screenshot_as_png
                # Save the screenshot to a file

                screenshot = Image.open(io.BytesIO(screenshot))

                # Save the screenshot to a file
                screenshot_filename = f"{screenshot_dir}/comment_{comment_number}.png"
                screenshot.save(screenshot_filename, "PNG")

                comment_number += 1
            except Exception as e:
                # Handle exceptions for individual comments (skip and continue)
                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
                view_more_comments_button = driver.find_element(
                    By.XPATH,
                    "/html/body/shreddit-app/div/main/faceplate-batch/faceplate-tracker/shreddit-comment-tree/faceplate-partial/div[1]/button",
                )

                view_more_comments_button.click()
                print("trying to load more comments")
                print(
                    f"Comment {comment_number} not found or has been deleted. Error: {str(e)}"
                )
                comment_number += 1
                continue

        # Save the comments to a text file
        with open(output_file, "w", encoding="utf-8") as file:
            for comment in comments:
                file.write(comment + "\n")
    except Exception as e:
        print("Error:", str(e))

    driver.quit()

if __name__ == "__main__":
    url = "https://www.reddit.com/r/AskReddit/comments/15x5272/what_was_your_sir_this_is_a_wendys_moment/"
    get_reddit_comments_range_with_screenshots(url)
