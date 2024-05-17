import os
import csv
import shutil

TOTAL_COUNT_FILE = 'total_count.txt'
LINKS_FILE = 'letter_links.txt'
TEMP_DIR = 'temp_results'
FAILED_FILE = 'failed_links.txt'
LOG_FILE = 'scraper.log'
PROGRESS_FILE = 'progress.txt'


def get_expected_total():
    if os.path.exists(TOTAL_COUNT_FILE):
        with open(TOTAL_COUNT_FILE, 'r') as file:
            return int(file.read().strip())
    elif os.path.exists(LINKS_FILE):
        with open(LINKS_FILE, 'r') as file:
            links = file.read().splitlines()
            return len(links)
    else:
        raise FileNotFoundError("Neither total_count.txt nor letter_links.txt found.")


def check_total_files(expected_total, temp_dir):
    actual_total = len([name for name in os.listdir(temp_dir) if name.endswith('.csv')])
    if actual_total == expected_total:
        print("All files have been successfully scraped.")
    else:
        print(f"Some files are missing. Expected: {expected_total}, Actual: {actual_total}")
    return actual_total == expected_total


def check_failed_links(failed_file):
    if not os.path.exists(failed_file):
        return True
    with open(failed_file, 'r') as file:
        failed_links = file.read().splitlines()

    if len(failed_links) == 0:
        print("No failed links.")
    else:
        print(f"There are {len(failed_links)} failed links that need to be retried.")
    return len(failed_links) == 0


def validate_csv_file(filename):
    with open(filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader, None)
        if headers != ['Title', 'Date', 'Content']:
            return False
        for row in reader:
            if len(row) != 3:
                return False
    return True


def check_csv_files(temp_dir):
    valid_files = []
    invalid_files = []

    for filename in os.listdir(temp_dir):
        if filename.endswith('.csv'):
            if validate_csv_file(os.path.join(temp_dir, filename)):
                valid_files.append(filename)
            else:
                invalid_files.append(filename)

    print(f"Valid files: {len(valid_files)}")
    print(f"Invalid files: {len(invalid_files)}")
    return len(invalid_files) == 0


def check_log_file(log_file):
    if not os.path.exists(log_file):
        return True
    with open(log_file, 'r') as file:
        log_contents = file.read()

    if "Error" in log_contents:
        print("There are errors in the log file that need to be addressed.")
        return False
    else:
        print("No errors found in the log file.")
        return True


def clear_log_file(log_file):
    with open(log_file, 'w'):
        pass


def delete_temp_files(temp_dir, progress_file, failed_file, total_count_file):
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    if os.path.exists(progress_file):
        os.remove(progress_file)
    if os.path.exists(failed_file):
        os.remove(failed_file)
    if os.path.exists(total_count_file):
        os.remove(total_count_file)
    print("Temporary files have been deleted.")


def main():
    all_checks_passed = True

    expected_total = get_expected_total()

    print("Checking total files...")
    total_files_check = check_total_files(expected_total, TEMP_DIR)
    all_checks_passed &= total_files_check

    print("Checking failed links...")
    failed_links_check = check_failed_links(FAILED_FILE)
    all_checks_passed &= failed_links_check

    print("Checking CSV files...")
    csv_files_check = check_csv_files(TEMP_DIR)
    all_checks_passed &= csv_files_check

    # 只有在其他所有检查都通过时才检查日志文件
    if all_checks_passed:
        print("All checks passed. Scraping process completed successfully.")
        clear_log_file(LOG_FILE)
        delete_temp_files(TEMP_DIR, PROGRESS_FILE, FAILED_FILE, TOTAL_COUNT_FILE)
    else:
        print("Some checks failed. Please review the issues above.")
        print("Checking log file...")
        log_file_check = check_log_file(LOG_FILE)
        if log_file_check:
            clear_log_file(LOG_FILE)
            print("Log file errors have been cleared.")

if __name__ == "__main__":
    main()
