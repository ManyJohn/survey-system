import csv, os, ast, abc, re

class Question:
    # Passing in question_id is optional. No question_id is denoted by -1
    def __init__(self, question, choices, question_id=-1):
        # Question ID (int)
        self.__question_id = question_id
        # Question string
        self.__question = question 
        # List of option strings
        self.__choices = choices

    @property
    def question_id(self):
        return self.__question_id

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

class DirectorySurveyReader(SurveyReader):
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

        
class Course:
    """docstring for Course"""
    @classmethod       
    def output_course(self):
        course_list=[]
        with open('courses.csv','r') as csv_in:
            reader = csv.reader(csv_in)
            i=0
           
            for row in reader:
               
                #name=row
                if (i==0):
                    i=i+1
                    continue
                if (len(row)==0):
                    continue

                name=row[0]
                #if str.isspace(name):
                #    continue
                course_list.append(name)

        return course_list


"""

class Survey:
    def __init__(self,file_name,question_list):
        self.file_name=file_name
        self.question_list=question_list

    def make_survey(self):
        survey_dir="./survey/"
        if not os.path.exists(survey_dir):
            os.makedirs(survey_dir)
        #question_file=open("question_pool.csv","r")
        with open('question_pool.csv','r') as csv_in:
            question_reader = csv.reader(csv_in,quoting=csv.QUOTE_ALL)
            question_reader =list(question_reader)
        with open(survey_dir+self.file_name+".csv",'a') as csv_out:
            writer = csv.writer(csv_out)
            for question_id in self.question_list:
                #options_of_each_question=ast.literal_eval(question_reader[int(question_id)][2])
                #print(options_of_each_question[0])
                print(question_id,"+id=============")
                num_of_options=len(question_reader[int(question_id)][2:])
                writer.writerow([question_id]+['0']*num_of_options) 
                
#question=input("what is the question?")
#option=str.split(input("enter option, and sperate them in comma"),',')
#print(option[0])
#take_in_qustion(question,option)



#make_survey(file_name="name",question_list=[0])
"""
