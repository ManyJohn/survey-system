import csv, os, ast, abc, re


class LoadEnrollment():
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def read():
        pass
class CSVLoadEnrollment(LoadEnrollment):
    def read():
        enrolment_list=[]
        with open("requiredFiles_iteration2/enrolments.csv","r") as enrolment_file:
            csv_reader=csv.reader(enrolment_file)
            for row in csv_reader:
                #print (row)
                enrolment_list.append(row)
        return enrolment_list




class User:
    def __init__(self,uid=None,passcode=None,enroll_type=None):
        self.__id = uid
        self.__passcode=passcode
        self.__type=enroll_type
    @property
    def id(self):
        return self.__id 
    
    @property
    def passcode(self):
        return self.__passcode

    @property
    def enroll_type(self):
        return self.__enroll_type


class LoadUser:
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def read():
        pass

class CSVLoadUser(LoadUser):
    def read():
        user_list=[]
        with open("requiredFiles_iteration2/passwords.csv","r") as user_file:
            csv_reader=csv.reader(user_file)
            for row in csv_reader:
                #print (row)
                user_list.append(row)
        return user_list
class Question:
    # Passing in question_id is optional. No question_id is denoted by -1
    def __init__(self, question, choices, question_id=-1):
        # Question ID (int)
        self.__id = question_id
        # Question string
        self.__question = question 
        # List of option strings
        self.__choices = choices

    @property
    def id(self):
        return self.__id

    @property
    def question(self):
        return self.__question

    @property
    def choices(self):
        return self.__choices

class QuestionRW:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def read_all():
        pass

    @classmethod
    def read(cls, question_id):
        return [q for q in cls.read_all() if q.id == question_id][0]

    @classmethod
    def get_no_choices(cls, question_id):
        return len(cls.read(question_id).choices)

    @abc.abstractmethod
    def write(question):
        pass

class CSVQuestionRW(QuestionRW):
    def read_all():
        with open("question_pool.csv", "r") as pool_file:
            csv_reader = csv.reader(pool_file)
            question_list = [Question(q[1], q[2:], q[0]) for q in csv_reader]

        return question_list

    def write(question):
        # Get next question number from question pool 
        with open("question_pool.csv", "r") as pool_file:
            next_question_no = int(list(csv.reader(pool_file)).pop()[0]) + 1

        list_question = [next_question_no, question.question] + question.choices

        with open("question_pool.csv", "a") as pool_file:
            csv.writer(pool_file).writerow(list_question)
        return 0

class Survey:
    def __init__(self, course_offering, question_ids):
        # String representing course offering
        self.__course_offering = course_offering
        # List of question IDs in the survey
        self.__question_ids = question_ids

    @property
    def course_offering(self):
        return self.__course_offering

    @property
    def question_ids(self):
        return self.__question_ids

class SurveyRW:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def read_all():
        pass

    @classmethod
    def read(cls, s_name):
        return [s for s in cls.read_all() if s.course_offering == s_name][0]

    @abc.abstractmethod
    def write(survey):
        pass

class CSVSurveyRW(SurveyRW):
    def read_all():
        # List of Survey objects, look at the class for details
        survey_list = []
        # Filter all .csv file names in surveys directory
        survey_files = [f for f in os.listdir("surveys") if 
                re.search("(.)+\.csv", f) is not None]
        # Extract data from each survey file
        for s in survey_files:
            # List of Question IDs for this particular survey
            question_ids = []
            with open("surveys/" + s, "r") as s_file:
                reader = csv.reader(s_file)
                # Question ID is the first element of each row, append this
                #   to our question_ids list
                for q in reader:
                    question_ids.append(q[0])
            # Course offering is the survey CSV file name, <course>.csv
            course_offering = s[:-4]
            # Instantiate Survey object and append to survey_list
            survey_list.append(Survey(course_offering, question_ids))
        return survey_list

    def write(survey):
        survey_file_name = "surveys/" + survey.course_offering + ".csv"
        # Prevent attempts to overwrite existing surveys
        if os.path.exists(survey_file_name):
            return 1

        # Produce list of rows to be written to file, each row starts with
        #   a question ID (of a question in the survey), followed by a 0 for
        #   each choice of answer
        # TODO Use dependency injection to get QuestionRW class rather than
        #   hardcoding CSVQuestionRW
        survey_file_data = [[q_id] + [0]*CSVQuestionRW.get_no_choices(q_id) 
                for q_id in survey.question_ids]
        with open(survey_file_name, "w") as s_file:
            csv.writer(s_file).writerows(survey_file_data)

class SurveyResponse:
    def __init__(self, course_offering, results):
        # String representing course offering
        self.__course_offering = course_offering
        # Dictionary with question IDs as keys and the index of the choice 
        #   selected as values
        self.__results = results

    @property
    def course_offering(self):
        return self.__course_offering

    @property
    def results(self):
        return self.__results

class SurveyResponseRW:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def write():
        pass

class CSVSurveyResponseRW(SurveyResponseRW):
    def write(s_response):
        s_filename = "surveys/" + s_response.course_offering + ".csv"
        with open(s_filename, "r") as s_file:
            s_data = list(csv.reader(s_file))
        # Add all results from response object to CSV list s_data
        for question_id, answer in s_response.results.items():
            question_id = int(question_id)
            answer = int(answer)
            # Get reference to relevant row in CSV list
            question_row = [row for row in s_data if int(row[0]) == question_id][0]
            # Increment the choice count for the chosen answer in the row
            question_row[1 + answer] = int(question_row[1 + answer]) + 1
        # Now that the relevant rows in s_data is updated, write to file
        # Note that the file is overwritten since all the file data was 
        #   already taken in to s_data
        with open(s_filename, "w") as s_file:
            csv.writer(s_file).writerows(s_data)

class CourseOfferingsRW:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def read():
        pass

    @classmethod
    def read_unsurveyed(cls):
        all_courses = cls.read()
        surveys = CSVSurveyRW.read_all();
        surveyed_courses = [s.course_offering for s in surveys]
        unsurveyed_courses = \
            [item for item in all_courses if item not in surveyed_courses]
        return unsurveyed_courses

class CSVCourseOfferingsRW(CourseOfferingsRW):
    def read():
        # Read from CSV file which has 1 course offering per line
        with open("courses.csv", "r") as courses_file:
            content = courses_file.readlines()
            # Remove first and last lines and strip new lines
            course_offering_list = [x.strip() for x in content[1:-1]]

        return course_offering_list

class CSVCourseOfferingsRW_V2(CourseOfferingsRW):
    def read():
        file_name = "requiredFiles_iteration2/courses.csv"
        if not os.path.exists(file_name):
            return None
        course_offering_list=[]
        with open("requiredFiles_iteration2/courses.csv", "r") as courses_file:
            content = csv.reader(courses_file)
            for row in content:
                course_offering_list.append(row)

        return course_offering_list

