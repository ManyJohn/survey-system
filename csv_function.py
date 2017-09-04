import csv
import os
import ast


class Question:
    def __init__(self,question,option):
        self.question = question
        self.option = option
    #@classmethod
    def take_in_qustion(self):
        with open('question_pool.csv','a') as csv_out:
                with open('question_pool.csv','r') as csv_in:
                    reader = csv.reader(csv_in)
                    i=len(list(reader))
                    print(i)
                    content=[]
                    content.append(i)
                    content.append(self.question)
                    option=str.split(self.option,',')
                    for each_op in option:
                        content.append(each_op)

                writer = csv.writer(csv_out,quoting=csv.QUOTE_ALL)
                writer.writerow(content) 
    @classmethod            
    def output_qurstion(cls):
         with open('question_pool.csv','a') as csv_out:
          question_list=[]
          with open('question_pool.csv','r') as csv_in:
            reader = csv.reader(csv_in)
            for row in reader:
               question_list.append(row)
            return question_list

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

