'''
Results of a single student
returns a dictionary
{
    examination_number, year_of_exam, exam_type, school_name, gender,
    division, points, subjects:
            {
                subject1:score1,
                subject2:score2,
                ...
            }
}
'''

import requests
from bs4 import BeautifulSoup
from nectaapi import summary
from nectaapi.students import splitAfter
from typing import Dict,Any
from nectaapi.student_name import student_names

def student(year:int, exam_type:str, school_number:str, student_number:int)->Dict[str,Any]:
    """Results of a single student

    Args:
        year(int), exam_type(str), school_number(str), student_number(int)
    
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
            if year > 2019:
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
        elif int(year) == 2021:
            url = f"https://onlinesys.necta.go.tz/results/2021/csee/results/{school_number}.htm"
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
        s = summary.summary(year, exam_type, school_number)

        student_data = {
            "examination_number":f"{school_number.upper()}/{student_number}",
            "year_of_exam":year,
            "exam_type":exam_type,
            "gender":"*",
            "school_name":s["school_name"],
            "division":"*",
            "points":"*",
            "subjects":{}
        }

        found = False

        studentsTable = soup.find_all("table")[index]
        for tr in studentsTable.find_all("tr"):
            row = []
            for td in tr.find_all("td"):
                row.append(td.text.strip('\n'))

            # search for student number
            print(row)
            if row[0] == student_data["examination_number"]:
                student_data["gender"] = row[1]
                student_data["division"] = row[3]
                student_data["points"] = row[2]
                student_data["subjects"] = splitAfter(row[4])
                found = True

        if not found:
            raise Exception(f"Wrong Examination Number {student_data['examination_number']}")
        else:
            # get student names
            names = student_names(student_number, school_number, year, exam_type)
            if names != None:
                student_data["firstname"] = names["firstname"]
                student_data["middlename"] = names["middlename"]
                student_data["lastname"] = names["lastname"]
                student_data["sex"] = names["sex"]
                
            return student_data