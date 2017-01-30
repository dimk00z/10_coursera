import requests
from lxml import etree
from bs4 import BeautifulSoup
from openpyxl import Workbook


def get_courses_list_from_url(url):
    courses_tree = etree.fromstring(requests.get(url).content)
    return [course.getchildren()[0].text
            for course in courses_tree]


def parser_course_page(course_content):
    course_info = {}
    soup = BeautifulSoup(course_content, 'html.parser')
    course_info['title'] = soup.find('div', {'class': 'title'}).text
    course_info['language_info'] = soup.find(
        'div', {'class': 'language-info'}).text
    course_info['startdate'] = soup.find('div', {'class': 'startdate'}).text
    weeks = soup.find('div', {'class': 'rc-WeekView'})
    course_info['weeks'] = len(weeks) if weeks else ''
    ratings = soup.find('div', {'class': 'ratings-text'})
    course_info['ratings'] = ratings.text if ratings else ''
    return course_info


def get_courses_info(courses_list, courses_count=20):
    return [parser_course_page(requests.get(course_url).content)
            for course_url in courses_list[:courses_count]]


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
                                filepath):
    xlsx_book = Workbook()
    sheet = xlsx_book.active
    for row in courses_rows:
        sheet.append(row)
    xlsx_book.save(filepath)
    return filepath


if __name__ == '__main__':
    coursera_url = 'https://www.coursera.org/sitemap~www~courses.xml'
    xlsx_filepath = 'output.xlsx'
    courses_list = get_courses_list_from_url(coursera_url)
    courses_info = get_courses_info(courses_list)
    courses_rows = get_courses_rows(courses_info)
    output_courses_info_to_xlsx(courses_rows, xlsx_filepath)
    print("Данные сохранены в {}".format(xlsx_filepath))
