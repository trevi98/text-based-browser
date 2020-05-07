# write your code here
import os
import sys
import requests
from bs4 import BeautifulSoup
from colorama import init
from colorama import Fore, Style
import io

tabs = []
history = []


def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)


def modify_name(url):
    if url.startswith("https://"):
        url=url[8:]
    elif url.startswith("http://"):
        url=url[7:]
    return url.rsplit(".",1)[0]

def validate_url(url):
    while True:
        try:
            if "." in url or url in ["exit","back"] or url in tabs:
                return url
            raise Exception("error: url not valid")
        except Exception as e:
            print(e)
            url =input()



def make_request(url):
    if not url.startswith("https://"):
        url="https://"+url
    try:
        r=requests.get(url)
        return True,r
    except Exception as e:
        return False , "404 page not found"




def add_to_history(url):
    if url in history:
        history.remove(url)
    history.append(url)

def view_form_history():
    return history.pop()

def view_from_files(path,url):
    tab_name=modify_name(url)
    content = ""
    with open(f"{path}/{tab_name}.txt", "r") as tab:
        content = tab.read()
    return content


def save_to_files(path,content,url):
    tab_name=modify_name(url)
    with io.open(f"{path}/{tab_name}.txt", "w",encoding="utf-8") as tab:
        tab.write(content)
    tabs.append(tab_name)


def render_page(content,b):
    if b:
        content=BeautifulSoup(content,'html.parser')
    tags=content.find_all(['p', 'a', 'ul', 'ol', 'li','h1','h1','h2','h3','h4','h5'])
    for tag in tags:
        if tag.name=="a":
            print(Fore.BLUE + " ".join(tag.get_text().split()))
        else:
            print(Style.RESET_ALL + " ".join(tag.get_text().split()))
        print(Style.RESET_ALL)



def main():
    args = sys.argv
    create_dir(args[1])
    init()
    temp=""
    while True:
        url=input()
        url= validate_url(url)

        if len(temp)>0:
            if not temp == url and url not in ["exit","back"]:
                add_to_history(temp)

        if url=="exit":
            break

        elif url=="back":
            if len(history)>0:
                url=view_form_history()
                content=view_from_files(args[1],url)
                render_page(content,True)
        else:
            if url in tabs:
                content=view_from_files(args[1],url)
                render_page(content,True)
            else:
                connection , r=make_request(url)
                if not connection:
                    print(r)
                    continue
                else:
                    content=BeautifulSoup(r.content,'html.parser')
                    save_to_files(args[1],str(content),url)
                    render_page(content,False)
            temp=url

main()