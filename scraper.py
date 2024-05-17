import requests
import urllib3
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from utils import handle_request_error, append_to_file, save_to_csv
import time
import random
import os
from urllib.parse import quote

urllib3.disable_warnings()
MAX_RETRIES = 10
RETRY_WAIT_TIME = 10  # seconds

def create_session():
    session = requests.Session()
    retries = Retry(total=MAX_RETRIES, backoff_factor=1,
                    status_forcelist=[500, 502, 503, 504],
                    allowed_methods=["HEAD", "GET", "OPTIONS"])
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

def get_letter_links(base_url, offset):
    url = f"{base_url}{offset}"
    print(f"Scraping URL: {url}")
    session = create_session()
    for attempt in range(MAX_RETRIES):
        try:
            response = session.get(url, timeout=10, verify=False)  # 忽略SSL验证
            response.raise_for_status()
            break
        except requests.RequestException as e:
            handle_request_error(e, url)
            if attempt < MAX_RETRIES - 1:
                wait_time = RETRY_WAIT_TIME + random.uniform(0, 5)
                print(f"Retrying in {wait_time:.2f} seconds...")
                time.sleep(wait_time)
            else:
                return []

    soup = BeautifulSoup(response.content, 'html.parser')
    link_elements = soup.find_all('a', href=True)
    letter_links = []
    for link in link_elements:
        href = link['href']
        if 'detail.xql?id=' in href:
            if href.startswith("/"):
                letter_links.append(f"https://megadigital.bbaw.de{href}")
            else:
                letter_links.append(f"https://megadigital.bbaw.de/{href}")

    for link in letter_links:
        print(f"Generated link: {link}")
    
    return letter_links

def scrape_letter_content(url, progress_file, failed_file, temp_dir):
    print(f"Scraping Letter URL: {url}")
    session = create_session()
    for attempt in range(MAX_RETRIES):
        try:
            response = session.get(url, timeout=10, verify=False)  # 忽略SSL验证
            response.raise_for_status()
            break
        except requests.RequestException as e:
            handle_request_error(e, url)
            if attempt < MAX_RETRIES - 1:
                wait_time = RETRY_WAIT_TIME + random.uniform(0, 5)
                print(f"Retrying in {wait_time:.2f} seconds...")
                time.sleep(wait_time)
            else:
                append_to_file(failed_file, url)
                return None

    soup = BeautifulSoup(response.content, 'html.parser')
    h1_elements = soup.find_all('h1')
    if len(h1_elements) > 1:
        title_text = h1_elements[1].get_text(strip=True)
        date = title_text.split(',')[-1].strip()
    else:
        title_text = "Unknown title"
        date = "Unknown date"

    content_element = soup.find('div', class_='boxInner transkription')
    content = content_element.get_text(separator="\n", strip=True) if content_element else "No content available"
    content = " ".join(content.split())  # 去除多余的空格和空行

    result = [(title_text, date, content)]
    encoded_url = quote(url, safe='')
    temp_filename = os.path.join(temp_dir, f"{encoded_url}.csv")
    save_to_csv(temp_filename, result, append=False)

    append_to_file(progress_file, url)
    return result
