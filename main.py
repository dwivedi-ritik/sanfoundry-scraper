import sys
import time
import os
import json

from argparse import ArgumentParser
from typing import List ,Optional
from concurrent.futures import ThreadPoolExecutor
from weasyprint import HTML , CSS
from pagescrape import pagescrape
from mcqscrape import mcqscrape_html, write_to_html  , mcqscrape_json
from bs4 import BeautifulSoup
from pprint import pprint

#added a little cli helper
parser = ArgumentParser(description="A CLI Tool for scrapping quizs from SANFOUNDARY" , usage="Try python main.py --url quiz_url", epilog="Batmobile lost the wheel lol")
parser.add_argument("--url" , help="URL of quiz" , type=str , default=None , dest="url")
parser.add_argument("--pdf" , help="Generate PDF File" , default=False , dest="pdf" ,action="store_true")
parser.add_argument("--thread" , action="store_true" , help="Uses Multithreading for scrapping")
parser.add_argument("--json" , help="return all quizs in json format" , action ="store_true" , default=False , dest="json")
parser.add_argument("--workers" , type=int , help="Maximum number of threads[ More number More speed but More Unstability]" , default=5 , metavar='')
parser.add_argument("--topic" , type=str , help="Filter only selected topic , pass in inverted commas" , default=None , dest="topic" ,metavar='')
args = parser.parse_args()

QUIZ_LIST: List[str] = []

def main(PAGE_URL: str ):
    MEGA_HTML = ''
    if PAGE_URL == '':
        print("Please Enter a URL!")
        sys.exit(0)
    pages = pagescrape(PAGE_URL , args.topic)
    
    if len(pages) == 0:
        MEGA_HTML += mcqscrape_html(PAGE_URL)
    else:
        for k, v in pages.items():
            print("getting", k, "from ->", v, end=' ... ')
            MEGA_HTML += mcqscrape_html(v)
            print("Done!")
    write_to_html(BeautifulSoup(MEGA_HTML, 'lxml'),
                  PAGE_URL.split('/')[-2])

#These both function is for multithreading
def writer(url: str) -> None:
    res: str = mcqscrape_html(url)
    QUIZ_LIST.append(res)

def async_main(url: str) -> None:
    pages: List[str] = [ v for _ , v in pagescrape(url , args.topic).items()]
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        #This will run writer function in multithread with each quiz url
        executor.map(writer , pages)

    MEGA_HTML = "".join(QUIZ_LIST)
    write_to_html(BeautifulSoup(MEGA_HTML, 'lxml'),
                  PAGE_URL.split('/')[-2])

def write_pdf(file_name: str) -> None:
    inp: str = input("\nWeasyPrint is known to be slow and Converting html to pdf is resource taking.High ram is normal in this process.\nif pages are above 50 please close other apps. Are you sure ? (yes/no) ")
    if not os.path.exists("Saved_PDFs"):
        os.mkdir("Saved_PDFs")
    if inp.lower() != "no":
        HTML(filename=f"./Saved_MCQs/{file_name}.html").write_pdf(f"./Saved_PDFs/{file_name}.pdf", stylesheets=[CSS(string='body { font-size: 13px }')])

def retrive_json(link: str , file_name: str):
    pages = pagescrape(link)
    dump_json = {
        file_name:{
        }
    }
    print(len(pages))
    if len(pages) == 0:
        dump_json[file_name]["Quizs"] = mcqscrape_json(link)
    else:
        for k, v in pages.items():
            print(f"{k}  has added.")
            dump_json[file_name][k] = mcqscrape_json(v)
    
    with open(file_name+".json", "w") as j:
        j.write(json.dumps(dump_json , indent=4))

if __name__ == "__main__":
    command = "Enter the URL of the Page where you see links of all Subject related MCQs: "
    PAGE_URL = args.url or input(command)
    file_name = PAGE_URL.split('/')[-2]
    
    condition_arr = [args.thread , args.json]

    if condition_arr.count(False) == 2:
        main(PAGE_URL)
    else:
        if args.thread:
            async_main(PAGE_URL)
        if args.json:
            retrive_json(PAGE_URL , file_name)
    
    if args.pdf:
        write_pdf(file_name)



"""
I did a test run with 10 workers on this link https://www.sanfoundry.com/1000-python-questions-answers/
Normal Function takes around 50 seconds , multithreading takes 17 seconds
"""
