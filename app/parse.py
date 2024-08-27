import csv
from dataclasses import dataclass, fields, astuple

import requests
from bs4 import BeautifulSoup


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


BASE_URL = "https://mate.academy/"
COURSES_FIELDS = [field.name for field in fields(Course)]


def get_single_course(soup: BeautifulSoup) -> Course:
    return Course(
        name=soup.select_one(".ProfessionCard_title__Zq5ZY").text,
        short_description=soup.select_one(".ProfessionCard_cardWrapper__JQBNJ > .mb-32").text,
        duration=soup.select_one(".ProfessionCard_subtitle__K1Yp6").text.split("•")[0],
    )


def fetch_and_parse():
    courses = requests.get(BASE_URL).content
    soup = BeautifulSoup(courses, "html.parser")
    return soup


def get_all_courses() -> list[Course]:
    soup = fetch_and_parse()
    courses = []
    for course_soup in soup.select(".ProfessionCard_cardWrapper__JQBNJ"):
        courses.append(get_single_course(course_soup))
    return courses


def write_to_csv() -> None:
    all_courses = get_all_courses()
    with open("courses.csv", "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(COURSES_FIELDS)
        writer.writerows([astuple(course) for course in all_courses])


def main():
    write_to_csv()


if __name__ == "__main__":
    main()

