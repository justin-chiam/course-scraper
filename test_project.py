import project
import pytest


def test_clean_text():
    assert project.clean_text("     hello       world      ") == "hello world"


def test_classify_faculty():
    assert project.classify_faculty("School of Computer Sci & Eng") == "Engineering"
    assert project.classify_faculty("School of Cybersecurity") == "Other / Unclassified"


def test_get_course_level():
    assert project.get_course_level("COMP1511") == "Level 1"
    assert project.get_course_level("COMP2521") == "Level 2"
    assert project.get_course_level("COMP3331") == "Level 3"
    assert project.get_course_level("NOTACOURSE") == "Other"


def test_validate_course_code():
    assert project.validate_course_code("comp1511") == "COMP1511"
    assert project.validate_course_code("          math1141       ") == "MATH1141"
    with pytest.raises(ValueError):
        project.validate_course_code("COMP99999")


def test_get_handbook_level():
    assert project.get_handbook_level("COMP3821") == "Undergraduate"
    assert project.get_handbook_level("COMP9024") == "Postgraduate"


def test_format_section_lines():
    lines = [
        "Topics include:",
        "Fundamental programming concepts",
        "Introduction to Computer Science",
        "The C programming language and use of a C compiler",
    ]

    assert project.format_section_lines(lines) == [
        "Topics include:",
        "- Fundamental programming concepts",
        "- Introduction to Computer Science",
        "- The C programming language and use of a C compiler",
    ]
