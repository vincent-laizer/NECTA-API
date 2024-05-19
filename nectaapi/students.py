'''
A list of all students with their performance in a particular school or center
returns a dictionary
school_name, school_number, number_of_students, year_of_exam, exam_type, students[
    {
        examination_number,
        gender,
        division,
        points,
        subjects:{
            subject1:score1,
            subject2:score2,
            ...
        }
    }
    ...
]
'''

import requests
from bs4 import BeautifulSoup
from nectaapi import summary
from typing import Dict,Any,List

def students(year:int, exam_type:str, school_number:str)->Dict[str,Any]:
    """Get all students with their performance in a particular school or center

    Args:
        year(int),exam_type(str), school_number(str)
    
    Returns:
        Dict
    """
    url = ""
    exam_type = exam_type.lower()
    school_number = school_number.lower()
    year = int(year)
    index = 0

    if exam_type == "acsee":
        if year == 2023:
            url = f"https://matokeo.necta.go.tz/results/2023/acsee/results/{school_number}.htm"
        else:
            url = f"https://onlinesys.necta.go.tz/results/{year}/acsee/results/{school_number}.htm" 
        
        if school_number.startswith("p"):
            if year >= 2019:
                index = 2
            else:
                index = 0
        else:
            if year >= 2019:
                index = 2
            else:
                index = 0

    elif exam_type == "csee":
        if int(year) == 2023:
            url = f"https://matokeo.necta.go.tz/results/2023/csee/CSEE2023/results/{school_number}.htm"
        elif int(year) > 2018:
            url = f"https://onlinesys.necta.go.tz/results/{year}/csee/results/{school_number}.htm"
        elif int(year) > 2014:
            url = f"https://onlinesys.necta.go.tz/results/{year}/csee/results/{school_number}.htm" 
            # http://127.0.0.1/necta/{year}/csee/s3881.php
        else:
            url = f"https://onlinesys.necta.go.tz/results/{year}/csee/{school_number}.htm" 
            # http://127.0.0.1/necta/{year}/csee/s3881.php

        if school_number.startswith("p"):
            if year > 2018:
                index = 2
            else:
                index = 0
        else:
            if year > 2018:
                index = 2
            else:
                index = 0
    
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')

    if data.status_code != 200:
        raise Exception(f"failed to connect to server\nError code {data.status_code}")
    else:
        # get some data from summary function
        school_summary = summary.summary(year, exam_type, school_number)

        students = {
            "school_number":school_number,
            "school_name":school_summary["school_name"],
            "year_of_exam":year,
            "exam_type":exam_type,
            "number_of_students":school_summary["number_of_students"],
            "students":[]
        }

        student_data = scrapStudents(soup, index)
        students["students"] = student_data

        return students

def scrapStudents(soup, index)->List[Dict[str,Any]]:
    studentsTable = soup.find_all("table")[index]
    data = []

    # [1:] -> eliminate the first row containing titles
    for tr in studentsTable.find_all("tr")[1:]:
        # row[reg_no, sex, points, division, subjects]
        row = []
        for td in tr.find_all("td"):
            row.append(td.text.strip('\n'))

        subjects = splitAfter(row[4])
        student = {
            "examination_number":row[0],
            "gender":row[1],
            "division":row[3],
            "points":row[2],
            "subjects":subjects
        }

        # print(student, end='\n')
        data.append(student)

    return data

# assisting function in obtaining a dictionary of candidates subjects and grades
def splitAfter(text)->Dict[str,str]:
    subjects = {} # a dictionary of subject grade pair
    values = []
    temp = ""
    for i in range(0, len(text)-1):
        temp += text[i]
        if text[i] == '\'' and text[i+1] == ' ':
            values.append(temp)
            temp = ""

    for v in values:
        q = v.split('-')
        subject = q[0].strip()
        grade = q[1].strip().strip('\'')
        subjects.update({subject: grade})

    return subjects