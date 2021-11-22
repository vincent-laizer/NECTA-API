# Necta-API
Get a formated data of examination results scrapped from necta results website.

Note this is not an official [NECTA](https://necta.go.tz/) API and is still in development

Current version is `Beta 1.0.0`

Developed by [**Tanzania Programmers**](http://tanzaniaprogrammers.com/), written *by Vincent Laizer.*
---

---

## Usage
- [x] Get the package via pip

``` python
    pip install nectaapi 
```

- [x] Get a list of all schools in a given year and exam type.

exam type can be **acsee** or **csee** (for now, more to be added)
  
```python
    from nectaapi import scrapper as sc

    data = sc.schools(2017, 'csee') 
```
  the function returns a dictionary in the form

  ```python
  {
      "exam_type": "examamination type",
      "year_of_exam": "year of examination",
      "number_of_schools": "number of schools in this exam and year",
      "description": "description of this particular result",
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
    from nectaapi import scrapper as sc

    sammury = sc.schoolSummary(year, examType, schoolNumber)

    # schoolNumber is the schools registration number ie s3881 or s1268
  ```

  this function is still buggy due to the varying nature of results publishing structure in necta website across the years

  - [x] Get a single students results
  ```python
    from nectaapi import scrapper as sc

    results = sc.student(year, examType, schoolNumber, studentNumber)

    # student number is the students part of their examination number eg 0040 or 0553
  ```

  The 'student' function returns a dictionary of this form
  ```python
    {
        "number": "students examination number",
        "division": "students division",
        "points": "students points",
        "subjects": {
            "subject name 1": "its grade",
            "subject name 2": "its grade",
            ...
        }
    }
  ```

  check out video tutorial on [YouTube](https://www.youtube.com/channel/UCuMUw-djxHqOHrvnnFGYtZA) for demos.

---

### contributions are awaited for
**GitHub repo [nectaapi](https://github.com/vincent-laizer/NECTA-API)**

