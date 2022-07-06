'''
Comparison of different schools' performance across years
takes parameters exam_type and a list of school numbers.
returns a dictionary of comparable data btn the school(s) in the given years range.
comparable data => gpa, national_position, no_of_students, division_count(not neccessary)
'''

from nectaapi import summary, schools
import datetime

def comparision(start_year, end_year, exam_type, school_list):
    data = {}

    for i in range(start_year, end_year+1):
        data[str(i)] = {}
        for sch in school_list:
            if schoolPresent(i, exam_type, sch):
                s = summary.summary(i, exam_type, sch)
                data[str(i)][sch] = {
                    "national_position":s["national_position"],
                    "number_of_students":s["number_of_students"],
                    "gpa":s["gpa"]
                }
            else:
                # school not present in this year
                data[str(i)][sch] = {
                    "national_position":"*",
                    "number_of_students":"*",
                    "gpa":"*"
                }
    return data

# function to check if a school participated in a national exam
def schoolPresent(year, exam_type, school_number):
    all = schools.schools(year, exam_type)["schools"]
    for s in all:
        if school_number.lower() == s["school_number"].lower():
            # print(year, s["school_number"].lower(), sep=" -> ")
            return True
    return False