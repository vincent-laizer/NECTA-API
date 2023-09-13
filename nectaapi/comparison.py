'''
Comparison of different schools' performance across years
takes parameters exam_type and a list of school numbers.
returns a dictionary of comparable data btn the school(s) in the given years range.
comparable data => gpa, national_position, no_of_students, division_count(not neccessary)
'''

from nectaapi import summary, schools
from typing import List,Union,Dict
import datetime

def comparison(start_year:int, end_year:int, exam_type:str, school_list:List[str])->Dict[str,Union[str,None]]:
    """Comparison of different schools' performance across years

    Args:
        start_year: int, end_year: int, exam_type:str and a list of school numbers

    Returns
        Dict[str, Union[str,None]]

    a dictionary of comparable data btn the school(s) in the given years range.
    comparable data => gpa, national_position, no_of_students, division_count(not neccessary)
    """
    data = {}

    for year in range(start_year, end_year+1):
        data[str(year)] = {}
        for school in school_list:
            if schoolPresent(year, exam_type, school):
                school_data = summary.summary(year, exam_type, school)
                data[str(year)][school] = {
                    "national_position":school_data["national_position"],
                    "number_of_students":school_data["number_of_students"],
                    "gpa":school_data["gpa"]
                }
            else:
                # school not present in this year,the data returned will be None
                data[str(year)][school] = {
                    "national_position":None,
                    "number_of_students":None,
                    "gpa":None
                }
    return data

# function to check if a school participated in a national exam
def schoolPresent(year:int, exam_type:str, school_number:str)->bool:
    """check if a school participated in a national exam

    Args: 
        year(int), exam_type(str), school_number(str)
    
    Returns
        Boolean : True if participated otherwise False
    """

    all_schools = schools.schools(year, exam_type)["schools"]
    for school in all_schools:
        if school_number.lower() == school["school_number"].lower():
            return True
    return False