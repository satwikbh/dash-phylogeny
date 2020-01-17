from random import randint

from pycountry import countries


def min_max_date(df):
    min_date = df['year'].min()
    max_date = df['year'].max()
    if min_date > max_date:
        tmp = min_date
        min_date = max_date
        max_date = tmp
    return min_date, max_date


def slicer(min_date, max_date):
    step = 1
    if 5 < max_date - min_date <= 10:
        step = 2
    elif 10 < max_date - min_date <= 50:
        step = 5
    elif max_date - min_date > 50:
        step = 10
    marks_data = {}
    for i in range(int(min_date), int(max_date) + 1, step):
        if i > int(max_date):
            marks_data[i] = str(int(max_date))
        else:
            marks_data[i] = str(i)

    if i < int(max_date):
        marks_data[int(max_date)] = str(max_date)

    return marks_data


def get_color():
    r, g, b = randint(0, 256), randint(0, 256), randint(0, 256)
    s = str("rgb") + "(" + str(r) + "," + str(g) + "," + str(b) + ")"
    return s


def get_countries(non_occurring_countries):
    countries_list = list()
    for country in countries:
        countries_list.append(country.name)
    if len(non_occurring_countries) != 0:
        countries_list += non_occurring_countries
    country_color_dict = {country: get_color() for country in countries_list}
    return country_color_dict
