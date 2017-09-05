import csv, os, ast, abc


class Question:
    def __init__(self, question, choices):
        # Question string
        self.__question = question 
        # List of option strings
        self.__choices = choices

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

class QuestionReaderCSV(QuestionReader):
    def read():
        question_list = []
        with open("question_pool.csv", "r") as pool_file:
            csv_reader = csv.reader(pool_file)

            for question in csv_reader:
                question_list.append(Question(question[1], question[2:]))
        return question_list
        
class QuestionWriter:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def write():
        pass

class QuestionWriterCSV(QuestionWriter):
    def write(question):
        # Get next question number from question pool 
        with open("question_pool.csv", "r") as pool_file:
            next_question_no = list(csv.reader(pool_file)).pop()[0]

        list_question = [next_question_no, question.question] + question.choices

        with open("question_pool.csv", "a") as pool_file:
            csv.writer(pool_file).writerow(list_question)

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

