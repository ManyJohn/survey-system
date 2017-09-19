import sqlite3
import os
from survey_system import CourseOfferingsRW ,CSVCourseOfferingsRW_V2
class  DBcontroller(object):
	"""docstring for  controller"""
	def __init__(self):
		pass
	def add_Courses_from_csv(self):
		model=DBModel()
		courses_list=CSVCourseOfferingsRW_V2.read()

		for detail in courses_list:
			model.insert_record(courses_type=detail[0][0:4],courses_no=detail[0][4:],courses_year=detail[1][0:2],courses_sem=detail[1][2:])


class DBModel(object):
	"""docstring for DBModel"""
	def insert_record(self,courses_type,courses_no,courses_year,courses_sem):
		command="INSERT INTO COURSES(COURSE_TYPE,COURSE_NO,COURSE_YEAR,COURSE_SEM) VALUES ('{}',{},{},'{}')".format(courses_type,courses_no,courses_year,courses_sem)
		self._insert(command)



		
	def _insert(self, command):
		 connection = sqlite3.connect('survey_system.db')
		 cursorObj = connection.cursor()
		 results=cursorObj.execute(command)
		 connection.commit()
		 cursorObj.close()
		 return results

class DBView(object):
	pass


new=DBcontroller()
new.add_Courses_from_csv()