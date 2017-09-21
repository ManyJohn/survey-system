import sqlite3
import os
from survey_system import CourseOfferingsRW ,CSVCourseOfferingsRW_V2,LoadUser,CSVLoadUser
from survey_system import LoadEnrollment,CSVLoadEnrollment
class  DBcontroller(object):
	"""docstring for  controller"""
	def __init__(self):
		pass
	def add_user_from_csv(self):
		model=DBModel()
		user_list=CSVLoadUser.read()
		for detail in user_list:
			model.insert_user_record(uid=detail[0],passcode=detail[1],user_type=detail[2])

	def add_courses_from_csv(self):
		model=DBModel()
		courses_list=CSVCourseOfferingsRW_V2.read()
		for detail in courses_list:
			model.insert_course_record(courses_type=detail[0][0:4],courses_no=detail[0][4:],\
				courses_year=detail[1][0:2],courses_sem=detail[1][2:])

	def add_enrollment_from_csv(self):
		model=DBModel()
		enrolment=CSVLoadEnrollment.read()
		for detail in enrolment:
			#print(enrolment)
			row=model.search_course_by_full_detail(courses_type=detail[1][0:4],courses_no=detail[1][4:],\
				courses_year=detail[2][0:2],courses_sem=detail[2][2:])
			model.insert_enrolment(zid=detail[0],course_id=row[0][0])
			print(row[0][0])


class DBModel(object):
	"""docstring for DBModel"""
	def insert_enrolment(self,zid,course_id):
		command="INSERT OR IGNORE INTO  RELATION(ZID,COURSE_ID) VALUES ({},{}) "\
		.format(zid,course_id)
		self._insert(command)


	def insert_course_record(self,courses_type,courses_no,courses_year,courses_sem):
		command=\
		"INSERT INTO COURSES(COURSE_TYPE,COURSE_NO,COURSE_YEAR,COURSE_SEM) VALUES ('{}',{},{},'{}')".\
		format(courses_type,courses_no,courses_year,courses_sem)
		self._insert(command)

	def search_course_by_full_detail(self,courses_type,courses_no,courses_year,courses_sem):
		command=\
		"SELECT ROWID FROM COURSES WHERE COURSE_TYPE='{}' AND COURSE_NO={} AND COURSE_YEAR={} AND COURSE_SEM='{}'".\
		format(courses_type,courses_no,courses_year,courses_sem)
		row=self._search(command)
		return row

	def insert_user_record(self,uid,passcode,user_type):
		command="INSERT INTO USERS(ID,PASSCODE,USER_TYPE) VALUES ({},'{}','{}')"\
		.format(uid,passcode,user_type)
		self._insert(command)
	def _insert(self, command):
		 connection = sqlite3.connect('survey_system.db')
		 cursorObj = connection.cursor()
		 results=cursorObj.execute(command)
		 connection.commit()
		 connection.close()
		 #cursorObj.close()
		 return results

	def _search(self, command):
		 connection = sqlite3.connect('survey_system.db')
		 cursorObj = connection.cursor()
		 
		 results=cursorObj.execute(command)
		 connection.commit()
		 
		 result_list=[]
		 for row in results:
		 	result_list.append(row)
		 #cursorObj.close()
		 connection.close()
		 return result_list

class DBView(object):
	pass


new=DBcontroller()
new.add_enrollment_from_csv()