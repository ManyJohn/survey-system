import csv, os, ast, abc, re

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

class QuestionReader:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def read():
        pass

class CSVQuestionReader(QuestionReader):
    def read():
        question_list = []
        with open("question_pool.csv", "r") as pool_file:
            csv_reader = csv.reader(pool_file)

            for q in csv_reader:
                question_list.append(Question(q[1], q[2:], q[0]))
        return question_list
        
class QuestionWriter:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def write():
        pass

class CSVQuestionWriter(QuestionWriter):
    def write(question):
        # Get next question number from question pool 
        with open("question_pool.csv", "r") as pool_file:
            next_question_no = list(csv.reader(pool_file)).pop()[0]

        list_question = [next_question_no, question.question] + question.choices

        with open("question_pool.csv", "a") as pool_file:
            csv.writer(pool_file).writerow(list_question)

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

class SurveyReader:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def read():
        pass

class CSVSurveyReader(SurveyReader):
    def read():
        # List of Survey objects, look at the class for details
        survey_list = []
        # Filter all .csv file names in surveys directory
        survey_files = list(filter(lambda x: re.search("(.)+\.csv", x) is not 
            None, os.listdir("surveys")))
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


class SurveyWriter:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def write():
        pass

class CSVSurveyWriter(SurveyWriter):
    def write(survey):
        pass

class CourseOfferingReader:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def read():
        pass

    @classmethod
    def read_unsurveyed(cls):
        all_courses = cls.read()
        surveys = DirectorySurveyReader.read();
        surveyed_courses = [s.course_offering for s in surveys]
        unsurveyed_courses = \
            [item for item in all_courses if item not in surveyed_courses]
        return unsurveyed_courses

class CSVCourseOfferingReader(CourseOfferingReader):
    def read():
        # Read from CSV file which has 1 course offering per line
        with open("courses.csv", "r") as courses_file:
            content = courses_file.readlines()
            # Remove first and last lines and strip new lines
            course_offering_list = [x.strip() for x in content[1:-1]]

        return course_offering_list
