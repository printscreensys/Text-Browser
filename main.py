import argparse
import os
from collections import deque
import requests
from bs4 import BeautifulSoup
from colorama import init, Fore

def make_text(text, links):
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    blue = Fore.BLUE
    reset = Fore.RESET
    links = [link.text for link in links]
    for l in links:
        i = text.find(l)
        text = text[:i]+(blue+l+reset)+text[i+len(l):]
    return text

init()
parser = argparse.ArgumentParser()
parser.add_argument('dir')
args = parser.parse_args()
try:
    os.mkdir(args.dir)
except OSError:
    pass

history = deque()
url = input()
while url != 'exit':
    if '.' in url:
        if not url.startswith('http'):
            url = 'https://' + url
        domain = url.split('/')[2].split('.')[0]
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        page = soup.get_text()
        links = soup.find_all('a')
        page = make_text(page, links)
        print(page)
        with open(file = args.dir + '\\' + domain, mode = 'w', encoding = 'utf-16') as f:
            f.write(page)
        history.appendleft(page)
    elif url == 'back':
        print(history.pop())
    else:
        try:
            with open(args.dir+'\\'+url, 'r') as f:
                print(f.read())
        except OSError:
            print('Error: Incorrect URL')

    url = input()