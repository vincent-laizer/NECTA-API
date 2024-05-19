# Necta-API

Get a formated data of examination results scrapped from necta results website.

Note this is not an official [NECTA](https://necta.go.tz/) API and is still in development

Current version is `Beta 2.0.6`

This Version comes with a more modular structure compared to the previsious ones 

Developed by [**Tanzania Programmers**](https://tanzaniaprogrammers.com/), written *by Vincent Laizer.*

---

---

## Usage

- [x] Get the package via pip

    ```bash
        pip install nectaapi 
    ```

    - In any return value **None** indicates that no data could be scrapped

- [x] Get a list of all schools in a given year and exam type.

    exam type can be **acsee** or **csee** (for now, more to be added)

    ```python
        from nectaapi import schools

        data = schools.schools(2017, 'csee') 
    ```

    The function returns a dictionary in the form

    ```python
    {
        "exam_type": "examamination type",
        "year_of_exam": "year of examination",
        "number_of_schools": "number of schools in this exam and year",
        "schools": [
            {
                "school_name": "school name 1",
                "registration_number":"registration number 1"
            },
            {
                "school_name": "school name 2",
                "registration_number":"registration number 2"
            },
            ...]
    }
    ```

- [x] Get a highlight of school overal results

  ```python
    from nectaapi import summary

    data = summary.summary(year, examType, schoolNumber)

    # schoolNumber is the schools registration number ie s3881 or s1268
  ```

  The function returns a dictionary in the form
  
  ```python
    {
        "school_name": "name of school",
        "school_number": "school_number",
        "exam_type": "exam_type",
        "year_of_exam": "year",
        "school_category":"category based on number of students",
        "number_of_students": "total number of students",
        "school_region":"regional location of the school",
        "male_students": "number of male students",
        "female_students": "number of female students",
        "absentees": "number of students who missed the exam",
        "division_one": "number of division one",
        "division_two": "number of division two",
        "division_three": "number of division three",
        "division_four": "number of division four",
        "division_zero":"number of division zero",
        "national_position": "school's national position",
        "regional_position": "school's regional position",
        "total_national_schools":"number of schools national wise",
        "total_regional_schools":"number of schools regional wise",
        "gpa": "school's GPA"
    }
  ```

- [x] Get a single students results

  ```python
    from nectaapi import student

    results = student.student(year, examType, schoolNumber, studentNumber)

    # student number is the students part of their examination number eg 0040 or 0553
  ```

  The 'student' function returns a dictionary of this form
  
  ```python  
    {
    "examination_number":"students examination number",
    "year_of_exam":"year",
    "exam_type":"exam type",
    "school_name":"name of student's school",
    "gender":"student's gender",
    "division":"students division",
    "points":"grade points",
    "subjects":
            {
                "subject1":"score1",
                "subject2":"score2",
                ...
            }
    }
  ```

- [x] Compare schools performance over a range of years or of just a single school

    _not present in perivious versions_

    The parameters of the function are, the start year, end year of comparison, exam type and a list of schools to compare. start year is always less than end year, suppose they are equal a one year comparison is returned

    ```python
        from nectaapi import comparison
        data = comparison.comparison(startYear, endYear, examType,  ["school_number1", "school_number2", ...])
    ```

    It then returns a dictionary with school comparable data like, gpa, national_position and number_of_students in the form

    ```python
        {
            "year1":{
                "school_number1":{
                    "gpa":"",
                    "national_position":"",
                    "number_of_students":""
                },
                "school_number2":{
                    "gpa":"",
                    "national_position":"",
                    "number_of_students":""
                },
                ...
            },
            "year2":{
                "school_number1":{
                    "gpa":"",
                    "national_position":"",
                    "number_of_students":""
                },
                "school_number2":{
                    "gpa":"",
                    "national_position":"",
                    "number_of_students":""
                },
                ...
            }
            ...
        }
    ```

    As one of my teachers said, **"Academics is one of the 3 areas in life where competition is allowed"** *Mr. H. Masegense*, so don't mind comparing performance of schools over the years

    + Comparison module comes with a bonus function to check if a school participated in national examinations of a given type and year. Returns a boolean value

    ```python
        from nectaapi import comparison
        isPresent = comparison.schoolPresent(year, exam_type, school_number)
    ```

## What's New

## Version 2.0.6

- Compatibility with 2023 **CSEE** results format
- Compatibility with 2023 **ACSEE** results format
- Minor bug fixes

## Version 2.0.5

- Minor bug fixes

## Version 2.0.4

- Compatibility with 2022 **ACSEE** results format

## Version 2.0.3

- Compatibility with 2021 **CSEE** results format

## Version 2.0.0

- Bug fixes on the school summary function
- proper handling of the year 2015 where GPA system was used.
    - note, in this year, distinction is counted as division one, merit as division two, credit as division three, pass as division four and fail as division zero.
- school comparison function
- code modularity improvement

---

  check out video tutorial on [YouTube](https://www.youtube.com/channel/UCuMUw-djxHqOHrvnnFGYtZA) for demos.

---

### contributions are awaited for **GitHub repo [NECTA-API](https://github.com/vincent-laizer/NECTA-API)**
