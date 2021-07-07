# sanfoundry-scraper

Extracts all MCQs of a subject that you input the link of.

run the main.py file after getting the code using the Download zip button or following this [link](https://github.com/dwivedi-ritik/sanfoundry-scraper).

`usage:
python main.py --thread --workers 15

A CLI Tool for scrapping quizs from SANFOUNDARY

optional arguments:
-h, --help show this help message and exit
--url URL URL of quiz
--pdf Generate PDF File
--thread Uses Multithreading for scrapping
--json return all quizs in json format
--workers WORKERS Maximum number of threads[ More number More speed but More
Unstability]

Batmobile lost the wheel lol`

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
python main.py --url {url-of-quiz} --thread --workers 15
```

Here workers are the number of threads. Default workers are 5 .

You can change by passing `--workers {thread-choice}` .

More workers can cause unstability

Input the URL of the Subject (for example, "https://www.sanfoundry.com/1000-object-oriented-programming-oops-questions-answers/") and run it to get a file in a folder named
`Saved_MCQs` of all the MCQs of the subject.

run the following command if you are using the program for the first time.

```bash
pip install -r requirements.txt
```

and

```bash
python main.py --help
```

to install requirements

LOG: This is getting traction hehe so gonna make it better to use and better at output

1. PDF Output instead of HTML or maybe optional idk
2. setup script so that installable from pip
3. good docs 💀
4. plain text output format with just questions and answers in txt. easier to "study" xD.
