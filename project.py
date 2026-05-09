from datetime import date
import re
import requests
import sys
from pyfiglet import Figlet

from bs4 import BeautifulSoup

YEAR = date.today().year
TIMETABLE = f"https://timetable.unsw.edu.au/{YEAR}/subjectSearch.html"
HANDBOOK = "https://www.handbook.unsw.edu.au"

class SubjectArea:
    def __init__(self, code, name, school, faculty, url):
        self.code = code
        self.name = name
        self.school = school
        self.faculty = faculty
        self.url = url

class Course:
    def __init__(self, code, title, uoc, url):
        self.code = code
        self.title = title
        self.uoc = uoc
        self.url = url

FACULTY_KEYWORDS = {
    "Arts, Design & Architecture": [
        "Architectural Studies Program",
        "Building Construction Mgt Prog",
        "Faculty of Arts, Design & Arch",
        "Industrial Design Program",
        "Interior Architecture Program",
        "Landscape Architecture Program",
        "Linguistics",
        "Planning & Urban Development",
        "School Humanities & Languages",
        "School of Art & Design",
        "School of Education",
        "School of Social Sciences",
        "School of the Arts & Media",
        "Social Research in Health",
    ],
    "Business School": [
        "AGSM MBA Programs",
        "School of Acctng, Audit & Tax",
        "School of Banking & Finance",
        "School of Economics",
        "School of Management & Gov'nce",
        "School of Marketing",
        "School of Risk & Actuarial St",
        "Sch Info Sys and Tech Mgmt",
        "UNSW Business School",
    ],
    "Engineering": [
        "Faculty of Engineering",
        "Grad. School of Biomedical Eng",
        "Grad. School of Engineering",
        "Minerals Energy Resources Eng",
        "Photovoltaic Engineering",
        "School of Chemical Engineering",
        "School of Civil & Env Eng",
        "School of Computer Sci & Eng",
        "School of Elec Eng & Telco",
        "School of Materials Sci & Eng",
        "School of Mech & Manf. Eng",
        "School of Mining Engineering",
        "School of Petroleum Eng",
    ],
    "Law & Justice": [
        "Faculty of Law and Justice",
    ],
    "Medicine & Health": [
        "Faculty of Medicine and Health",
        "Schl of Optometry & Vision Sci",
        "School of Biomedical Sciences",
        "School of Clinical Medicine",
        "School of Health Sciences",
        "School of Population Health",
    ],
    "Science": [
        "Faculty of Science",
        "Sch Biol, Earth & Environ Sci",
        "Sch Biotech & Biomolecular Sci",
        "Sch Mathematics & Statistics",
        "School of Aviation",
        "School of Chemistry",
        "School of Physics",
        "School of Psychology",
    ],
    "Other / Unclassified": [
        "Canberra Sch of Prof Studies",
        "Div. Registrar & Deputy Princ",
        "Nura Gili Indigenous Programs",
        "Std Acad & Career Success",
        "Student Administration Dept",
        "UC Humanities and Soc Science",
        "UC School of Business",
        "UC Science",
        "UNSW Canberra at ADFA",
        "UNSW College Diplomas",
    ],
}

def fetch_soup(url):
    """Fetch a page from a URL and return BeautifulSoup."""
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")

def choose_from_list(title, options):
    if not options:
        raise ValueError(f"No options available for {title}")
    
    print(f"\n{title}")
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")

    while True:
        choice = input("Select: ").strip()
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(options):
                return options[idx - 1]
        print("Invalid selection. Try again.")


def main():
    print(Figlet(font="small").renderText(f"UNSW Course Scraper {YEAR}"))
    print("This scraper uses the UNSW timetable page to find courses and the UNSW Handbook for details.")

    level = choose_from_list("Degree level", ["Undergraduate", "Postgraduate"])











if __name__ == "__main__":
    main()