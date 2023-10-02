from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time

def scroll_and_get_posts(url, num_posts_to_obtain=14, scroll_delay=5):
    # Set up Firefox options (you can customize this as needed)
    options = Options()
    options.headless = False  # Set to True for headless mode

    # Create a Firefox WebDriver instance with the specified options
    driver = webdriver.Firefox(options=options)

    driver.get(url)

    try:
        # Initialize an empty list to store post links
        post_links = []

        for i in range(1, num_posts_to_obtain + 1):
            # Scroll down
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_delay)

            # Try the first XPath structure
            try:
                post_link_element = driver.find_element(
                    By.XPATH, f"/html/body/shreddit-app/div/main/div[3]/shreddit-post[{i}]/a[@slot='full-post-link']"
                )
                post_link = post_link_element.get_attribute("href")

                if post_link:
                    post_links.append(post_link)
                    continue  # If a link is found, continue to the next post
            except:
                pass  # If the first structure fails, continue to the second structure

            # Try the second XPath structure
            try:
                post_link_element = driver.find_element(
                    By.XPATH, f"/html/body/shreddit-app/div/main/div[3]/faceplate-batch[1]/shreddit-post[{i}]/a[@slot='full-post-link']"
                )
                post_link = post_link_element.get_attribute("href")

                if post_link:
                    post_links.append(post_link)
            except:
                pass  # If both structures fail, continue to the next post

        return post_links
    finally:
        # Close the browser when done
        driver.quit()

if __name__ == "__main__":
    # Specify the URL, number of posts to obtain, and scroll delay (in seconds)
    url = "https://www.reddit.com/r/AskReddit/top/?t=week"
    num_posts_to_obtain = 24  # Adjust the number of posts you want to obtain
    scroll_delay = 5  # Adjust the scroll delay as needed

    # Call the function to scroll and obtain the specified number of posts
    post_links = scroll_and_get_posts(url, num_posts_to_obtain, scroll_delay)

    # Print the obtained post links
    for i, link in enumerate(post_links, start=1):
        print(f"Post {i}: {link}")
