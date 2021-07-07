from pprint import pprint
import requests
from bs4 import BeautifulSoup
# from pagescrape import pagescrape
# from mcqscrape import mcqscrape_json
from weasyprint import HTML , CSS

def main() -> None:
    LORD_MD = ""
    url: str = "https://www.sanfoundry.com/1000-data-structure-questions-answers/"
    pages = pagescrape(url = url)
    
    for module , link in pages.items():
        temp = f"##### {module}\n"
        for count , quiz in enumerate(mcqscrape_json(link)):
            temp += f"{count+1}. {quiz['question']}\n"
            for q in quiz["options"]:
                temp += f"- {q}\n"
            temp += f"##### Answer: {quiz['answer']}\n"
            temp += f"##### Explanation: {quiz['explanation']}\n"
        LORD_MD += temp

    with open("op.md" , "w") as f:
        f.write(LORD_MD)

def codes(q_content , obj):
    coll = q_content.find_all("div" , "collapseomatic_content ")
    for co , ob in zip(coll , obj):
        prev = co.findPreviousSiblings()
        try:
            if prev[1]['class'][0] == "hk1_style-wrap5":
                ob['code'] = prev[1].text
        except KeyError as e:
            ob['code'] = None
    return obj


def main2() -> None:
    # HTML(filename="./Saved_MCQs/c-interview-questions-answers.html").write_pdf('test.pdf', stylesheets=[CSS(string='body { font-size: 10px }')])
    HTML(filename="ch.html").write_pdf('test.pdf', stylesheets=[CSS(string='body { font-size: 10px }')])

def find_without_code(content):
    soup = BeautifulSoup(content , "lxml")
    q_content = soup.find("div" , "entry-content")
    coll = q_content.find_all("div" , "collapseomatic_content")
    mcq_json = []
    for c in coll:
        question , code , pre_code , answer ,  explain , options, = None , None , None , None , None , None
        prevs = c.find_previous_siblings()
        res = prevs[0].text
        if res[0].isdigit():
            if prevs[0].span:
                    prevs[0].span.decompose()
                    temp_qna = res.split("\n")
                    question , *options = temp_qna
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
            # options
            options = prevs[0].text.split("\n")
        answer , *temp_explain = c.text.split("\n")
        explain = "".join(temp_explain)
        mcq_json.append({
            "question":question,
            "pre_code":pre_code,
            "code":code,
            "options":options,
            "answer":answer,
            "explaination":explain
        })
    return mcq_json

if __name__ == "__main__":
    url = "https://www.sanfoundry.com/c-programming-questions-answers-variable-names-1/"
    content = requests.get(url).content
    pprint(find_without_code(content))
