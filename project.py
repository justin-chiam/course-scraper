from datetime import date
import re
import requests
import sys
from pyfiglet import Figlet

from bs4 import BeautifulSoup

YEAR = date.today().year
TIMETABLE_BASE = f"https://timetable.unsw.edu.au/{YEAR}"
TIMETABLE = TIMETABLE_BASE + "/subjectSearch.html"

HANDBOOK = "https://www.handbook.unsw.edu.au"

class SubjectArea:
    def __init__(self, code, name, offered_by, faculty, url):
        self.code = code
        self.name = name
        self.offered_by = offered_by
        self.faculty = faculty
        self.url = url

class Course:
    def __init__(self, code, title, uoc, url):
        self.code = code
        self.title = title
        self.uoc = uoc
        self.url = url

FACULTIES = {
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
    ]
}

def fetch_soup(url):
    """Fetch a page from a URL and return BeautifulSoup."""
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")

def clean_text(text):
    return re.sub(r"\s+", " ", text).strip()

def choose_from_list(title, options):
    """Print numbered options and ask the user to choose one."""
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

def classify_faculty(offered_by):
    """Find the main faculty from the timetable "Offered by" text."""
    offered_by = offered_by.lower()
    for faculty, keywords in FACULTIES.items():
        for keyword in keywords:
            if keyword.lower() in offered_by:
                return faculty
    return "Other / Unclassified"

def extract_subject_areas():
    """Scrape subject areas from main timetable page."""
    soup = fetch_soup(TIMETABLE)
    subjects = []

    # Timetable page is table-based. Useful rows contain:
    # Course code (with link), subject area (with link), "offered-by" text
    for row in soup.find_all("tr"):
        cells = [clean_text(cell.get_text(" ", strip="True")) for cell in row.find_all("td")]
        if len(cells) < 3:
            continue

        links = row.find_all("a", href=True)
        if not links:
            continue

        code = clean_text(links[0].get_text(" ", strip=True))
        if not re.fullmatch(r"[A-Z]{4}", code):
            continue

        href = links[0]["href"]
        if ".html" not in href:
            continue

        name = clean_text(links[1].get_text(" ", strip=True)) if len(links) > 1 else cells[1]
        offered_by = cells[-1]
        url = TIMETABLE_BASE + "/" + href
        faculty = classify_faculty(offered_by)

        subjects.append(SubjectArea(code=code, name=name, offered_by=offered_by, faculty=faculty, url=url))

    return subjects

def extract_courses(subject, level):
    """Scrape courses from a specific subject area page for either undergraduate or postgraduate."""
    soup = fetch_soup(subject.url)
    courses = []
    in_level_section = False

    for row in soup.find_all("tr"):
        text = clean_text(row.get_text(" ", strip=True))

        if text == level:
            in_level_section = True
            continue

        if text in ["Undergraduate", "Postgraduate", "Research"] and text != level:
            in_level_section = False
            continue

        if not in_level_section:
            continue
        
        cells = [clean_text(cell.get_text(" ", strip=True)) for cell in row.find_all("td")]
        if len(cells) < 3:
            continue

        links = row.find_all("a", href=True)
        if not links:
            continue

        code = clean_text(links[0].get_text(" ", strip=True))
        if not re.fullmatch(r"[A-Z]{4}\d{4}", code):
            continue

        title = clean_text(links[1].get_text(" ", strip=True)) if len(links) > 1 else cells[1]
        uoc = cells[-1]
        url = TIMETABLE_BASE + "/" + links[0]["href"]
        courses.append(Course(code=code, title=title, uoc=uoc, url=url))
    
    return courses

def get_course_level(course_code):
    """Return the course level based on the first digit in the course code."""
    match = re.fullmatch(r"[A-Z]{4}(\d)\d{3}", course_code)
    if not match:
        return "Other"
    return f"Level {match.group(1)}"

def filter_courses_by_level(courses):
    """Ask the user which course level they want, then return courses under that course level"""
    available_levels = sorted(
        set(get_course_level(course.code) for course in courses),
        key=lambda level: int(level.split()[1]) if level.startswith("Level ") else -1,
    )

    level_options = []
    for course_level in available_levels:
        count = sum(1 for course in courses if get_course_level(course.code))
        level_options.append(f"{course_level} courses ({count})")
    
    # Add another option to list all courses within the subject area
    level_options.append(f"All levels ({len(courses)})")

    selected_level_text = choose_from_list("Course level within this subject area", level_options)

    if selected_level_text.startswith("All levels"):
        return courses
    
    selected_level = selected_level_text.split(" courses", 1)[0]
    return [course for course in courses if get_course_level(course.code) == selected_level]

def main():
    print(Figlet(font="small").renderText(f"UNSW Course Scraper {YEAR}"))
    print("This scraper uses the UNSW timetable page to find courses and the UNSW Handbook for details.")

    level = choose_from_list("Degree level", ["Undergraduate", "Postgraduate"])

    print("\nLoading main faculties...")
    faculties = list(FACULTIES.keys())
    selected_faculty = choose_from_list("Main faculty", faculties)

    subjects = extract_subject_areas()
    if not subjects:
        print("No subject areas found. Timetable page may have changed.")
        sys.exit(1)
    faculty_subjects = [subject for subject in subjects if subject.faculty == selected_faculty]
    schools = sorted(set(subject.offered_by for subject in faculty_subjects))
    selected_school = choose_from_list("School", schools)

    school_subjects = [subject for subject in faculty_subjects if subject.offered_by == selected_school]
    subject_options = [f"{subject.code} - {subject.name}" for subject in school_subjects]
    selected_subject_text = choose_from_list("Subject areas", subject_options)
    selected_subject_code = selected_subject_text.split(" - ")[0]
    selected_subject = None
    for subject in subjects:
        if subject.code == selected_subject_code:
            selected_subject = subject
            break
    
    print(f"\nLoading {level} courses for {selected_subject.code} subject area...")
    courses = extract_courses(selected_subject, level)
    if not courses:
        print(f"No {level} courses found for {selected_subject.code}.")
        sys.exit(0)

    filtered_courses = filter_courses_by_level(courses)
    if not filtered_courses:
        print("No courses found for that level.")
        sys.exit(0)


if __name__ == "__main__":
    main()