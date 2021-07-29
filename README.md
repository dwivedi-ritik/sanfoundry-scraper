# sanfoundry-scraper

This repo is the fork of [this repo](https://github.com/raprocks/sanfoundry-scraper) with some little extra weirdo features 🤠.

- Scrape HTML
- You can make pdf of all quizs
- Support faster scrapping with multithreading
- Support json response

Extracts all MCQs of a subject that you input the link of.

run the `python main.py` file after getting the code using the Download zip button or following this [link](https://github.com/dwivedi-ritik/sanfoundry-scraper).

```terminal
usage:
python main.py

A CLI Tool for scrapping quizs from SANFOUNDARY

optional arguments:
-h, --help show this help message and exit
--url URL URL of quiz
--pdf Generate PDF File
--thread Uses Multithreading for scrapping
--json return all quizs in json format
--workers WORKERS Maximum number of threads[ More number More speed but More
Unstability]

Batmobile lost the wheel lol
```

just run main.py using the following command

```bash
python main.py
```

or

```bash
python main.py --url {url-of-quiz}
```

this scrapper also uses multithreading

```bash
python main.py --url {url-of-quiz} --thread
```

Here workers are the number of threads. Default workers are 5 .

You can change by passing `--workers {thread-choice}` eg `--workers 10`.

note - More workers can cause unstability

You can make pdf of scrapped quiz

```bash
python main.py --url {url-of-quiz} --thread --pdf
```

Get json file of all yours quizs

```bash
python main.py --url {url-of-quiz} --json
```

### Basic Guide

Input the URL of the Subject (for example, "https://www.sanfoundry.com/1000-object-oriented-programming-oops-questions-answers/") and run it to get a file in a folder named
`Saved_MCQs` of all the MCQs of the subject.

run the following command if you are using the program for the first time.

```bash
pip install -r requirements.txt
```
to install requirements.

after that just run `python main.py` with required flags.

### Notes

Wheasyprint require gtk libraries so if you running windows machine which does not have gtk libraries you may require to download [GTK for windows runtime envoironment](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases/tag/2021-04-29) libraries .


LOG: This is getting traction hehe so gonna make it better to use and better at output

1. PDF Output instead of HTML or maybe optional idk
2. setup script so that installable from pip
3. good docs 💀
4. plain text output format with just questions and answers in txt. easier to "study" xD.
