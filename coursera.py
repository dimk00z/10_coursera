import requests
from lxml import etree
from bs4 import BeautifulSoup
from openpyxl import Workbook


def get_courses_list_from_url(url):
    courses_tree = etree.fromstring(requests.get(url).content)
    courses_list = []
    for cours in courses_tree:
        courses_list.append(cours.getchildren()[0].text)
    return courses_list


def get_course_info(course_url):
    course_html = requests.get(course_url).content
    soup = BeautifulSoup(course_html, 'html.parser')
    title = soup.find('div', {'class': 'title'}).text
    language_info = soup.find('div', {'class': 'language-info'}).text
    startdate = soup.find('div', {'class': 'startdate'}).text
    weeks = soup.find('div', {'class': 'rc-WeekView'})
    if weeks:
        weeks = len(weeks)
    ratings = soup.find('div', {'class': 'ratings-text'})
    if ratings:
        ratings = ratings.text
    return title, language_info, startdate, weeks, ratings


def output_courses_info_to_xlsx(courses_info,
                                filepath='output.xlsx',
                                courses_count=20):
    xlsx_book = Workbook()
    sheet = xlsx_book.active
    sheet['A1'] = 'Course name'
    sheet['B1'] = 'Language'
    sheet['C1'] = 'Start date'
    sheet['D1'] = 'Number of weeks'
    sheet['E1'] = 'Rating'
    for course_number, course in enumerate(courses_list[:courses_count]):
        course_info = get_course_info(course)
        string_number = str(course_number + 2)
        sheet['A' + string_number] = course_info[0]
        sheet['B' + string_number] = course_info[1]
        sheet['C' + string_number] = course_info[2]
        if course_info[3]:
            sheet['D' + string_number] = course_info[3]
        if course_info[4]:
            sheet['E' + string_number] = course_info[4]
    xlsx_book.save(filepath)


if __name__ == '__main__':
    url = 'https://www.coursera.org/sitemap~www~courses.xml'
    courses_list = get_courses_list_from_url(url)
    output_courses_info_to_xlsx(courses_list)
