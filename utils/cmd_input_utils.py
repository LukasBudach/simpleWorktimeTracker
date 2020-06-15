from datastructures import Time

from datetime import date
import re


def is_last_char_space(in_str: str):
    return in_str[len(in_str) - 1] == ' '


def make_last_char_space(in_str: str):
    return in_str if is_last_char_space(in_str) else in_str + ' '


def format_binary_question(question: str):
    if 'y/n' not in question.lower():
        question = make_last_char_space(question)
        question += '(y/n)'
    return make_last_char_space(question)


def binary_question_input(question: str):
    input_invalid = True
    response = ''
    while input_invalid:
        response = input(format_binary_question(question)).lower()
        input_invalid = response not in ['y', 'n']
        if input_invalid:
            print('The input was invalid, please use only one of the characters "y, n, Y, N" as response to the '
                  'question.')
    return response == 'y'


def format_time_input(request: str):
    if 'hh:mm' not in request.lower():
        request = make_last_char_space(request)
        request += '(hh:mm)'
    return make_last_char_space(request)


def time_input(request: str):
    input_invalid = True
    response = ''
    valid_time_regex = re.compile('-?[0-9]{1,2}:[0-9]{2}')
    while input_invalid:
        response = input(format_time_input(request))
        input_invalid = not valid_time_regex.match(response)
        if input_invalid:
            print('The input was invalid, please enter the time in the format hh:mm (h = hour, m = minute).')
    return Time.from_string(response)


def format_date_input(request: str):
    if 'dd.mm.yyyy' not in request.lower():
        request = make_last_char_space(request)
        request += '(dd.mm.yyyy)'
    return make_last_char_space(request)


def date_input(request: str, empty_for_today=False):
    input_invalid = True
    response = ''
    valid_date_regex = re.compile('[0-3][0-9].[0-1][0-9].[0-9]{4}')
    while input_invalid:
        response = input(format_date_input(request))
        input_invalid = not valid_date_regex.match(response)
        if empty_for_today and response == '':
            break
        if input_invalid:
            print('The input was invalid, please enter the date in the format dd.mm.yyyy (d = hour, m = month, '
                  'y = year).')
    return date.today() if response == '' else date(int(response[-4:]), int(response[3:5]), int(response[:2]))
