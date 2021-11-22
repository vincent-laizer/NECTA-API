from bs4 import BeautifulSoup
import requests

# return a list of all schools in a given year and exam type
def schools(year, examType):
    url = ""
    if examType.lower() == "csee":
        url = f"https://onlinesys.necta.go.tz/results/{year}/csee/csee.htm"
    elif examType.lower() == "acsee":
        url = f"https://onlinesys.necta.go.tz/results/{year}/acsee/index.htm"
    else:
        url = f"https://onlinesys.necta.go.tz/results/{year}/csee/csee.htm"

    schools = {}

    data = requests.get(url)
    if data.status_code == 200:
        soup = BeautifulSoup(data.text, 'html.parser')

        # a list of dictionaries to hold school's registration number and name
        schools = []

        # get all the data present in the tables i.e list of schools and centers
        for font in soup.find_all('font'):
            for a in font.find_all('a'):
                clean = a.text.strip('\n')
                school = clean.split(' ')

                school_name = ""
                for s in school[1:]:
                    school_name = f"{school_name} {s}"

                schools.append({"school_name": school_name, "registration_number":school[0]})

        # eliminate initial dirt, the first letters that were extracted as school names
        schools = schools[27:]
        schools.insert(0, {"year": year, "level":examType})

        schools_data = {
            "exam_type": examType,
            "year_of_exam": year,
            "number_of_schools": len(schools),
            "description": f"a list of all schools and centers that participated in {examType} in {year}",
            "schools": schools            
        }

        # return a dictionary of all schools and more info
        return schools_data
    else:
        # upon error return raise an exception
        raise Exception(f"failed to access {url}.\n Error code: {data.status_code}")


###############################################################################################################

# summary of school results in a given year and exam type
def schoolSummary(year, examType, schoolNumber):
    url = f"https://onlinesys.necta.go.tz/results/{year}/{examType}/results/{schoolNumber}.htm"

    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')
    
    if data.status_code != 200:
        raise Exception("failed to connect to server")
    else:
        summary = {}
        '''
        a dictionary containing divisions based on gender i.e
        {"I": {"F":20, "M":24, "T":44}, "II":{"F":20, "M":24, "T":44}, ...} for all divisions present
        '''
        rows = []

        tables = soup.find_all('table')
        for tr in tables[0].find_all('tr'):
            r = []
            for td in tr.find_all('td'):
                r.append(td.text.strip('\n'))
            rows.append(r)

        for i in range(1, 6):
            div = {
                rows[0][i]:{
                    "F": rows[1][i],
                    "M": rows[2][i],
                    "T": rows[3][i],
                    }
                }
            summary.update(div)
        return summary

###############################################################################################################

# assisting function in obtaining a dictionary of candidates subjects and grades
def splitAfter(text):
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


###############################################################################################################


def student(year, examType, schoolNumber, studentNumber):
    url = f"https://onlinesys.necta.go.tz/results/{year}/{examType}/results/{schoolNumber}.htm"

    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')
    
    rows = []

    if data.status_code != 200:
        raise Exception("failed to connect to server")
    else:
        # table position has changed in varoius year
        '''
            the year difference is different for acsee and csee, put that in consideration
        '''
        index = 0
        if int(year) < 2019:
            index = 0
        elif int(year) == 2019 and examType == "acsee":
            index = 0
        else:
            index = 2

        studentsTable = soup.find_all("table")
        for t in studentsTable[index].find_all("tr"):
            row = []
            for d in t.find_all("td"):
                row.append(d.text.strip('\n'))
            rows.append(row)

        completeNumber = f"{schoolNumber.upper()}/{studentNumber}"
        studentDetails = {}

        # varable to check whether the given reg no is present or not
        found = False

        # loop through every row and search for students examination number
        for r in rows:
            if r[0] == completeNumber:
                subjects = r[4:]
                studentDetails["number"] = completeNumber
                studentDetails["division"] = r[3]
                studentDetails["points"] = r[2]
                studentDetails["subjects"] = splitAfter(subjects[0])
                
                found = True

        if not found:
            raise Exception(f"Wrong Examination Number {completeNumber}")
        else:
            return studentDetails