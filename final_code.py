import os
import time
from posts import scroll_and_get_posts

# Load the list of already processed URLs from a file if it exists
done_urls = []
if os.path.exists("done_urls.txt"):
    with open("done_urls.txt", "r") as file:
        done_urls = [line.strip() for line in file.readlines()]

# Define the URL to scrape and other parameters
url = "https://www.reddit.com/r/AskReddit/top/?t=week"
num_posts_to_obtain = 24  # Adjust the number of posts you want to obtain
scroll_delay = 5

# Get a list of URLs using the scroll_and_get_posts function
urls = scroll_and_get_posts(url, num_posts_to_obtain, scroll_delay)
print("Scraped URLs:")
print(urls)

# Iterate through the scraped URLs
for url in urls:
    print("Processing URL:", url)
    
    # Check if the URL has already been processed, and skip if it has
    if url in done_urls:
        print(f"URL {url} has already been processed. Skipping.")
        continue
    
    try:
        # Extract the base directory name from the URL
        base_dir = url.split("/")[-2]
        os.makedirs(base_dir, exist_ok=True)
        os.chdir(base_dir)
        time.sleep(3)

        # Define variables for the directory and number of comments
        aud_dir = "output_audio"
        total_comments = 21
        time.sleep(3)

        # Import necessary modules for comment scraping and video creation
        from scrapper_tts import get_reddit_comments_range_with_screenshots
        from video_maker import create_reddit_comments_video

        # Call functions to scrape comments and create a video
        get_reddit_comments_range_with_screenshots(url, total_comments)
        try:
            create_reddit_comments_video()
        except Exception as video_error:
            print(f"An error occurred in create_reddit_comments_video for URL: {url}")
            print("Error:", str(video_error))
            continue  # Continue to the next URL even if there's a video creation error

        # Write the processed URL to the 'done_urls.txt' file
        with open("../done_urls.txt", "a") as file:
            file.write(url + "\n")
        
        # Change back to the local directory (modify this path as needed)
        os.chdir("C:/path/to/your/local/directory")
    
    except Exception as e:
        print(f"An error occurred for URL: {url}")
        print("Error:", str(e))
        
        # Continue to the next URL even if there's an error
        os.chdir("C:/path/to/your/local/directory")
        continue  # Continue to the next URL even if there's an error
