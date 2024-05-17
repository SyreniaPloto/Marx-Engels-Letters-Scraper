import csv
import logging
import os

# 设置日志记录
logging.basicConfig(filename='scraper.log', level=logging.ERROR)

def save_to_csv(filename, data, append=False):
    mode = 'a' if append else 'w'
    with open(filename, mode, encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        if not append:
            writer.writerow(['Title', 'Date', 'Content'])
        writer.writerows(data)

def handle_request_error(exception, url):
    logging.error(f"Error fetching {url}: {exception}")
    print(f"Error fetching {url}: {exception}")

def save_links_to_file(filename, links):
    with open(filename, 'w') as file:
        for link in links:
            file.write(f"{link}\n")

def load_links_from_file(filename):
    with open(filename, 'r') as file:
        links = file.read().splitlines()
    return links

def save_progress(filename, links):
    with open(filename, 'w') as file:
        for link in links:
            file.write(f"{link}\n")

def load_progress(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, 'r') as file:
        links = file.read().splitlines()
    return links

def append_to_file(filename, link):
    with open(filename, 'a') as file:
        file.write(f"{link}\n")

def fix_link(link):
    if '../' in link:
        link = link.replace('../', '/')
    return link

def fix_links_in_file(filename):
    links = load_links_from_file(filename)
    fixed_links = [fix_link(link) for link in links]
    save_links_to_file(filename, fixed_links)

def merge_csv_files(temp_dir, output_file):
    with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Title', 'Date', 'Content'])
        for filename in os.listdir(temp_dir):
            if filename.endswith('.csv'):
                with open(os.path.join(temp_dir, filename), 'r', encoding='utf-8') as infile:
                    reader = csv.reader(infile)
                    next(reader)  # 跳过标题行
                    for row in reader:
                        writer.writerow(row)
