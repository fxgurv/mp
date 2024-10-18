import os
import sys
import json
import srt_equalizer

from termcolor import colored

ROOT_DIR = os.path.dirname(sys.path[0])

def assert_folder_structure() -> None:
    # Create the .mp folder
    if not os.path.exists(os.path.join(ROOT_DIR, ".mp")):
        if get_verbose():
            print(colored(f"=> Creating .mp folder at {os.path.join(ROOT_DIR, '.mp')}", "green"))
        os.makedirs(os.path.join(ROOT_DIR, ".mp"))

def get_first_time_running() -> bool:
    return not os.path.exists(os.path.join(ROOT_DIR, ".mp"))

def get_email_credentials() -> dict:
    with open(os.path.join(ROOT_DIR, "config.json"), "r") as file:
        return json.load(file)["email"]

def get_verbose() -> bool:
    with open(os.path.join(ROOT_DIR, "config.json"), "r") as file:
        return json.load(file)["verbose"]

def get_browser_profile_path() -> str:
    with open(os.path.join(ROOT_DIR, "config.json"), "r") as file:
        return json.load(file)["profile_path"]

def get_headless() -> bool:
    with open(os.path.join(ROOT_DIR, "config.json"), "r") as file:
        return json.load(file)["headless"]

def get_model() -> str:
    with open(os.path.join(ROOT_DIR, "config.json"), "r") as file:
        return json.load(file)["llm"]

def get_language() -> str:
    with open(os.path.join(ROOT_DIR, "config.json"), "r") as file:
        return json.load(file)["language"]

def get_image_model() -> str:
    with open(os.path.join(ROOT_DIR, "config.json"), "r") as file:
        return json.load(file)["image_model"]

def get_threads() -> int:
    with open(os.path.join(ROOT_DIR, "config.json"), "r") as file:
        return json.load(file)["threads"]
    
def get_image_prompt_llm() -> str:
    with open(os.path.join(ROOT_DIR, "config.json"), "r") as file:
        return json.load(file)["image_prompt_llm"]

def get_zip_url() -> str:
    with open(os.path.join(ROOT_DIR, "config.json"), "r") as file:
        return json.load(file)["zip_url"]

def get_is_for_kids() -> bool:
    with open(os.path.join(ROOT_DIR, "config.json"), "r") as file:
        return json.load(file)["is_for_kids"]

def get_google_maps_scraper_zip_url() -> str:
    with open(os.path.join(ROOT_DIR, "config.json"), "r") as file:
        return json.load(file)["google_maps_scraper"]

def get_google_maps_scraper_niche() -> str:
    with open(os.path.join(ROOT_DIR, "config.json"), "r") as file:
        return json.load(file)["google_maps_scraper_niche"]

def get_scraper_timeout() -> int:
    with open(os.path.join(ROOT_DIR, "config.json"), "r") as file:
        return json.load(file)["scraper_timeout"] or 300

def get_outreach_message_subject() -> str:
    with open(os.path.join(ROOT_DIR, "config.json"), "r") as file:
        return json.load(file)["outreach_message_subject"]
    
def get_outreach_message_body_file() -> str:
    with open(os.path.join(ROOT_DIR, "config.json"), "r") as file:
        return json.load(file)["outreach_message_body_file"]


def get_gemini_api_key() -> str:
    with open(os.path.join(ROOT_DIR, "config.json"), "r") as file:
        return json.load(file)["gemini_api_key"]

def get_assemblyai_api_key() -> str:
    with open(os.path.join(ROOT_DIR, "config.json"), "r") as file:
        return json.load(file)["assembly_ai_api_key"]
    
def equalize_subtitles(srt_path: str, max_chars: int = 10) -> None:
    srt_equalizer.equalize_srt_file(srt_path, srt_path, max_chars)
    
def get_font() -> str:
    with open(os.path.join(ROOT_DIR, "config.json"), "r") as file:
        return json.load(file)["font"]

def get_fonts_dir() -> str:
    return os.path.join(ROOT_DIR, "fonts")

def get_imagemagick_path() -> str:
    with open(os.path.join(ROOT_DIR, "config.json"), "r") as file:
        return json.load(file)["imagemagick_path"]


def get_tts_engine() -> str:
    with open(os.path.join(ROOT_DIR, "config.json"), "r") as file:
        return json.load(file).get("tts_engine")

def get_tts_voice() -> str:
    with open(os.path.join(ROOT_DIR, "config.json"), "r") as file:
        return json.load(file).get("tts_voice")

def get_openai_api_key() -> str:
    with open(os.path.join(ROOT_DIR, "config.json"), "r") as file:
        return json.load(file)["openai_api_key"]

def get_elevenlabs_api_key() -> str:
    with open(os.path.join(ROOT_DIR, "config.json"), "r") as file:
        return json.load(file)["elevenlabs_api_key"]

def get_browser() -> str:
    with open(os.path.join(ROOT_DIR, "config.json"), "r") as file:
        return json.load(file).get("browser")

def get_telegram_api_id():
    with open(os.path.join(ROOT_DIR, "config.json"), "r") as file:
        return json.load(file)["telegram_api_id"]


def get_telegram_api_hash():
    with open(os.path.join(ROOT_DIR, "config.json"), "r") as file:
        return json.load(file)["telegram_api_hash"]

def get_phone():
    with open(os.path.join(ROOT_DIR, "config.json"), "r") as file:
        return json.load(file)["phone_number"]

def get_db_file():
    with open(os.path.join(ROOT_DIR, "config.json"), "r") as file:
        return json.load(file)["db_file"]
