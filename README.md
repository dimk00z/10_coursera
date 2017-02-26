# Coursera Dump

Скрипт считывает xml <https://www.coursera.org/sitemap~www~courses.xml>.
И парсит первые 20 курсов, данные о курсах сохраняет в файл

Для работы необходимо установить модули из **requirements.txt**
под администратором/рутом выполнить: `pip install -r requirements.txt` 

Для скрипта доступен параметр имени выходного файла:`-o <file_name>` или `--output <file_name>`.

Если не задавать выходной файл, данные будут сохранены в `output.xlsx`

Пример запуска в консоли:
```
$ python coursera.py -o courseradump.xlsx
The data saved as courseradump.xlsx

```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
