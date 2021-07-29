import os
import requests
from typing import List, Optional, Dict

from bs4 import BeautifulSoup
from weasyprint import HTML, CSS

from pagescrape import pagescrape


def write_to_html(data: BeautifulSoup, filename):
    if not os.path.exists("Saved_MCQs"):
        os.mkdir("Saved_MCQs")
    head = BeautifulSoup("""
    <head>
    <script>
      MathJax = {
        tex: {
          inlineMath: [['$', '$'], ['\\(', '\\)']]
        }
      };
    </script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js">
    </script>
    </head>""", "lxml")
    data.body.insert_before(head)

    with open(f"./Saved_MCQs/{filename}.html", "w+", encoding="utf-8") as file:
        file.write(str(data.prettify()))

# This function does not work everytime


def write_to_formated_html(pages: List[str], file_name: str, write_pdf: Optional[bool] = False):
    LORD_MD: str = ""
    for module, link in pages.items():
        temp = f"<h4><i>{module}<i></h4>\n"
        for count, quiz in enumerate(mcqscrape_json(link)):
            temp += f"<p>{count + 1}. {quiz['question']}</p>\n"
            temp += "<ol type='a'>\n"
            for q in quiz["options"]:
                temp += f"<li>{q}</li>\n"
            temp += "</ol>"
            temp += f"<p><b>Answer:</b> {quiz['answer']}</p>\n"
            temp += f"<p>{quiz['explanation']}</p>\n"
        LORD_MD += temp

    with open(f"./Saved_MCQs/{file_name}.html", "w") as f:
        f.write(LORD_MD)
    inp = input("WeasyPrint is known to be slow and Converting html to pdf is resource taking and freezing can occur due to high ram use if pages are above 50 please close other apps. Are you sure ? (yes/no)")
    if write_pdf:
        if not os.path.exists("Saved_PDFs"):
            os.mkdir("Saved_PDFs")
        if inp.lower() != "no":
            HTML(filename=f"./Saved_MCQs/{file_name}.html").write_pdf(
                f"./Saved_PDFs/{file_name}.pdf", stylesheets=[CSS(string='body { font-size: 13px }')])


def mcqscrape_json(url) -> Dict[str, str]:
    content: str = requests.get(url).content
    soup = BeautifulSoup(content, "lxml")
    q_content = soup.find("div", "entry-content")
    coll = q_content.find_all("div", "collapseomatic_content")
    mcq_json: List = []
    for c in coll:
        question, code, pre_code, answer,  explain, options, = None, None, None, None, None, None
        prevs = c.find_previous_siblings()
        res = prevs[0].text
        if res[0].isdigit():
            if prevs[0].span:
                prevs[0].span.decompose()
                temp_qna = res.split("\n")
                question, *options = temp_qna
        else:
            try:
                if prevs[2]['class'][0] == "sf-mobile-ads":
                    question = prevs[3].text
            except KeyError as e:
                question = prevs[2].text
            try:
                if prevs[1].name == "pre":
                    pre_code = prevs[1].text
                if prevs[1]['class'][0] == "hk1_style-wrap5":
                    code = prevs[1].text
            except KeyError as e:
                pass
            options = prevs[0].text.split("\n")
        answer, *temp_explain = c.text.split("\n")
        explain = "".join(temp_explain)
        mcq_json.append({
            "question": question,
            "pre_code": pre_code,
            "code": code,
            "options": options,
            "answer": answer,
            "explaination": explain
        })
    return mcq_json


def mcqscrape_html(url: str) -> str:
    if '1000' in url:
        pages = pagescrape(url)
        mega_html = ''
        for k, v in pages.items():
            print("getting", k, "from ->", v, end=' ... ')
            mega_html += mcqscrape_html(v)
            print("Done!")
        write_to_html(BeautifulSoup(mega_html, 'lxml'),
                      url.split('/')[-2])
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'lxml')
    content = soup.find('div', class_='entry-content')
    # print(content.prettify())
    paras = content.findAll('p')
    classes_to_remove = ["sf-mobile-ads",
                         "desktop-content", "mobile-content", "sf-nav-bottom"]
    tags_to_remove = ["script"]
    # remove the answer drop downs
    [sp.decompose() for sp in content.findAll('span', class_="collapseomatic")]
    for class_to_remove in classes_to_remove:
        [sp.decompose() for sp in content.findAll('div',
                                                  class_=class_to_remove)]
    for tag_to_remove in tags_to_remove:
        [sp.decompose() for sp in content.findAll(tag_to_remove)]
    for tag in paras[-3:]:
        tag.decompose()
    [tag.extract() for tag in content.find_all(
        "div") if tag.text == "advertisement"]
    # span attribute cleanup
    for tag in content.findAll(True):
        tag.attrs.pop("class", "")
        tag.attrs.pop("id", "")
    try:
        heading = soup.find(
            'h1', class_="entry-title").text.split('–')[1].strip()
        print(heading)
    except IndexError:
        print("cant get heading", IndexError)
        print(str(content)[:100])
        return ''
    return content.prettify()
