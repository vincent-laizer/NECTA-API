'''
return student names from heslb api, return None if student is not found
works for csee only

return format:
type: dictionary
example: {
	"firstname":"",
	"middlename":"",
	"lastname":"",
	"sex":""
}
'''

import requests
import json

def student_names(student_number, school_number, year, exam_type):
	if exam_type == "csee":
		headersList = {
			"Content-Type": "application/json"
		}

		try:
			url = "https://olas.heslb.go.tz/appli/api/application/search-applicant/"
			payload = json.dumps({
				"index_no": f"{school_number}-{student_number}",
				"app_year": "",
				"exam_year": f"{year}",
				"applicant_type": "necta"
			})
			
			response = requests.request("POST", url, data=payload,  headers=headersList, verify=False)
			details = response.json().get("data").get("applicant")
			return {
				"firstname": details.get("first_name"),
				"middlename": details.get("middle_name"),
				"lastname": details.get("last_name"),
				"sex": details.get("sex")
			}
		except Exception as e:
			print(e)
			return None
	else:
		return None
