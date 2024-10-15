import time
from utils import *
from constants import *
from typing import List 
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException



class Uploader:
    def __init__(self, fp_profile_path: str):
        info("Setting up Firefox profile for Uploader")
        self.options: Options = Options()
        if get_headless():
            info("Setting browser to headless mode")
            self.options.add_argument("--headless")
        info(f"Setting Firefox profile path: {fp_profile_path}")
        self.options.add_argument("-profile")
        self.options.add_argument(fp_profile_path)
        info("Installing GeckoDriver")
        self.service: Service = Service(GeckoDriverManager().install())
        info("Initializing Firefox browser")
        self.browser: webdriver.Firefox = webdriver.Firefox(service=self.service, options=self.options)

    def get_channel_id(self) -> str:
        try:
            info("Getting Channel ID from YouTube Studio")
            driver = self.browser
            driver.get("https://studio.youtube.com")
            time.sleep(2)
            channel_id = driver.current_url.split("/")[-1]
            self.channel_id = channel_id
            success(f"Retrieved Channel ID: {channel_id}")
            return channel_id
        except Exception as e:
            error(f"Failed to get Channel ID: {e}")
            return None

    def upload_video(self, video_path, title, description):
        try:
            info("Starting video upload process")
            self.get_channel_id()

            driver = self.browser
            verbose = get_verbose()

            # Go to youtube.com/upload
            driver.get("https://www.youtube.com/upload")
            info("Navigated to YouTube upload page")

            # Set video file
            FILE_PICKER_TAG = "ytcp-uploads-file-picker"
            file_picker = driver.find_element(By.TAG_NAME, FILE_PICKER_TAG)
            INPUT_TAG = "input"
            file_input = file_picker.find_element(By.TAG_NAME, INPUT_TAG)
            file_input.send_keys(video_path)
            info(f"Selected video file: {video_path}")

            # Wait for upload to finish
            time.sleep(5)

            # Set title
            textboxes = driver.find_elements(By.ID, YOUTUBE_TEXTBOX_ID)

            title_el = textboxes[0]
            description_el = textboxes[-1]

            if verbose:
                info("\t=> Setting title...")

            title_el.click()
            time.sleep(1)
            title_el.clear()
            title_el.send_keys(title)
            success(f"Set video title: {title}")

            if verbose:
                info("\t=> Setting description...")

            # Set description
            time.sleep(10)
            description_el.click()
            time.sleep(0.5)
            description_el.clear()
            description_el.send_keys(description)
            success(f"Set video description: {description}")

            time.sleep(0.5)

            # Set `made for kids` option
            if verbose:
                info("\t=> Setting `made for kids` option...")

            is_for_kids_checkbox = driver.find_element(By.NAME, YOUTUBE_MADE_FOR_KIDS_NAME)
            is_not_for_kids_checkbox = driver.find_element(By.NAME, YOUTUBE_NOT_MADE_FOR_KIDS_NAME)

            if not get_is_for_kids():
                is_not_for_kids_checkbox.click()
                info("Set video as not made for kids")
            else:
                is_for_kids_checkbox.click()
                info("Set video as made for kids")

            time.sleep(0.5)

            # Click next
            if verbose:
                info("\t=> Clicking next...")

            next_button = driver.find_element(By.ID, YOUTUBE_NEXT_BUTTON_ID)
            next_button.click()

            # Click next again
            if verbose:
                info("\t=> Clicking next again...")
            next_button = driver.find_element(By.ID, YOUTUBE_NEXT_BUTTON_ID)
            next_button.click()

            # Wait for 2 seconds
            time.sleep(2)

            # Click next again
            if verbose:
                info("\t=> Clicking next again...")
            next_button = driver.find_element(By.ID, YOUTUBE_NEXT_BUTTON_ID)
            next_button.click()

            # Set as unlisted
            if verbose:
                info("\t=> Setting as unlisted...")
            
            radio_button = driver.find_elements(By.XPATH, YOUTUBE_RADIO_BUTTON_XPATH)
            radio_button[2].click()
            success("Set video visibility to unlisted")

            if verbose:
                info("\t=> Clicking done button...")

            # Click done button
            done_button = driver.find_element(By.ID, YOUTUBE_DONE_BUTTON_ID)
            done_button.click()

            # Wait for 2 seconds
            time.sleep(2)

            # Get latest video
            if verbose:
                info("\t=> Getting video URL...")

            # Get the latest uploaded video URL
            driver.get(f"https://studio.youtube.com/channel/{self.channel_id}/videos/short")
            time.sleep(2)
            videos = driver.find_elements(By.TAG_NAME, "ytcp-video-row")
            first_video = videos[0]
            anchor_tag = first_video.find_element(By.TAG_NAME, "a")
            href = anchor_tag.get_attribute("href")
            if verbose:
                info(f"\t=> Extracting video ID from URL: {href}")
            video_id = href.split("/")[-2]

            # Build URL
            url = build_url(video_id)

            self.uploaded_video_url = url

            if verbose:
                success(f" => Uploaded Video: {url}")

            # Add video to cache
            self.add_video({
                "title": title,
                "description": description,
                "url": url,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

            # Close the browser
            driver.quit()

            return True
        except Exception as e:
            error(f"Failed to upload video: {e}")
            self.browser.quit()
            return False

    def add_video(self, video: dict) -> None:
        info(f"Adding video to cache: {video}")
        videos = self.get_videos()
        videos.append(video)

        cache = get_youtube_cache_path()

        with open(cache, "r") as file:
            previous_json = json.loads(file.read())
            
            accounts = previous_json["accounts"]
            for account in accounts:
                if account["id"] == self._account_uuid:
                    account["videos"].append(video)
            
            with open(cache, "w") as f:
                f.write(json.dumps(previous_json))
        success("Video added to cache")

    def get_videos(self) -> List[dict]:
        try:
            info("Retrieving uploaded videos from cache")
            if not os.path.exists(get_youtube_cache_path()):
                # Create the cache file
                with open(get_youtube_cache_path(), 'w') as file:
                    json.dump({
                        "videos": []
                    }, file, indent=4)
                return []

            videos = []
            # Read the cache file
            with open(get_youtube_cache_path(), 'r') as file:
                previous_json = json.loads(file.read())
                # Find our account
                accounts = previous_json["accounts"]
                for account in accounts:
                    if account["id"] == self._account_uuid:
                        videos = account["videos"]
            success(f"Retrieved {len(videos)} videos from cache")
            return videos
        except Exception as e:
            error(f"Failed to retrieve videos from cache: {e}")
            return []
