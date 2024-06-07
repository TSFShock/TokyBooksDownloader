import re
import json5
import requests
from pathlib import Path
from tqdm import tqdm
import time

def get_chapter_content(chapter_data):
    BASE_URLS = ['https://files01.tokybook.com/audio/',  'https://files02.tokybook.com/audio/']

    for base_url in BASE_URLS:
        response = requests.get(base_url + chapter_data['chapter_link_dropbox'], stream=True)
        if response.status_code == 200:
            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024  # 1 Kibibyte
            progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)
            with open(chapter_data['name'] + '.mp3', 'wb') as f:
                for data in response.iter_content(block_size):
                    progress_bar.update(len(data))
                    f.write(data)
                    progress_bar.set_description(f'Downloading {chapter_data["name"]}')
            progress_bar.close()
            return True
        
    print('[FAILED] Failed to download chapter', chapter_data['name'])
    print(response.text)
    return False

def download_chapter(chapters_queue: list):
    chapter_info = chapters_queue.pop()
    print(chapter_info)
    chapter_file = Path('./MP3/' + chapter_info['name'] + '.mp3')
    chapter_file.touch(exist_ok=True)

    start_time = time.time()
    downloaded = get_chapter_content(chapter_info)
    if downloaded:
        end_time = time.time()
        download_speed = chapter_file.stat().st_size / (end_time - start_time) / 1024  # KB/s
        print(f'Download speed: {download_speed:.2f} KB/s')

def extract_chapters_data(web_page_response: str) -> list:
    data = re.search(r"tracks\s*=\s*(\[[^\]]+\])\s*", web_page_response)
    parsed_data_str = data.group(1)
    parsed_data = json5.loads(parsed_data_str)
    
    # It is necessary to remove the first chapter entry, since it is not an actual chapter but rather 
    # an audio from tokybook's website
    parsed_data.pop(0)
    return parsed_data

def get_tokybook_data(tokybook_url: str):
    response = requests.get(tokybook_url)
    return response.text

if __name__ == '__main__':
    # Prompt the user to enter the URL
    tokybook_url = input("Please enter the Tokybook URL: ")
    
    toky_response = get_tokybook_data(tokybook_url)
    chapters_datas = extract_chapters_data(toky_response)
    
    # Ensure the MP3 directory exists
    Path('./MP3').mkdir(exist_ok=True)
    
    while chapters_datas:
        download_chapter(chapters_datas)
