import os
from concurrent.futures import ThreadPoolExecutor
from scraper import get_letter_links, scrape_letter_content
from utils import save_links_to_file, load_links_from_file, load_progress, append_to_file, merge_csv_files
import subprocess

LINKS_FILE = 'letter_links.txt'
PROGRESS_FILE = 'progress.txt'
FAILED_FILE = 'failed_links.txt'
TEMP_DIR = 'temp_results'
TOTAL_COUNT_FILE = 'total_count.txt'

def main():
    base_url = "https://megadigital.bbaw.de/briefe/index.xql?&offset="

    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

    # 加载信件链接
    if os.path.exists(LINKS_FILE):
        print(f"Loading links from {LINKS_FILE}")
        all_links = load_links_from_file(LINKS_FILE)
    else:
        print(f"{LINKS_FILE} not found, generating new link list...")
        offsets = [i for i in range(1, 2001 + 1, 40)]  # 每页偏移量增加40
        all_links = []

        # 使用多线程获取所有信件链接（3个线程）
        with ThreadPoolExecutor(max_workers=3) as executor:
            links = list(executor.map(lambda offset: get_letter_links(base_url, offset), offsets))

        # 展平列表
        all_links = [link for sublist in links for link in sublist]

        # 保存信件链接到文件
        save_links_to_file(LINKS_FILE, all_links)

        # 保存信件总数到文件
        with open(TOTAL_COUNT_FILE, 'w') as f:
            f.write(str(len(all_links)))

    # 加载进度
    processed_links = load_progress(PROGRESS_FILE)
    failed_links = load_progress(FAILED_FILE)

    # 过滤已经处理的链接
    links_to_process = [link for link in all_links if link not in processed_links]

    # 使用多线程爬取信件内容（8个线程）
    with ThreadPoolExecutor(max_workers=8) as executor:
        list(executor.map(lambda link: scrape_letter_content(link, PROGRESS_FILE, FAILED_FILE, TEMP_DIR), links_to_process + failed_links))

    # 合并临时结果文件
    merge_csv_files(TEMP_DIR, 'marx_letters_all.csv')

    # 调用验证脚本
    subprocess.run(["python", "verifier.py"])

if __name__ == "__main__":
    main()
