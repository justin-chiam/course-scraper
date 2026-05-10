# UNSW Course Scraper

A Python web scraping project that helps users explore UNSW courses using the UNSW timetable and handbook websites.
This program is designed for students who want a faster way to browse potential courses or electives to take, filtering by faculty, school, subject area and course level, and then viewing handbook details such as the course overview and enrolment conditions.

The program allows users to:
- choose between undergraduate or postgraduate courses
- browse courses by faculty and school
- select a subject area (e.g. COMP, MATH, SENG)
- filter courses by course level (Level 1, Level 2, etc)
- retrieve course information from the UNSW handbook
- display the course overview and enrolment conditions/prerequisites

This project is an independent project and is not affiliated with, endorsed by, or maintained by UNSW Sydney.

## Features
In the main use case, the user is guided through a series of menus. They choose whether they are interested in undergraduate or postgraduate courses, choose a faculty, choose a school, choose a subject area, filter courses by level, and finally select a course. The program then opens the relevant UNSW handbook page and prints the course overview and conditions for enrolment.

The program also supports a direct course lookup mode using the "-c" or "--course" command-line argument. This skips the menu system and directly retrieves handbook information for the selected course code. For example,
```sh
python project.py -c COMP2521
```

## Installation
Install the Python dependencies:
```sh
pip install -r requirements.txt
```
Install the Chromium browser used by playwright:
```sh
python -m playwright install chromium
```
Then, run the program:
```sh
python project.py
```
Or, alternatively, use direct course lookup:
```sh
python project.py --course COMP1511
```