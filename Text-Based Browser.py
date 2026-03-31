import argparse
import os
import requests
from bs4 import BeautifulSoup
from colorama import Fore
from colorama import Style

nytimes_com = '''
This New Liquid Is Magnetic, and Mesmerizing

Scientists have created "soft" magnets that can flow 
and change shape, and that could be a boon to medicine 
and robotics. (Source: New York Times)


Most Wikipedia Profiles Are of Men. This Scientist Is Changing That.

Jessica Wade has added nearly 700 Wikipedia biographies for
 important female and minority scientists in less than two 
 years.

'''

bloomberg_com = '''
The Space Race: From Apollo 11 to Elon Musk

It's 50 years since the world was gripped by historic images
 of Apollo 11, and Neil Armstrong -- the first man to walk 
 on the moon. It was the height of the Cold War, and the charts
 were filled with David Bowie's Space Oddity, and Creedence's 
 Bad Moon Rising. The world is a very different place than 
 it was 5 decades ago. But how has the space race changed since
 the summer of '69? (Source: Bloomberg)


Twitter CEO Jack Dorsey Gives Talk at Apple Headquarters

Twitter and Square Chief Executive Officer Jack Dorsey 
 addressed Apple Inc. employees at the iPhone maker’s headquarters
 Tuesday, a signal of the strong ties between the Silicon Valley giants.
'''

def match_url_to_contents(url):
    url_pairs = {
        "bloomberg.com": bloomberg_com,
        "nytimes.com": nytimes_com
    }

    if url in url_pairs:
        return url_pairs[url]
    else:
        response = get_url_request(url)
        if response:
            return response

    return None

def get_url_request(url):
    fix_url = url
    if not url.startswith("https://"):
        fix_url = url.replace("http://", "https://")
        if not fix_url.startswith("https://"):
            fix_url = f"https://{url}"

    try:
        response = requests.get(fix_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        tags = ['p', 'a', 'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
        page = ""
        for descendant in soup.body.descendants:
            if descendant.name in tags:
                if descendant.name == 'a':
                    page += Fore.BLUE + descendant.get_text().strip()
                else:
                    page += Style.RESET_ALL + descendant.get_text().strip()
        return page
    except requests.RequestException:
        return None

def parse_args():
    parser = argparse.ArgumentParser(description="My program")
    parser.add_argument('dir', type=str, help='Directory to save files')
    args = parser.parse_args()
    return args

def validate_url(user_string):
    if "." in user_string and any(suffix in user_string for suffix in [".com", ".org", ".edu"]):
        return user_string
    else:
        return None

def validate_dir(dir_path):
    try:
        os.makedirs(dir_path, exist_ok=True)
        return dir_path
    except OSError:
        return None

def print_page_content(url_contents):
    print(url_contents)

def save_page_content(dir_path, file_name, contents):
    file_path = os.path.join(dir_path, file_name.split('.')[0])
    with open(file_path, 'w') as f:
        f.write(contents)



def main():
    args = parse_args()
    dir_to_save_urls = args.dir
    dir_result = validate_dir(dir_to_save_urls)
    if dir_result is None:
        print("Error: Invalid directory")
        return

    stack = []
    while True:
        url = input()
        if url == 'exit':
            break

        if url == "back" and stack:
            stack.pop()
            url = stack[-1]
        elif url == "back":
            continue

        valid_url_name = validate_url(url)
        url_contents = match_url_to_contents(url)


        if valid_url_name and url_contents:
            stack.append(url)
            print_page_content(url_contents)
            save_page_content(dir_result, valid_url_name, url_contents)
        else:
            print("Error: Invalid URL")
            continue

"/home/master/PycharmProjects/Text-Based Browser/Text-Based Browser/task/browser.py"
if __name__ == '__main__':
    main()
