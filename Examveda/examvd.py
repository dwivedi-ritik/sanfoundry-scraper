import requests
from bs4 import BeautifulSoup
from typing import List, Set

ARRAY_OF_QUIZ: Set = set()


def return_quizs(url: str) -> List:
    global ARRAY_OF_QUIZ
    res: str = requests.get(url)
    if res.status_code == 200:
        dummy_content = res.content
    else:
        raise Exception("No valid url")

    soup: BeautifulSoup = BeautifulSoup(dummy_content, "lxml")
    main_content: BeautifulSoup = soup.find("div", "col-md-8")

    quiz_cont: BeautifulSoup = main_content.find_all(
        'article', "question-type-normal")
    formated_quiz_cont: List[BeautifulSoup] = [format_el
                                               for format_el in quiz_cont if format_el.find('div', 'row')]

    for el in formated_quiz_cont:
        el.find('div', 'answer_container')['style'] = ''
        el.find('div', "question-bottom").decompose()
        print('quiz scrapped')
        ARRAY_OF_QUIZ.add(el)


def return_content_url(soup: BeautifulSoup) -> List[str]:

    main_content: BeautifulSoup = soup.find("div", "col-md-8")
    all_sections: BeautifulSoup = main_content.find("div", "chapter-section")

    # This contains links of all section
    all_sections_links: List[str] = [url["href"]
                                     for url in all_sections.find_all("a")]
    return all_sections_links


def main(url: str) -> None:
    file_name: str = url.split("/")[-1]
    res: str = requests.get(url)
    if res.status_code == 200:
        dummy_content: str = res.content
    else:
        raise Exception("No valid url")

    soup: BeautifulSoup = BeautifulSoup(dummy_content, "lxml")

    page_content: BeautifulSoup = soup.find("div", "pagination")

    # This will contains the links of all pages
    all_pages: Set = {url["href"] for url in page_content.find_all("a")}

    # This will contain all sections
    total_section: List[str] = return_content_url(soup)

    all_urls: List[str] = []
    for page, _ in enumerate(all_pages):
        for section,  _ in enumerate(total_section):
            all_urls.append(f"{url}?page={page+1}&section={section+1}")

    for url in all_urls:
        try:
            return_quizs(url)
        except Exception as e:
            pass

    MEGA_HTML = ''
    for q in ARRAY_OF_QUIZ:
        MEGA_HTML += str(q)

    with open(f"{file_name}.html", "w") as f:
        f.write(MEGA_HTML)


# A exam veda scrapped which scrape all the quizs from examveda
if __name__ == "__main__":
    main("https://www.examveda.com/computer-fundamentals/practice-mcq-question-on-operating-system/")
