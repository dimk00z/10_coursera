import requests
from lxml import etree
from bs4 import BeautifulSoup
from openpyxl import Workbook


COURSERA_URL = 'https://www.coursera.org/sitemap~www~courses.xml'


def get_courses_info_from_url(url, courses_count=20):
    courses_tree = etree.fromstring(requests.get(url).content)
    courses_list = [course.getchildren()[0].text
                    for course in courses_tree[:courses_count]]
    return [parser_course_page(requests.get(course_url).content)
            for course_url in courses_list]


def parser_course_page(course_content):
    course_info = {}
    soup = BeautifulSoup(course_content, 'html.parser')
    title = soup.find('h1', {'class': 'title display-3-text'})
    course_info['title'] = title.text if title else ''
    language_info = soup.find(
        'div', {'class': 'language-info'})
    course_info['language_info'] = language_info.text if language_info else ''
    startdate = soup.find('div', {'class': 'startdate'})
    course_info['startdate'] = startdate.text if startdate else ''
    weeks = soup.find('div', {'class': 'rc-WeekView'})
    course_info['weeks'] = len(weeks) if weeks else ''
    ratings = soup.find('div', {'class': 'ratings-text'})
    course_info['ratings'] = ratings.text if ratings else ''
    return course_info


def get_courses_rows(courses_info):
    courses_rows = []
    courses_rows.append(['Course name', 'Language', 'Start date',
                         'Number of weeks', 'Rating'])
    for course_info in courses_info:
        courses_rows.append([course_info['title'],
                             course_info['language_info'],
                             course_info['startdate'],
                             course_info['weeks'],
                             course_info['ratings']])
    return courses_rows


def output_courses_info_to_xlsx(courses_rows,
                                filepath='output.xlsx'):
    xlsx_book = Workbook()
    sheet = xlsx_book.active
    for row in courses_rows:
        sheet.append(row)
    xlsx_book.save(filepath)
    return filepath


if __name__ == '__main__':
    courses_info = get_courses_info_from_url(COURSERA_URL)
    courses_rows = get_courses_rows(courses_info)
    out_file_name = output_courses_info_to_xlsx(courses_rows)
    print("Данные сохранены в {}".format(out_file_name))
