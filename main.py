import sqlite3
from sqlite3 import Error
from tkinter import *
import smtplib
import imghdr
from email.message import EmailMessage
import tkinter.messagebox
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import speech_recognition as sr
import urllib3
import json



root = Tk()
root.geometry('300x200')
root.title('student-helper')
assignment = StringVar()
assignmarks=StringVar()
assignment_bystudent= StringVar()
marks = StringVar()
submitted = StringVar()
link= StringVar()
linkassign=StringVar()


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def create_task():
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    sql = ''' INSERT INTO tasks(Assignment,marks,submitted)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (assignment.get(),0,0))
    conn.commit()
    return cur.lastrowid


def update_task_student():
    """
    update priority, begin_date, and end date of a task
    :param conn:
    :param task:
    :return: project id
    """
    sql = ''' UPDATE tasks
              SET marks = ? ,
                  submitted = ?
              WHERE Assignment = ?'''
    sql_update_query = """Update tasks set submitted = ?,link=? where Assignment = ?"""
    data = (1,link.get(), assignment_bystudent.get())
    cur = conn.cursor()
    cur.execute(sql_update_query, data)
    conn.commit()
    

def update_task_teacher():
    """
    update priority, begin_date, and end date of a task
    :param conn:
    :param task:
    :return: project id
    """
    sql = ''' UPDATE tasks
              SET marks = ? ,
                  submitted = ?
              WHERE Assignment = ?'''
    sql_update_query = """Update tasks set marks = ? where Assignment = ?"""
    
    r_set=conn.execute('''SELECT * from tasks''');
    lis=[]
    boolean=False
    for student in r_set:
        lis.append((student[1]))
        lis.append(student)
        if(student[1]==assignmarks.get()):
            if(student[3]==1):
                boolean=True
                
    print(lis)
    if(assignmarks.get() not in lis):
        tkinter.messagebox.showinfo(" ","Assignment not found")
        
    else:
        
        if(boolean):
            
            if(int(marks.get())>100):
                tkinter.messagebox.showinfo(" ","marks should be less than or equal to 100")
            else:
                
                data = (marks.get(), assignmarks.get())
                cur = conn.cursor()
                cur.execute(sql_update_query, data)
                conn.commit()
                tkinter.messagebox.showinfo(" ","Marks successfully uploaded")
                
        else:
            tkinter.messagebox.showinfo(" ",assignmarks.get()+" not yet submitted")
        
                
            
    





database = r"C:\Users\pksds\Documents\dynamichack1221.db"
sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                    id integer PRIMARY KEY,
                                    Assignment text NOT NULL,
                                    marks integer,
                                    submitted integer,
                                    link text
                                );"""


conn = create_connection(database)



if conn is not None:
    create_table(conn, sql_create_tasks_table)
else:
    print("Error! cannot create the database connection.")
        
        

def getlink():
    boole=0
    r_set=conn.execute('''SELECT * from tasks''');
    lis=[]
    for student in r_set:
        if(assignmarks.get()==student[1]):
            print(student[4])
            
            tkinter.messagebox.showinfo(" ",student[4])
            boole=1
    if(boole==0):
        tkinter.messagebox.showinfo(" ","Assignment not found")
            
            
    print(lis)
    
    


    
def teacher():
    top = Toplevel(root)
    top.geometry('500x600')
    
    Button(top,text="Mail Results", font='Times 14 bold',bg='dark gray', command = mail,width=20).place(x= 130, y=20)
    Label(top, text = '-----------------------------------------------------------------', font='Times 15 bold').place(x= 20, y=80)
    Label(top, text = 'Assignment Name', font='Times 15 bold').place(x= 20, y=120)
    Entry(top, textvariable = assignment ,width=62).place(x= 20, y=160)
    
    
    Button(top, text = 'Upload', font='Times 15 bold',command = create_task).place(x= 20, y=180)
    Label(top, text = '-----------------------------------------------------------------', font='Times 15 bold').place(x= 20, y=220)
    Label(top, text = 'Assign Marks', font='Times 15 bold').place(x= 20, y=250)
    Label(top, text = 'Assignment Name', font='Times 15 bold').place(x= 20, y=290)
    Entry(top, textvariable = assignmarks ,width=45).place(x= 190, y=290)
    Button(top, text = 'Get link', font='Times 15 bold',command=getlink).place(x= 20, y=320)
    
    Label(top, text = 'Mark\'s obtained', font='Times 15 bold').place(x= 20, y=350)
    Entry(top, textvariable = marks ,width=32).place(x= 190, y=350)
    Button(top, text = 'Upload', font='Times 15 bold',command = update_task_teacher).place(x= 20, y=380)
    Label(top, text = '-----------------------------------------------------------------', font='Times 15 bold').place(x= 20, y=410)
    
    
    
    

def student():
    top = Toplevel(root)
    top.geometry('500x600')
    Label(top,text="OpenStudy", font='Times 14 bold',bg='dark gray',width=20).place(x= 130, y=20)
    Label(top, text = '-----------------------------------------------------------------', font='Times 15 bold').place(x= 20, y=80)
    Label(top, text = 'Assignment Name', font='Times 15 bold').place(x= 20, y=120)
    Entry(top, textvariable = assignment_bystudent ,width=62).place(x= 20, y=160)
    Label(top, text = 'link for the assignment', font='Times 15 bold').place(x= 20, y=200)
    Entry(top, textvariable = link ,width=62).place(x= 20, y=240)
    Button(top, text = 'submit', font='Times 15 bold',command = update_task_student).place(x= 20, y=280)
    Label(top, text = '-----------------------------------------------------------------', font='Times 15 bold').place(x= 20, y=320)
    Button(top, text = 'Complete notes', font='Times 15 bold',command = aud).place(x= 20, y=360)
    Button(top, text = 'Summarize video lecture', font='Times 15 bold',command = summarize).place(x= 220, y=360)
    Label(top, text = '-----------------------------------------------------------------', font='Times 15 bold').place(x= 20, y=410)
    Button(top, text = 'Report Teacher', font='Times 15 bold',command = spam_words).place(x= 20, y=440)
    
    
    

def mail():
    


    EMAIL_ADDRESS = "dynamiccompetition123@gmail.com"
    EMAIL_PASSWORD = "Dynamiccompetition@123"

    msg = EmailMessage()
    msg['Subject'] = 'This is regarding your student result'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = 'dynamiccompetition123@gmail.com'     #type in ur mailid

    msg.set_content(' ')
    r_set=conn.execute('''SELECT * from tasks''');
    r_set=list(r_set)
    xaxis=[i[1] for i in r_set]
    yaxis=[i[2] for i in r_set]
    #print(yaxis)
    
    plt.bar(xaxis, yaxis, color ='maroon',width = 0.4)
    plt.xlabel('subjects')
    plt.ylabel('marks')
    plt.savefig('C:/Users/pksds/Desktop/read.png',tranparent=True)
    
    with open('C:/Users/pksds/Desktop/read.png','rb') as f:
        filedata=f.read()
        filetype=imghdr.what(f.name)
        filename="analysis"

    msg.add_attachment(filedata,maintype='image',subtype=filetype,filename=filename)
    

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)



    

def mailspam():

    EMAIL_ADDRESS = "dynamiccompetition123@gmail.com"
    EMAIL_PASSWORD = "Dynamiccompetition@123"

    msg = EmailMessage()
    msg['Subject'] = 'Reporting Teacher'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = 'dynamiccompetition123@gmail.com'    

    msg.set_content(' ')
    msg.add_alternative("""\
    <!DOCTYPE html>
    <html>
    
        
        <body>
            <p style="color:SlateGray;">Good Morning,</p>
            <p style="color:SlateGray;">This is to state that the teacher had used
            inappropriate langauge and behaved wrongly.Hence i am reporting it to the concerned authorities and
            please look into it.</p>
            
        </body>
    </html>
    """, subtype='html')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)





def spam_words():
    quotes = open("text.txt",encoding="utf8")
    contents_of_files = quotes.read()
    
    contents_of_files = contents_of_files.replace('\n', ' ').replace('\r', '').replace('\t', '').replace(' ', '')
    quotes.close()
    check_profanity(contents_of_files)

def check_profanity(text_to_check):
    with open('C:/Users/pksds/Desktop/text.txt',encoding="utf8") as f:
        text = f.read()
    with open('C:/Users/pksds/Desktop/spam.txt',encoding="utf8") as f:
        spam = f.read()
    spam=spam.split()
    text1=text.split()
    text1=text1[1:100]
    for i in text1:
        if(i in spam):
            print(i)

    http = urllib3.PoolManager()
    connection = http.request("GET", "http://www.wdylike.appspot.com/?q="+text_to_check)
    output = json.loads(connection.data.decode('utf-8'))
    
    if output==True:
        
        mailspam()
        tkinter.messagebox.showinfo(" Profanity alert!!!","Informed to authorities")
    elif output==False:
        print("\n\nThis document has to curse words!")
    else:
        print("\n\nCould not scan document properly.")



def summarize():
    with open('C:/Users/pksds/Desktop/text.txt',encoding="utf8") as f:
        text = f.read()
    
    

    
    stopWords = set(stopwords.words("english"))
    words = word_tokenize(text)

    freqTable = dict()
    for word in words:
        word = word.lower()
        if word in stopWords:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1

    sentences = sent_tokenize(text)
    sentenceValue = dict()
       
    for sentence in sentences:
        for word, freq in freqTable.items():
            if word in sentence.lower():
                if sentence in sentenceValue:
                    sentenceValue[sentence] += freq
                else:
                    sentenceValue[sentence] = freq
       
       
       
    sumValues = 0
    for sentence in sentenceValue:
        sumValues += sentenceValue[sentence]

       
    average = int(sumValues / len(sentenceValue))
       
    
    summary = ''
    for sentence in sentences:
        if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * average)):
            summary += " " + sentence
    #print(summary)
    f=open("summaryofnotes.txt","w+")
    f.write(summary)
    f.close()


def aud():
    r = sr.Recognizer()


    with sr.AudioFile('Audio1.wav') as source:
        
        audio_text = r.listen(source)
        
        try:

            text = r.recognize_google(audio_text)
            
            print(text)
            f=open("text.txt","w+")
            f.write(text)
            f.close()
         
        except:
             print('Sorry.. run again...')




Button(root,text="Teacher", font='Times 14 bold',bg='dark gray', command = teacher,width=10).place(x= 20, y=80)
Button(root,text="Student", font='Times 14 bold',bg='dark gray', command = student,width=10).place(x= 170, y=80)


root.mainloop()
