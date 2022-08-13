# auth.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from models import User
from models import db
import os
from flask import Flask, render_template, request, session, redirect,flash,url_for
from werkzeug.utils import secure_filename
import json
import os
import math
from datetime import datetime
from flask_caching import Cache
from flask import jsonify
from flask import json
import requests
from flask import send_from_directory
import docx
import docx2txt
import sys 
import math 
import pdfplumber 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PyPDF2 import PdfFileReader
from flask import Flask
import re
import json
import jinja2
import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from pickle import dump, load
from nltk.corpus import brown
from itertools import dropwhile
from nltk import word_tokenize, pos_tag
from flask import send_file
from io import StringIO
import pandas as pd
from pdfminer.high_level import extract_text
import spacy
nlp = spacy.load('en_core_web_sm')
from spacy.matcher import Matcher
import datetime
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import plotly.io as pio
from flask_login import LoginManager 
from flask_sqlalchemy import SQLAlchemy
from openpyxl import load_workbook
from random import randint
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
#Imports end Here

#download Nltk Packages
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('brown')
nltk.download('punkt')
#nltk packages download end here


#Define Flask App and other APP COnfigs
app = Flask(__name__)
app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER']='./uploads'

ALLOWED_EXTENSIONS ={'pdf','docx','doc','png'}

#Rules for extentions Defined



#Verify File Names
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower()in {'pdf','docx','doc','png'}

#Define Global Variables since its needed

keyword = "N"
text_main=""
length = 0
match=0


#Define Database Model and Login manager
from models import db

db.init_app(app)

with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))



# blueprint for non-auth parts of app
from main import main as main_blueprint
app.register_blueprint(main_blueprint)


#route for login
@app.route('/login')
def login():
    return render_template('login.html')


#Route for login after post
@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password): 
        flash('Please check your login details and try again.')
        return redirect(url_for('login')) # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))


#Route For Signup
@app.route('/signup')
def signup():
    return render_template('candidate.html')

#Data Storage For Signup
@app.route('/signup', methods=['POST'])
def signup_post():
    
#Get the required values and if not found, then set as null

    email = str(request.form.get('email')) if request.form.get('email') else "NA" 
    password = str(request.form.get('password')) if request.form.get('password') else 'NA' 
    nationality = str(request.form.get('nationality')) if request.form.get('nationality') else 'NA'
    first_name = str(request.form.get('first_name')) if request.form.get('first_name') else 'NA'
    last_name = str(request.form.get('last_name')) if request.form.get('last_name') else 'NA'
    area_code = str(request.form.get('area_code')) if request.form.get('area_code') else 'NA'
    phone = str(request.form.get('phone')) if request.form.get('phone') else 'NA'
    industry = str(request.form.get('industry')) if request.form.get('industry') else 'NA'
    # functional = str(request.form.get('functional')) if request.form.get('functional') else 'NA'
    # experience = str(request.form.get('experience')) if request.form.get('experience') else 'NA'
    # n1 = str(request.form.get('n1')) if request.form.get('n1') else 'NA'
    # d1 = str(request.form.get('d1')) if request.form.get('d1') else 'NA'
    # sd1 = str(request.form.get('sd1')) if request.form.get('sd1') else 'NA'
    # ed1 = str(request.form.get('ed1')) if request.form.get('ed1') else 'NA'
    # cwh = str(request.form.get('cwh')) if request.form.get('cwh') else 'NA'
    # n2 = str(request.form.get('n2')) if request.form.get('n2') else 'NA'
    # d2 = str(request.form.get('d2')) if request.form.get('d2') else 'NA'
    # sd2 = str(request.form.get('sd2')) if request.form.get('sd2') else 'NA'
    # ed2 = str(request.form.get('ed2')) if request.form.get('ed2') else 'NA'
    # n3 = str(request.form.get('n3')) if request.form.get('n3') else 'NA'
    # d3 = str(request.form.get('d3')) if request.form.get('d3') else 'NA'
    # sd3 = str(request.form.get('sd3')) if request.form.get('sd3') else 'NA'
    # ed3 = str(request.form.get('ed3')) if request.form.get('ed3') else 'NA'
    # n4 = str(request.form.get('n4')) if request.form.get('n4') else 'NA'
    # d4 = str(request.form.get('d4')) if request.form.get('d4') else 'NA'
    # sd4 = str(request.form.get('sd4')) if request.form.get('sd4') else 'NA'
    # ed4 = str(request.form.get('ed4')) if request.form.get('ed4') else 'NA'
    # n5 = str(request.form.get('n5')) if request.form.get('n5') else 'NA'
    # d5 = str(request.form.get('d5')) if request.form.get('d5') else 'NA'
    # sd5 = str(request.form.get('sd5')) if request.form.get('sd5') else 'NA'
    # ed5 = str(request.form.get('ed5')) if request.form.get('ed5') else 'NA'
    # n6 = str(request.form.get('n6')) if request.form.get('n6') else 'NA'
    # d6 = str(request.form.get('d6')) if request.form.get('d6') else 'NA'
    # sd6 = str(request.form.get('sd6')) if request.form.get('sd6') else 'NA'
    # ed6 = str(request.form.get('ed6')) if request.form.get('ed6') else 'NA'
    # n7 = str(request.form.get('n7')) if request.form.get('n7') else 'NA'
    # d7 = str(request.form.get('d7')) if request.form.get('d7') else 'NA'
    # sd7 = str(request.form.get('sd7')) if request.form.get('sd7') else 'NA'
    # ed7 = str(request.form.get('ed7')) if request.form.get('ed7') else 'NA'
    # n8 = str(request.form.get('n8')) if request.form.get('n8') else 'NA'
    # d8 = str(request.form.get('d8')) if request.form.get('d8') else 'NA'
    # sd8 = str(request.form.get('sd8')) if request.form.get('sd8') else 'NA'
    # ed8 = str(request.form.get('ed8')) if request.form.get('ed8') else 'NA'
    # n9 = str(request.form.get('n9')) if request.form.get('n9') else 'NA'
    # d9 = str(request.form.get('d9')) if request.form.get('d9') else 'NA'
    # sd9 = str(request.form.get('sd9')) if request.form.get('sd9') else 'NA'
    # ed9 = str(request.form.get('ed9')) if request.form.get('ed9') else 'NA'
    # n10 = str(request.form.get('n10')) if request.form.get('n10') else 'NA'
    # d10 = str(request.form.get('d10')) if request.form.get('d10') else 'NA'
    # sd10 = str(request.form.get('sd10')) if request.form.get('sd10') else 'NA'
    # ed10 = str(request.form.get('ed10')) if request.form.get('ed10') else 'NA'
    # n11 = str(request.form.get('n11')) if request.form.get('n11') else 'NA'
    # d11 = str(request.form.get('d11')) if request.form.get('d11') else 'NA'
    # sd11 = str(request.form.get('sd11')) if request.form.get('sd11') else 'NA'
    # ed11 = str(request.form.get('ed11')) if request.form.get('ed11') else 'NA'
    # n12 = str(request.form.get('n12')) if request.form.get('n12') else 'NA'
    # d12 = str(request.form.get('d12')) if request.form.get('d12') else 'NA'
    # sd12 = str(request.form.get('sd12')) if request.form.get('sd12') else 'NA'
    # ed12 = str(request.form.get('ed12')) if request.form.get('ed12') else 'NA'
    # n13 = str(request.form.get('n13')) if request.form.get('n13') else 'NA'
    # d13 = str(request.form.get('d13')) if request.form.get('d13') else 'NA'
    # sd13 = str(request.form.get('sd13')) if request.form.get('sd13') else 'NA'
    # ed13 = str(request.form.get('ed13')) if request.form.get('ed13') else 'NA'
    # n14 = str(request.form.get('n14')) if request.form.get('n14') else 'NA'
    # d14 = str(request.form.get('d14')) if request.form.get('d14') else 'NA'
    # sd14 = str(request.form.get('sd14')) if request.form.get('sd14') else 'NA'
    # ed14 = str(request.form.get('ed14')) if request.form.get('ed14') else 'NA'
    # n15 = str(request.form.get('n15')) if request.form.get('n15') else 'NA'
    # d15 = str(request.form.get('d15')) if request.form.get('d15') else 'NA'
    # sd15 = str(request.form.get('sd15')) if request.form.get('sd15') else 'NA'
    # ed15 = str(request.form.get('ed15')) if request.form.get('ed15') else 'NA'
    # n16 = str(request.form.get('n16')) if request.form.get('n16') else 'NA'
    # d16 = str(request.form.get('d16')) if request.form.get('d16') else 'NA'
    # sd16 = str(request.form.get('sd16')) if request.form.get('sd16') else 'NA'
    # ed16 = str(request.form.get('ed16')) if request.form.get('ed16') else 'NA'
    # n17 = str(request.form.get('n17')) if request.form.get('n17') else 'NA'
    # d17 = str(request.form.get('d17')) if request.form.get('d17') else 'NA'
    # sd17 = str(request.form.get('sd17')) if request.form.get('sd17') else 'NA'
    # ed17 = str(request.form.get('ed17')) if request.form.get('ed17') else 'NA'
    # n18 = str(request.form.get('n18')) if request.form.get('n17') else 'NA'
    # d18 = str(request.form.get('d18')) if request.form.get('d18') else 'NA'
    # sd18 = str(request.form.get('sd18')) if request.form.get('sd18') else 'NA'
    # ed18 = str(request.form.get('ed18')) if request.form.get('ed18') else 'NA'
    # n19 = str(request.form.get('n19')) if request.form.get('n19') else 'NA'
    # d19 = str(request.form.get('d19')) if request.form.get('d19') else 'NA'
    # sd19 = str(request.form.get('sd19')) if request.form.get('sd19') else 'NA'
    # ed19 = str(request.form.get('ed19')) if request.form.get('ed19') else 'NA'
    # n20 = str(request.form.get('n20')) if request.form.get('n20') else 'NA'
    # d20 = str(request.form.get('d20')) if request.form.get('d20') else 'NA'
    # sd20 = str(request.form.get('sd20')) if request.form.get('sd20') else 'NA'
    # ed20 = str(request.form.get('ed20')) if request.form.get('ed20') else 'NA'
    # np = str(request.form.get('np')) if request.form.get('np') else 'NA'
    # ctc = str(request.form.get('ctc')) if request.form.get('ctc') else 'NA'
    # number = str(request.form.get('number')) if request.form.get('number') else 'NA'
    # variable = str(request.form.get('variable')) if request.form.get('variable') else 'NA'
    # benefits = str(request.form.get('benefits')) if request.form.get('benefits') else 'NA'
    # cloc = str(request.form.get('cloc')) if request.form.get('cloc') else 'NA'
    # ploc = str(request.form.get('ploc')) if request.form.get('ploc') else 'NA'
    # qualification = str(request.form.get('qualification')) if request.form.get('qualification') else 'NA'
    # type1 = str(request.form.get('type')) if request.form.get('type') else 'NA'
    # degree = str(request.form.get('degree')) if request.form.get('degree') else 'NA'
    # sd21 = str(request.form.get('sd21')) if request.form.get('sd21') else 'NA'
    # ed21 = str(request.form.get('ed21')) if request.form.get('ed21') else 'NA'
    # skills = str(request.form.get('skills')) if request.form.get('skills') else 'NA'
    # resume_text_new = str(request.form.get('resume')) if request.form.get('resume') else 'NA'
    # busi= str(request.form.get('busi')) if request.form.get('busi') else 'NA'
    # k=request.form.getlist('t')
    # k='; '.join(k)
    # t=k
    coun='0'
    status='true'
    
    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again  
        flash('Email address already exists')
        return redirect(url_for('signup'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(email=email,  password=generate_password_hash(password, method='sha256'), nationality= nationality, first_name = first_name, last_name = last_name, area_code = str(area_code), phone = str(phone), industry = industry, count_used=coun, status=status)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('login'))


#Route For Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))



#optional route to store candidate details in csv
@app.route('/candidate', methods=['GET','POST'])
@login_required
def candidate():
    if request.method=='POST':
        data = request.form #all form field data
        k=request.form.getlist('t')
        k='; '.join(k) #multiple checkbox employment type
        res =str(data) +", "+str(k)
        
        kd=[]
        for m in data:
            if m!='t':
                kd.append(data[m])

        kd.append(k)
        wb = load_workbook("Candidate.xlsx")
# Select First Worksheet
        ws = wb.worksheets[0]


        ws.append(kd)

        wb.save("Candidate.xlsx")


        
        return render_template('jd.html')
    return render_template('candidate.html')


#Route for resume Audit
@app.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    try:
        f_name = os.path.join(app.config['UPLOAD_FOLDER'],filename)

        global text_main,length,match,keyword
        file_name = f_name
        
        impact = 0
        pres =0
        text_main = ""
        edu_msg =0 
        vol_msg=0
        pro_msg=0
        jd_msg=""

        #Check if resume is Docx, PDF or any other Format
        if(file_name[-3:]=="pdf"):
            
            jd_score=pdf(file_name)
            
        elif(file_name[-4:] == "docx"):
            
            jd_score=docx1(file_name)
            
        else:
            
            return render_template('unsupported.html')
        
        
        text_count=text_main.split(" ")
        word_count=len(text_count)
        liness=[]
        line=""
        line1=[]
    
        
        #Store resume Text as a list of sentences
        
        if(file_name[-4:] == "docx" ):
            for i in text_main:
                
                if(i!='\n'):
                    line+=i
                else:
                    liness.append(line)
                    line=""
            
            for line in liness:
                if len(line)!=0:
                    line1.append(line)
        elif(file_name[-3:]=="pdf"):
            liness=text_main.split("\\n")
   
                    
            
            for line in liness:
                if len(line)!=0:
                    line1.append(line)

        
        #Find Phone Number
        phone=re.findall(r"(?<!\d)\d{10}(?!\d)", text_main)
        
        #Find email
        email=re.findall(r"([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)",text_main)
        
        #Find Links
        links= re.findall(r"(^(http\:\/\/|https\:\/\/)?([a-z0-9][a-z0-9\-]*\.)+[a-z0-9][a-z0-9\-]*)",text_main)
        
        #Segregate social Media links
        mlink=[]
        for link in links:
            if 'facebook' in link:
                mlink.append(link)
            elif 'github' in link:
                mlink.append(link)
            elif 'linkedin' in link:
                mlink.append(link)
            else:
                links.remove(link)
        links=list(set(mlink))
        section=[]
        sections={}
        line2=[]
        
        #List of titles with with Resume headings are checked
        titles=['education','Licensures', 'Professional Qualification', 'academic qualification', 'Educational Qualification', 'academia', 'education and professional development', 'academic credentials', 'educational summary', 'academic profile', 'Experience', 'work experience', 'Job Titles held', 'Position Description and purpose', 'Professional Experience', 'Professional Summary', 'Profile', 'Qualifications', 'Employment History', 'history', 'previous employment', 'organisational experience', 'employers', 'positions of responsibility','Position of Responsibilities', 'employment scan', 'past experience', 'organizational experience', 'career', 'experience and qualification summary', 'relevant experience', 'experience summary', 'career synopsis', 'career timeline', 'banking IT experience', 'AML & FCM Suite Experience', 'employment details', 'Skill','skills', 'Technical Skills', 'Soft Skills', 'Key Skills', 'Design Skills', 'Expertise', 'Abilities', 'Area of Expertise', 'Key attributes', 'Computer Skills', 'IT Skills', 'Technical Expertise', 'Technical Skills Set', 'Functional Skill Set', 'functional skills', 'strengths', 'areas of expertise', 'banking knowledge', 'Award', 'Honours and awards', 'Key achievements', 'Accomplishments', 'Highlights', 'Affiliations', 'Achievements', 'Extra Curricular activities and achievements', 'awards and recognition','awards/achievements', 'Certificate', 'Most proud of', 'Specialization', 'Certifications', 'Certification/training','Coursework','other credentials', 'professional accomplishments', 'certification & trainings', 'scholastics', 'professional credentials and certifications','Project','projects', 'Additional Activities', 'Activities', 'Major Tasks', 'Responsibilities', 'key accountabilities', 'Contributions', 'Personal Projects', 'Key Contributions', 'Strategic Planning and execution', 'Academic projects', 'Key projects', 'projects/trainings', 'key implementations','Volunteer', 'Volunteer Experience', 'Affiliations', 'Misc','Extra Curricular Activities', 'Community Service','EDUCATIONAL BACKGROUND','INTERNSHIPS EXPERIENCE','WINNING PORTFOLIO','AWARDS & RECOGNITIONS','CORE COMPETENCIES','PROJECTS ADMINISTERED','TECHNICAL SKILLS','CERTIFICATIONS','VOLUNTEERING','PERSONAL DOSSIER','Licensure', 'Professional Qualifications', 'academic qualifications', 'academics qualification', 'academics qualifications',  'Educational Qualifications', 'education and professional developments', 'academic credential', 'academics credential', 'academics credentials', 'educational summaries', 'academic profiles', 'academics profile','Experiences', 'work experiences', 'Position Descriptions and purpose', 'Positions Description and purpose', 'Positions Descriptions and purpose', 'Professional Experiences', 'Profiles', 'Qualification', 'Employment Histories', 'previous employments', 'organisational experiences', 'organizational experiences', 'organizational experience', 'employer', 'positions of responsibilities', 'position of responsibility', 'position of responsibilities', 'employment scans', 'past experiences', 'organizational experiences', 'organisational experience', 'organisational experiences', 'careers', 'experiences and qualifications summary', 'experience and qualifications summary', 'experiences and qualification summary', 'relevant experiences', 'career timelines', 'banking IT experiences', 'AML & FCM Suite Experiences', 'employment details', 'employment detail','Skills', 'Technical Skill', 'Soft Skill', 'Key Skill', 'Design Skill', 'Expertises', 'Ability', 'Areas of Expertises', 'Areas of Expertise', 'Area of Expertises', 'Key attribute', 'Computer Skill', 'IT Skill', 'Technical Expertises', 'Technical Skill Set', 'Technical Skill Sets', 'Functional Skills Set', 'Functional Skill Sets', 'Functional Skills Sets', 'functional skill', 'strength', 'area of expertise', 'area of expertises','Awards', 'Key achievement', 'Accomplishment', 'Highlight', 'Affiliation', 'Achievement', 'Extra Curricular activities and achievements',  'Extra Curricular activity and achievements',  'Extra Curricular activities and achievement',  'Extra Curricular activity and achievement', 'awards and recognitions',  'award and recognition',  'award and recognitions', 'Certificates', 'Specializations', 'Certification', 'Certifications/trainings', 'Certifications/training', 'Certification/trainings', 'other credential', 'professional accomplishment', 'certifications & trainings', 'certifications & training', 'certification & training', 'scholastic', 'professional credential and certification', 'professional credential and certifications', 'professional credentials and certification','Project', 'Additional Activity', 'Activity', 'Major Task', 'Responsibily', 'key accountability', 'Contribution', 'Personal Project', 'Key Contribution', 'Strategic Plannings and executions', 'Strategic Plannings and execution', 'Strategic Planning and executions', 'Academic project', 'Key project', 'project/training', 'projects/training', 'project/trainings', 'key implementation','Volunteer', 'Volunteer Experiences', 'Affiliation', 'Community Services' ]
        titles1=[x.lower() for x in titles]
       
       #Append the sections and respective content 
        for i in line1:
            if i[-1]==" ":
                line2.append(i[:-1])
            else:
                line2.append(i)
        
        line1=line2
        temp = '\t'.join(titles1)
        for x in line1:
            
            global keyword
            if(x==line1[-1]):
            
                section.append(x)
                sections[keyword] = section
                keyword = x
                    
                section =[]
                break
            elif x.lower() not in temp:
                section.append(x)
                
            elif (len(x.split(" "))>=4):
                section.append(x)
                
            
                
            else :
                if(len(section)!=0):
                    sections[keyword] = section
                    keyword = x
                    
                    section =[]
                else:
                    sections[keyword]=[]
                    keyword=x
                    section =[]
                    
        
        sections['phone']=list(set(phone))
        sections['links']=mlink
        if (len(mlink) != 0):
            impact+=5


        #Keyword Denoting Different Important Sections
        ed_list=['Education', 'Education Details','Licensures', 'Professional Qualification', 'academic qualification', 'Educational Qualification', 'academia', 'education and professional development', 'academic credentials', 'educational summary', 'academic profile','EDUCATIONAL BACKGROUND','Licensure', 'Professional Qualifications', 'academic qualifications', 'academics qualification', 'academics qualifications',  'Educational Qualifications', 'education and professional developments', 'academic credential', 'academics credential', 'academics credentials', 'educational summaries', 'academic profiles', 'academics profile']
        ex_list=['Experience', 'Experience Details','work experience', 'Job Titles held', 'Position Description and purpose', 'Professional Experience', 'Professional Summary', 'Profile', 'Qualifications', 'Employment History', 'history', 'previous employment', 'organisational experience', 'employers', 'positions of responsibility', 'employment scan','past experience', 'organizational experience', 'career', 'experience and qualification summary', 'relevant experience', 'experience summary', 'career synopsis', 'career timeline', 'banking IT experience', 'AML & FCM Suite Experience', 'employment details','INTERNSHIPS EXPERIENCE','Experiences', 'work experiences', 'Position Descriptions and purpose', 'Positions Description and purpose', 'Positions Descriptions and purpose', 'Professional Experiences', 'Profiles', 'Qualification', 'Employment Histories', 'previous employments', 'organisational experiences', 'organizational experiences', 'organizational experience', 'employer', 'positions of responsibilities', 'position of responsibility', 'position of responsibilities', 'employment scans', 'past experiences', 'organizational experiences', 'organisational experience', 'organisational experiences', 'careers', 'experiences and qualifications summary', 'experience and qualifications summary', 'experiences and qualification summary', 'relevant experiences', 'career timelines', 'banking IT experiences', 'AML & FCM Suite Experiences', 'employment details', 'employment detail', 'career progression']
        sk_list=['Skill', 'Technical Skills', 'Soft Skills', 'Key Skills', 'Design Skills', 'Expertise', 'Abilities', 'Area of Expertise', 'Key attributes', 'Computer Skills', 'IT Skills', 'Technical Expertise', 'Technical Skills Set', 'Functional Skill Set', 'functional skills', 'strengths', 'areas of expertise', 'banking knowledge','WINNING PORTFOLIO','CORE COMPETENCIES','TECHNICAL SKILLS','skills','Skills', 'Technical Skill', 'Soft Skill', 'Key Skill', 'Design Skill', 'Expertises', 'Ability', 'Areas of Expertises', 'Areas of Expertise', 'Area of Expertises', 'Key attribute', 'Computer Skill', 'IT Skill', 'Technical Expertises', 'Technical Skill Set', 'Technical Skill Sets', 'Functional Skills Set', 'Functional Skill Sets', 'Functional Skills Sets', 'functional skill', 'strength', 'area of expertise', 'area of expertises']
        aw_list=['Award' , 'Achievement Details','Honours and awards', 'Key achievements', 'Accomplishments', 'Highlights', 'Affiliations', 'Achievements', 'Extra Curricular activities and achievements', 'awards and recognition','AWARDS & RECOGNITIONS','awards','achievements','Awards', 'Key achievement', 'Accomplishment', 'Highlight', 'Affiliation', 'Achievement', 'Extra Curricular activities and achievements',  'Extra Curricular activity and achievements',  'Extra Curricular activities and achievement',  'Extra Curricular activity and achievement', 'awards and recognitions',  'award and recognition',  'award and recognitions']
        ce_list=['Certificate', 'Certification Details','Most proud of', 'Specialization', 'Certifications', 'Certification/training', 'other credentials', 'professional accomplishments', 'certification & trainings', 'scholastics', 'professional credentials and certifications','CERTIFICATION','coursework', 'competencies', 'Certificates', 'Specializations', 'Certification', 'Certifications/trainings', 'Certifications/training', 'Certification/trainings', 'other credential', 'professional accomplishment', 'certifications & trainings', 'certifications & training', 'certification & training', 'scholastic', 'professional credential and certification', 'professional credential and certifications', 'professional credentials and certification',  'key accountability', 'Contribution', 'Personal Project', 'Key Contribution', 'Strategic Plannings and executions', 'Strategic Plannings and execution', 'Strategic Planning and executions',]
        pe_list=['Project', 'Project Details','Additional Activities', 'Activities', 'Major Tasks', 'Responsibilities', 'key accountabilities', 'Contributions', 'Personal Projects', 'Key Contributions', 'Strategic Planning and execution', 'Academic projects', 'Key projects', 'projects/trainings', 'key implementations','PROJECTS ADMINISTERED','projects','Project', 'Additional Activity', 'Activity', 'Major Task', 'Responsibily', 'key accountability', 'Contribution', 'Personal Project', 'Key Contribution', 'Strategic Plannings and executions', 'Strategic Plannings and execution', 'Strategic Planning and executions', 'Academic project', 'Key project', 'project/training', 'projects/training', 'project/trainings', 'key implementation','Additional Activity', 'Activity', 'Major Task', 'Responsibily', 'Academic project', 'Key project', 'project/training', 'projects/training', 'project/trainings', 'key implementation']
        vo_list=['Volunteer', 'Volunteer Details','Volunteer Experience', 'Affiliations', 'Misc', 'Community Service','VOLUNTEERING','extra curricular activities','EXTRA-CURRICULAR INVOLVEMENT','Volunteer', 'Volunteer Experiences', 'Affiliation', 'Community Services']
        ed1_list=[x.lower() for x in ed_list]
        temp_ed= '\t'.join(ed1_list)
        ex1_list=[x.lower() for x in ex_list]
        temp_ex='\t'.join(ex1_list)
        sk1_list=[x.lower() for x in sk_list]
        temp_sk='\t'.join(sk1_list)
        aw1_list=[x.lower() for x in aw_list]
        temp_aw='\t'.join(aw1_list)
        ce1_list=[x.lower() for x in ce_list]
        temp_ce='\t'.join(ce1_list)
        pe1_list=[x.lower() for x in pe_list]
        temp_pe='\t'.join(pe1_list)
        vo1_list=[x.lower() for x in vo_list]
        temp_vol='\t'.join(vo1_list)
        
        score = 0
        msg = []
        edu=0
        ed=0
        ex=0
        sk=0
        aw=0
        ce=0
        pe=0
        vo=0
        ed_date_format_list=[0,0]
        ex_date_format_list=[0,0]
        ach_msg = 0 
        cert_msg = 0 
        sections['edu_year']=""
        sections['exp_year']=""
        sections['paragraph']=0
        checkfornos=0
        alphanum=""
        checkfornos2=0
        

        #Check for different sections and give marks accordingly. Also set the flag values
        for key in sections.keys():
            
            for i in ed1_list:
                if(i in key.lower() and ed==0 and key.lower()!='n'):
                    score +=10
                    pres+=10
                    edu = 1
                    ed=1
                    edu_msg =1
                    ed_date_format_list=date_format(sections[key])
                    if ed_date_format_list>0:
                        score-=10
                        pres-=10
                    
                    sections['edu_year']=extract(sections[key])
                    sections['paragraph']+=paragraph_check(sections[key])
                    
                    msg.append("Education Section is Present")
                    break
                
            for i in ex1_list:    
                if(i in key.lower() and ex==0 and key.lower()!='n'):
                    score +=20
                    ex=1
                    sections['exp_year']=extract(sections[key])
                    ex_date_format_list=date_format(sections[key])
                    impact+=20
                    sections['paragraph']+=paragraph_check(sections[key])
                            
                    msg.append("Experience Section is Present")
                    
                    break
                
            for i in sk1_list:
                if(i in key.lower() and sk==0 and key.lower()!='n'):
                    score +=20
                    sk=1
                    msg.append("Skills Section is Present")
                    sections['paragraph']+=paragraph_check(sections[key])
                    break
            for i in aw1_list:    
                if(i in key.lower() and aw==0 and key.lower()!='n'):
                    score +=5
                    impact+=5
                    aw=1
                    ach_msg = 1
                    alpha_num = ['one','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen','twenty','thirty','fourty','fifty','sixty','seventy','eighty','ninety','hundred','thousand']
                    checkfornos = checknos(sections[key],alpha_num)
                    sections['paragraph']+=paragraph_check(sections[key])
                    msg.append("Awards/Achievement Section is Present")
                    
                    break
            for i in vo1_list:    
                if(i in key.lower() and vo==0 and key.lower()!='n'):
                    pres+=5
                    score +=5
                    vo=1
                    vol_msg =1
                    msg.append("Volunteering Section is Present")
                    
                    break
            for i in ce1_list:    
                if(i in key.lower() and ce==0 and key.lower()!='n'):
                    impact+=5
                    score +=10
                    cert_msg=1
                    ce=1
                    msg.append("Certificate Section is Present")
                    
                    break
            for i in pe1_list:    
                if(i in key.lower() and pe==0 and key.lower()!='n'):
                    pres+=10
                    pe=1
                    score +=10
                    pro_msg=1
                    sections['paragraph']+=paragraph_check(sections[key])
                    alpha_num = ['one','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen','twenty','thirty','fourty','fifty','sixty','seventy','eighty','ninety','hundred','thousand']
                    checkfornos2 = checknos(sections[key],alpha_num)
                    msg.append("Projects Section is Present")
                    
                    break
        list_present=[ed,ex,sk,aw,ce,pe,vo]
        fed=0
        fex=0
        fsk=0
        faw=0
        fce=0
        fpe=0
        fvo=0
        sect=[]
        
        
        #Check which flags arent set and give marks accordingly. If flags arent set, check if corresponding keywords are present
        for i in range(len(list_present)):
            if i ==0 and list_present[i]==0:
                
                for ik in ed1_list:
                    if ik in text_main.lower():
                        fed=1
                score+=5
            if i ==1 and list_present[i]==0:
                
                for ik in ex1_list:
                    if ik in text_main.lower():
                        fex=1
                score+=10
            if i ==2 and list_present[i]==0:
                
                for ik in sk1_list:
                    if ik in text_main.lower():
                        fsk=1
                score+=10
            if i ==3 and list_present[i]==0:
                
                for ik in aw1_list:
                    if ik in text_main.lower():
                        faw=1
                score+=2
            if i ==4 and list_present[i]==0:
                
                for ik in ce1_list:
                    if ik in text_main.lower():
                        fce=1
                score+=5
            if i ==5 and list_present[i]==0:
                
                for ik in pe1_list:
                    if ik in text_main.lower():
                        fpe=1
                score+=5
            if i ==6 and list_present[i]==0:
                
                for ik in vo1_list:
                    if ik in text_main.lower():
                        fvo=1
                score+=2
        
        
        #Check Which section has Improper Format
        improper_format=[]
        if(fed==1 and ed==0):
            improper_format.append('education')
        if(fex==1 and ex==0):
            improper_format.append('experience')
        if(fsk==1 and sk==0):
            improper_format.append('skill')
        if(faw==1 and aw==0):
            improper_format.append('achievement')
        if(fce==1 and ce==0):
            improper_format.append('certification')
        if(fpe==1 and pe==0):
            improper_format.append('project')
        if(fvo==1 and vo==0):
            improper_format.append('volunteer')
        
            
        
        sections['Message']=msg
        
        rev=""
        
        #Check for stop Words        
        stop_words = set(stopwords.words('english')) 
        d=""
        skillsets=0
        filtered_sentence=[]
        
        #Find sections for work experience and competency and mark accordingly
        for i in sections.keys():
            if(i.lower()=="work experience"):
                score +=5
            if(i.lower()=="core competencies"):
                score +=5            
            if 'skill' in i.lower():
                skillsets=len(sections[i])
                for j in sections[i]:
                     
                    d=d+" "+j
                d = word_tokenize(d)
                 
                for w in d: 
                    if w not in stop_words: 
                        if(len(w)>3):
                            filtered_sentence.append(w)
    
        
        
        sections['SkCount']=skillsets
        
        sections['linkedin']=Find(text_main)
        ck=sections['linkedin']
        link_msg=1
        if(len(ck) == 0):
            link_msg=0
        
        ac=0
        rd=0
        action_list=[]
        act_msg=0

        #Check for action Words in Resume
        if actionwords(text_main)[0] > 5 :
            act_msg =1
            action_list=actionwords(text_main)[1]
            ac=10
            sections['action_word']="Your resume contains Action Verbs! Strong, unique action verbs show hiring managers that you have held different roles and skill sets. They also help your accomplishments stand out and make them more impactful."
        elif actionwords(text_main)[0]<=5:
            act_msg =0
            sections['action_word']="Your resume doesnt contain much Action Verbs! Strong, unique action verbs show hiring managers that you have held different roles and skill sets. They also help your accomplishments stand out and make them more impactful. "
        elif actionwords(text_main)[0]==0:
            
            act_msg =0
            sections['action_word']="Your resume doesnt contain any Action Verbs! Strong, unique action verbs show hiring managers that you have held different roles and skill sets. They also help your accomplishments stand out and make them more impactful. "
        
        
        #Check for filler words in resume
        fct_msg=0
        filler_list=[]
        if fillerwords(text_main)[0] > 1 :
            fct_msg =1
            filler_list=fillerwords(text_main)[1]
            
            
        
        elif fillerwords(text_main)[0]==0:
            
            fct_msg =0
            
        
        #Check for Redundant words
        if redundancy(text_main) > 10:
            rd=5
            sections['redundancy']="1"
        elif redundancy(text_main)<=10:
            sections['redundancy']="0"
            
        
        
        sections['match']=match
        
        #Calculate The Score
        if(score == 100):
            rev="The Resume looks perfect but to get a more accurate comparison with the job you are looking for try analysing by adding Job Description"
        elif(score < 60):
            rev="The analysis suggests that there is a lot of room for improvement. But don't worry! We have highlighted a number of quick fixes you can make to improve your resume's score and your success rate. Try adding more skills or experience into your resume to increase your resume score to 80% or above."
        else:
            rev="Your Resume looks good however we have highlighted a number of quick fixes you can make to improve your resume's score. Try adding more skills or experience into your resume to increase your resume score."
        sections["Review"]=rev
        sections["Length"]=length
        sections["WordCount"]=word_count
        #Check Wordcount
        if sections["WordCount"] <= 600 and sections["WordCount"] > 1:
            score += 5
            sections['Message'].append("Word Count of the Resume is Optimal")
        else:
            sections['Message'].append("Word Count should be less than 600")

        #Check Length of Resume
        if sections["Length"] and sections["WordCount"] > 1:
            score += 5
            sections['Message'].append("Length of Resume is Optimal")
        else:
            sections['Message'].append("Length of Resume should not exceed 2 pages")
        sections['Score']=round(((score/100)*100),2) #calculating score out of overall score.
        if(sections['Score'] >=90 and sections['Score'] <100):
            sections["Review"]="The Resume is correctly Parsed and Optimal. There may be some room for Improvement"
        if(sections['Score'] >=75 and sections['Score']<90):
            sections["Review"]="The Resume may be Correctly Parsed and Optimal. It is advised to pass DOCX Format in ATS Checker. There is certainly Some Room For Improvement"        
        
        #Check for passive Form
        count_passive1=[]
        count_passive=0
        co_pa=0
        for i in line1:
            if(is_passive(re.sub(r'[^\x00-\x7f]',r'', i))):
                count_passive += 1
                count_passive1.append(re.sub(r'[^\x00-\x7f]',r'', i))
        
                
        if(count_passive > 0):
            co_pa= 1
        elif(len(line1)==0):
            co_pa= 1
            
        else:
            co_pa=0
            ac += 5
        
        
        #Check whether tenses have been used incorrectly
        count_tense1=[]
        co_ta=0
        count_tenses=0
        for i in line1:
            if(tenses_res(re.sub(r'[^\x00-\x7f]',r'', i))):
                count_tenses += 1
                count_tense1.append(re.sub(r'[^\x00-\x7f]',r'', i))
                
        if(count_tenses >= 5):
            co_ta= 1
        elif(len(line1)==0):
            co_ta= 1
            
        else:
            co_ta=0
            ac += 5
            
        #Check whether there is a balance between bullet points and Paragraphs
        if(len(line1)==0):
            sections['paragraph']=0 
        elif sections['paragraph'] <= 2:
            ac += 5
            
        
        
        #Check whether all contact details are present of not
        cont=[]
        contact_all=contact_details(text_main)
        for elem in contact_all:
            if elem:
                if len(contact_all[0]) == 0:
                    cont.append('email')
                if len(contact_all[1]) == 0:
                    cont.append('phone')
                if len(contact_all[2]) == 0:
                    cont.append('linkedin')
                if len(contact_all[0]) !=0 and len(contact_all[1])!=0 and len(contact_all[2])!=0:
                    cont.append('all')
                    break

            if elem not in contact_all:
                cont.append("none")
        cont1=list(set(cont))
        cont=cont1    
            
        #Store Keywords for critical competencies
        analytical =['Research', 'collected', 'conducted', 'defined', 'detected', 'discovered', 'examined',
        'experimented', 'explored', 'extracted', 'found', 'gathered', 'identified', 'inquired', 'inspected',
        'investigated', 'located', 'measured', 'modelled', 'observed', 'researched', 'reviewed', 'searched',
        'studied',' surveyed', 'tested', 'tracked', 'Analyse', 'Evaluate', 'analysed', 'assessed', 'calculated',
        'catalogued', 'categorized', 'clarified', 'classified', 'compared', 'compiled', 'critiqued', 
        'derived', 'determined', 'diagnosed', 'estimated', 'evaluated', 'formulated', 'interpreted',
        'prescribed', 'organized', 'rated', 'recommended', 'reported', 'summarized', 'systematized', 
        'tabulated', 'assembled', 'built', 'coded', 'computed', 'constructed', 'converted', 'debugged',
        'designed', 'engineered', 'fabricated', 'installed', 'maintained', 'operated',
        'printed', 'programmed', 'proved', 'rectified', 'regulated', 'repaired', 'resolved',
        'restored', 'specified', 'standardized', 'upgraded', 'adjusted', 'allocated', 'appraised',
        'audited', 'balanced', 'budgeted', 'conserved', 'controlled', 'disbursed', 'figured', 'financed',
        'forecasted', 'netted', 'projected', 'reconciled']

        communication = ['addressed', 'articulated', 'authored', 'briefed', 'clarified', 
        'conveyed', 'composed', 'condensed', 'corresponded', 'debated', 'delivered', 'described',
        'discussed', 'drafted', 'edited', 'expressed', 'formulated', 'informed', 'instructed',
        'interacted', 'interpreted', 'lectured', 'negotiated', 'notified', 'outlined', 'reconciled',
        'reinforced', 'reported', 'presented', 'proposed', 'specified', 'spoke', 'translated',
        'wrote', 'advertised', 'influenced', 'marketed', 'solicited', 'contacted', 'convinced',
        'represented', 'persuaded', 'motivated',' communicated', 'elicited', 
        'recruited', 'promoted', 'publicized', 'enlisted', 'arbitrated', 'consulted', 'conferred',
        'interviewed', 'mediated', 'moderated', 'listened', 'responded', 'suggested']

        leadership = ['administered', 'appointed', 'approved', 'assigned', 'authorized', 'chaired',
        'conducted', 'contracted', 'controlled', 'coordinated', 'decided', 'delegated', 'directed',
        'developed', 'enforced', 'ensured', 'evaluated', 'executed', 'headed', 'hired', 'hosted', 
        'implemented', 'instituted', 'led', 'managed', 'overhauled', 'oversaw', 'prioritized', 
        'recruited', 'represented', 'strategized', 'supervised', 'trained', 'anticipated', 'arranged',
        'contacted', 'convened', 'logged', 'obtained', 'ordered', 'planned',
        'prepared', 'processed', 'purchased', 'recorded', 'registered', 'reserved', 'scheduled', 
        'verified', 'consolidated', 'distributed', 'eliminated', 'filed', 'grouped', 'incorporated',
        'merged', 'monitored', 'organized', 'regulated', 'reviewed', 'routed', 'standardized',
        'structured', 'submitted', 'systematized', 'updated']

        teamwork = ['aided', 'answered', 'arranged', 'catalogued', 'categorized', 'collated', 'collected',
        'coordinated', 'distributed', 'emailed', 'ensured', 'expedited', 'explained', 'filed', 'greeted',
        'handled', 'informed', 'implemented', 'maintained', 'offered', 'ordered', 'organized', 'performed',
        'prepared', 'processed', 'provided', 'purchased', 'recorded', 'received', 'resolved', 'scheduled', 'served',
        'supported', 'tabulated', 'collaborated', 'consulted', 'cooperated', 'liaised', 'reached', 
        'out']

        initiative = ['authored', 'began', 'built', 'changed', 'combined', 'conceived', 'constructed',
        'created', 'customized', 'designed', 'developed', 'devised', 'established', 'formed',
        'formulated', 'founded', 'generated', 'initiated', 'integrated', 'introduced', 'invented',
        'launched', 'originated', 'produced', 'shaped', 'staged', 'visualized', 'modified', 'revamped',
        'revised', 'updated', 'advocated', 'aided', 'assisted', 'cared', 'contributed', 'cooperated',
        'coordinated', 'ensured', 'furthered', 'guided', 'intervened', 'offered', 'referred',
        'rehabilitated', 'supplied', 'supported', 'volunteered', 'served', 'adapted', 'advised',
        'clarified', 'coached', 'counselled', 'demonstrated', 'educated', 'enabled',
        'encouraged', 'evaluated', 'explained', 'facilitated', 'familiarized', 'individualized',
        'instructed', 'mentored', 'modelled' ] 


        ab = text_main.lower()
        sentence = nltk.tokenize.sent_tokenize(ab)
        comp1 = check(sentence,analytical)
        

        #Count no of keywords corresponding to each critical competency
        try:
            comp1_count = len(comp1)
        except:
            comp1_count = 0
        comp2 = check(sentence,communication)
        try:
            comp2_count = len(comp2)
        except:
            comp2_count = 0
        
        comp3 = check(sentence,leadership)
        try:
            comp3_count = len(comp3)
        except:
            comp3_count = 0
        
        comp4 = check(sentence,teamwork)
        try:
            comp4_count = len(comp4)
        except:
            comp4_count = 0
        
        comp5 = check(sentence,initiative)
        try:
            comp5_count = len(comp5)
        except:
            comp5_count = 0
        

        
        
        #Create dictionaries to store words and Counts
        
        match_dict = {'analytical' : comp1, 'communication': comp2, 'leadership': comp3, 'teamwork': comp4,
                    'initiative': comp5} 
        
        count_dict = {'analytical' : comp1_count, 'communication': comp2_count, 'leadership': comp3_count, 
                    'teamwork': comp4_count, 'initiative': comp5_count}


        count_competancies=[]
        for i in count_dict.keys():
            if(count_dict[i]!=0):
                count_competancies.append(i)
        sumaa=0
        for key in count_dict.keys():
            sumaa+=count_dict[key]

        nl=[]
        quant=0
        if checkfornos==1 or checkfornos2==1:
            quant=1
        elif checkfornos!=1 and checkfornos2!=1:
            nl=quan(text_main,aw1_list+pe1_list )
        if(nl[1]):
            quant=1
                
        
        ab = text_main.lower()
        sentence = nltk.tokenize.sent_tokenize(ab)

       
        
        session['bared'] = count_dict
        count_dict_dict={}
        stop_words = set(stopwords.words('english')) 
        
        #remove stopwords
        filtered_sentence = [w for w in sentence if not w in stop_words] 
        for i in filtered_sentence:
            count_dict_dict[i]=filtered_sentence.count(i)

        
                
        
        #Check if date format is correct or wrong
        if ed_date_format_list==1:
            pres-=5
        
        skillmatch=skillsMatch(text_main)

        namee=extract_name(text_main)
        empty_competency=""
        cot=0
        for i in match_dict.keys():
            cot=cot+len(match_dict[i])

        if(cot==0):
            empty_competency = "You might want to add few competencies in your resume as it's an efficient way to provide comprehensive proof that you are qualified for a certain job. "

        
        keys_chart = [k for k in count_dict]
    
        values_chart = [count_dict[k] for k in count_dict]
        if len(count_passive1)>5:
            count_passive1=count_passive1[:5]
        if len(count_tense1)>5:
            count_tense1=count_tense1[:5]
        
        return render_template('services.html', results=sections,skillmatch=skillmatch, quant=quant, empty_competency=empty_competency,name=namee,fct_msg=fct_msg,filler_list=filler_list,wc=word_count,pro_msg=pro_msg,edu_msg=edu_msg,matched_comment= rev,jd_msg=jd_msg,score= sections['Score'],email=email,education=edu,rud_mdg=sections['redundancy'],vol_msg=vol_msg,cert_msg=cert_msg,link_msg=link_msg,ach_msg = ach_msg,count_pass=co_pa,count_tense=co_ta,act_msg=act_msg,para=sections['paragraph'],action_list=list(set(action_list)),count_tense1=count_tense1,count_passive1=count_passive1,contacts=cont,edu_year=sections['edu_year'],exp_year=sections['exp_year'],imp_for=improper_format,fed=fed,fex=fex,fsk=fsk,fce=fce,fpe=fpe,faw=faw,fvo=fvo,ed_correct_year=ed_date_format_list,ex_correct_year=ex_date_format_list,count_dict=count_dict,match_dict=match_dict,count_competancies=count_competancies,sumaa=sumaa, depth=int(((ac+rd)/30*100)),pres=int(pres/25*100),impact=int(impact/45 *100),keys_chart=keys_chart,values_chart=values_chart)
           
    except Exception as e:
        print(e)
        return render_template('error_page.html')










    
    
@app.route('/details')
@login_required
def detailed():
    return render_template('detailed.html')


@app.route('/chrtjs')
@login_required
def chrtjs():
    return render_template('chrt.html')


@app.route('/',methods= ["GET",'POST'])
@app.route('/home',methods= ["GET",'POST'])
def resume():
    return render_template('index0.html')

@app.route('/demo',methods= ["GET",'POST'])
@login_required
def demo():
    return render_template('services.html')




    
#route to recieve JD and Resume
@app.route('/analyse',methods= ["GET",'POST'])
@login_required
def analyse():
    if request.method == 'POST':
        session.pop('data', None)
        session['data'] = request.form['jd']
        
        
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No Selected File')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename= secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            
            return redirect (url_for('uploaded_file',filename=filename))
    return render_template('elements.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def uploadfile():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      return 'file uploaded successfully'

@app.route('/jd',methods= ["GET",'POST'])
@login_required
def jd_analyse():
    ct=""
    if request.method == 'POST':
        session.pop('data', None)
        session['data'] = request.form['jd']
        session['email'] = request.form['Login Email']
        user = User.query.filter_by(email=session['email']).first()
        print(user)
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No Selected File')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename= secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            if not user: 
                flash('Please check your email and try again.')
                return redirect(url_for('login'))
            else:
                ct=int(user.count_used)
                print(ct)
                user.count_used=str(ct+1)
                db.session.commit()
                print(user.email, user.count_used)
                
                
                return redirect (url_for('jd_file',filename=filename))
    return render_template('jd.html')




#Route for JD
@app.route('/jd/<filename>')
@login_required
def jd_file(filename):
    try:
        user = User.query.filter_by(email=session['email']).first()
        if user.status =="false":
                flash('Subscription has not been activated yet. Contact Admin Support @email')
                return render_template("login.html")
        if int(user.count_used)>=50:
            user=User.query.filter_by(email=session['email'])
            user.status="false"
            flash('Subscription Expired. Subscribe again or Contact Admin Support @email')
            return render_template("login.html")

        f_name = os.path.join(app.config['UPLOAD_FOLDER'],filename)
        # return f_name
        global text_main,length,match,keyword
        file_name = f_name
        print(f_name)
        impact = 0
        pres =0
        text_main = ""
        edu_msg =0 
        vol_msg=0
        pro_msg=0
        jd_msg=""
        typee=0
        if(file_name[-3:]=="pdf"):
            
            jd_score=pdf(file_name)
            typee=0
            
        elif(file_name[-4:] == "docx"):
            
            jd_score=docx1(file_name)
            typee=1
 
            
        else:
            
            return render_template('unsupported.html')
        
        
        text_count=text_main.split(" ")
        word_count=len(text_count)
        liness=[]
        line=""
        line1=[]
        if(file_name[-4:] == "docx" ):
            for i in text_main:
                
                if(i!='\n'):
                    line+=i
                else:
                    liness.append(line)
                    line=""
            
            for line in liness:
                if len(line)!=0:
                    line1.append(line)
        elif(file_name[-3:]=="pdf"):
            liness=text_main.split("\\n")
    
                    
            
            for line in liness:
                if len(line)!=0:
                    line1.append(line)

        
        
        phone=re.findall(r"(?<!\d)\d{10}(?!\d)", text_main)
        email=re.findall(r"([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)",text_main)
        
        links= re.findall(r"(^(http\:\/\/|https\:\/\/)?([a-z0-9][a-z0-9\-]*\.)+[a-z0-9][a-z0-9\-]*)",text_main)
        mlink=[]
        for link in links:
            if 'facebook' in link:
                mlink.append(link)
            elif 'github' in link:
                mlink.append(link)
            elif 'linkedin' in link:
                mlink.append(link)
            else:
                links.remove(link)
        links=list(set(mlink))
        section=[]
        sections={}
        line2=[]
        titles=['education','Licensures', 'Professional Qualification', 'academic qualification', 'Educational Qualification', 'academia', 'education and professional development', 'academic credentials', 'educational summary', 'academic profile', 'Experience', 'work experience', 'Job Titles held', 'Position Description and purpose', 'Professional Experience', 'Professional Summary', 'Profile', 'Qualifications', 'Employment History', 'history', 'previous employment', 'organisational experience', 'employers', 'positions of responsibility','Position of Responsibilities', 'employment scan', 'past experience', 'organizational experience', 'career', 'experience and qualification summary', 'relevant experience', 'experience summary', 'career synopsis', 'career timeline', 'banking IT experience', 'AML & FCM Suite Experience', 'employment details', 'Skill','skills', 'Technical Skills', 'Soft Skills', 'Key Skills', 'Design Skills', 'Expertise', 'Abilities', 'Area of Expertise', 'Key attributes', 'Computer Skills', 'IT Skills', 'Technical Expertise', 'Technical Skills Set', 'Functional Skill Set', 'functional skills', 'strengths', 'areas of expertise', 'banking knowledge', 'Award', 'Honours and awards', 'Key achievements', 'Accomplishments', 'Highlights', 'Affiliations', 'Achievements', 'Extra Curricular activities and achievements', 'awards and recognition','awards/achievements', 'Certificate', 'Most proud of', 'Specialization', 'Certifications', 'Certification/training','Coursework','other credentials', 'professional accomplishments', 'certification & trainings', 'scholastics', 'professional credentials and certifications','Project','projects', 'Additional Activities', 'Activities', 'Major Tasks', 'Responsibilities', 'key accountabilities', 'Contributions', 'Personal Projects', 'Key Contributions', 'Strategic Planning and execution', 'Academic projects', 'Key projects', 'projects/trainings', 'key implementations','Volunteer', 'Volunteer Experience', 'Affiliations', 'Misc','Extra Curricular Activities', 'Community Service','EDUCATIONAL BACKGROUND','INTERNSHIPS EXPERIENCE','WINNING PORTFOLIO','AWARDS & RECOGNITIONS','CORE COMPETENCIES','PROJECTS ADMINISTERED','TECHNICAL SKILLS','CERTIFICATIONS','VOLUNTEERING','PERSONAL DOSSIER','Licensure', 'Professional Qualifications', 'academic qualifications', 'academics qualification', 'academics qualifications',  'Educational Qualifications', 'education and professional developments', 'academic credential', 'academics credential', 'academics credentials', 'educational summaries', 'academic profiles', 'academics profile','Experiences', 'work experiences', 'Position Descriptions and purpose', 'Positions Description and purpose', 'Positions Descriptions and purpose', 'Professional Experiences', 'Profiles', 'Qualification', 'Employment Histories', 'previous employments', 'organisational experiences', 'organizational experiences', 'organizational experience', 'employer', 'positions of responsibilities', 'position of responsibility', 'position of responsibilities', 'employment scans', 'past experiences', 'organizational experiences', 'organisational experience', 'organisational experiences', 'careers', 'experiences and qualifications summary', 'experience and qualifications summary', 'experiences and qualification summary', 'relevant experiences', 'career timelines', 'banking IT experiences', 'AML & FCM Suite Experiences', 'employment details', 'employment detail','Skills', 'Technical Skill', 'Soft Skill', 'Key Skill', 'Design Skill', 'Expertises', 'Ability', 'Areas of Expertises', 'Areas of Expertise', 'Area of Expertises', 'Key attribute', 'Computer Skill', 'IT Skill', 'Technical Expertises', 'Technical Skill Set', 'Technical Skill Sets', 'Functional Skills Set', 'Functional Skill Sets', 'Functional Skills Sets', 'functional skill', 'strength', 'area of expertise', 'area of expertises','Awards', 'Key achievement', 'Accomplishment', 'Highlight', 'Affiliation', 'Achievement', 'Extra Curricular activities and achievements',  'Extra Curricular activity and achievements',  'Extra Curricular activities and achievement',  'Extra Curricular activity and achievement', 'awards and recognitions',  'award and recognition',  'award and recognitions', 'Certificates', 'Specializations', 'Certification', 'Certifications/trainings', 'Certifications/training', 'Certification/trainings', 'other credential', 'professional accomplishment', 'certifications & trainings', 'certifications & training', 'certification & training', 'scholastic', 'professional credential and certification', 'professional credential and certifications', 'professional credentials and certification','Project', 'Additional Activity', 'Activity', 'Major Task', 'Responsibily', 'key accountability', 'Contribution', 'Personal Project', 'Key Contribution', 'Strategic Plannings and executions', 'Strategic Plannings and execution', 'Strategic Planning and executions', 'Academic project', 'Key project', 'project/training', 'projects/training', 'project/trainings', 'key implementation','Volunteer', 'Volunteer Experiences', 'Affiliation', 'Community Services' ]
        titles1=[x.lower() for x in titles]
        for i in line1:
            if i[-1]==" ":
                line2.append(i[:-1])
            else:
                line2.append(i)
        
        line1=line2
        temp = '\t'.join(titles1)
        for x in line1:
            
            global keyword
            if(x==line1[-1]):
            
                section.append(x)
                sections[keyword] = section
                keyword = x
                    
                section =[]
                break
            elif x.lower() not in temp:
                section.append(x)
               
            elif (len(x.split(" "))>=4):
                section.append(x)
                  
            
                
            else :
                if(len(section)!=0):
                    sections[keyword] = section
                    keyword = x
                    
                    section =[]
                else:
                    sections[keyword]=[]
                    keyword=x
                    section =[]
                    
        sections['phone']=list(set(phone))
        sections['links']=mlink
        if (len(mlink) != 0):
            impact+=5
        
        ed_list=['Education', 'Education Details','Licensures', 'Professional Qualification', 'academic qualification', 'Educational Qualification', 'academia', 'education and professional development', 'academic credentials', 'educational summary', 'academic profile','EDUCATIONAL BACKGROUND','Licensure', 'Professional Qualifications', 'academic qualifications', 'academics qualification', 'academics qualifications',  'Educational Qualifications', 'education and professional developments', 'academic credential', 'academics credential', 'academics credentials', 'educational summaries', 'academic profiles', 'academics profile']
        ex_list=['Experience', 'Experience Details','work experience', 'Job Titles held', 'Position Description and purpose', 'Professional Experience', 'Professional Summary', 'Profile', 'Qualifications', 'Employment History', 'history', 'previous employment', 'organisational experience', 'employers', 'positions of responsibility', 'employment scan','past experience', 'organizational experience', 'career', 'experience and qualification summary', 'relevant experience', 'experience summary', 'career synopsis', 'career timeline', 'banking IT experience', 'AML & FCM Suite Experience', 'employment details','INTERNSHIPS EXPERIENCE','Experiences', 'work experiences', 'Position Descriptions and purpose', 'Positions Description and purpose', 'Positions Descriptions and purpose', 'Professional Experiences', 'Profiles', 'Qualification', 'Employment Histories', 'previous employments', 'organisational experiences', 'organizational experiences', 'organizational experience', 'employer', 'positions of responsibilities', 'position of responsibility', 'position of responsibilities', 'employment scans', 'past experiences', 'organizational experiences', 'organisational experience', 'organisational experiences', 'careers', 'experiences and qualifications summary', 'experience and qualifications summary', 'experiences and qualification summary', 'relevant experiences', 'career timelines', 'banking IT experiences', 'AML & FCM Suite Experiences', 'employment details', 'employment detail', 'career progression']
        sk_list=['Skill', 'Technical Skills', 'Soft Skills', 'Key Skills', 'Design Skills', 'Expertise', 'Abilities', 'Area of Expertise', 'Key attributes', 'Computer Skills', 'IT Skills', 'Technical Expertise', 'Technical Skills Set', 'Functional Skill Set', 'functional skills', 'strengths', 'areas of expertise', 'banking knowledge','WINNING PORTFOLIO','CORE COMPETENCIES','TECHNICAL SKILLS','skills','Skills', 'Technical Skill', 'Soft Skill', 'Key Skill', 'Design Skill', 'Expertises', 'Ability', 'Areas of Expertises', 'Areas of Expertise', 'Area of Expertises', 'Key attribute', 'Computer Skill', 'IT Skill', 'Technical Expertises', 'Technical Skill Set', 'Technical Skill Sets', 'Functional Skills Set', 'Functional Skill Sets', 'Functional Skills Sets', 'functional skill', 'strength', 'area of expertise', 'area of expertises']
        aw_list=['Award' , 'Achievement Details','Honours and awards', 'Key achievements', 'Accomplishments', 'Highlights', 'Affiliations', 'Achievements', 'Extra Curricular activities and achievements', 'awards and recognition','AWARDS & RECOGNITIONS','awards','achievements','Awards', 'Key achievement', 'Accomplishment', 'Highlight', 'Affiliation', 'Achievement', 'Extra Curricular activities and achievements',  'Extra Curricular activity and achievements',  'Extra Curricular activities and achievement',  'Extra Curricular activity and achievement', 'awards and recognitions',  'award and recognition',  'award and recognitions']
        ce_list=['Certificate', 'Certification Details','Most proud of', 'Specialization', 'Certifications', 'Certification/training', 'other credentials', 'professional accomplishments', 'certification & trainings', 'scholastics', 'professional credentials and certifications','CERTIFICATION','coursework', 'competencies', 'Certificates', 'Specializations', 'Certification', 'Certifications/trainings', 'Certifications/training', 'Certification/trainings', 'other credential', 'professional accomplishment', 'certifications & trainings', 'certifications & training', 'certification & training', 'scholastic', 'professional credential and certification', 'professional credential and certifications', 'professional credentials and certification',  'key accountability', 'Contribution', 'Personal Project', 'Key Contribution', 'Strategic Plannings and executions', 'Strategic Plannings and execution', 'Strategic Planning and executions',]
        pe_list=['Project', 'Project Details','Additional Activities', 'Activities', 'Major Tasks', 'Responsibilities', 'key accountabilities', 'Contributions', 'Personal Projects', 'Key Contributions', 'Strategic Planning and execution', 'Academic projects', 'Key projects', 'projects/trainings', 'key implementations','PROJECTS ADMINISTERED','projects','Project', 'Additional Activity', 'Activity', 'Major Task', 'Responsibily', 'key accountability', 'Contribution', 'Personal Project', 'Key Contribution', 'Strategic Plannings and executions', 'Strategic Plannings and execution', 'Strategic Planning and executions', 'Academic project', 'Key project', 'project/training', 'projects/training', 'project/trainings', 'key implementation','Additional Activity', 'Activity', 'Major Task', 'Responsibily', 'Academic project', 'Key project', 'project/training', 'projects/training', 'project/trainings', 'key implementation']
        vo_list=['Volunteer', 'Volunteer Details','Volunteer Experience', 'Affiliations', 'Misc', 'Community Service','VOLUNTEERING','extra curricular activities','EXTRA-CURRICULAR INVOLVEMENT','Volunteer', 'Volunteer Experiences', 'Affiliation', 'Community Services']
        ed1_list=[x.lower() for x in ed_list]
        temp_ed= '\t'.join(ed1_list)
        ex1_list=[x.lower() for x in ex_list]
        temp_ex='\t'.join(ex1_list)
        sk1_list=[x.lower() for x in sk_list]
        temp_sk='\t'.join(sk1_list)
        aw1_list=[x.lower() for x in aw_list]
        temp_aw='\t'.join(aw1_list)
        ce1_list=[x.lower() for x in ce_list]
        temp_ce='\t'.join(ce1_list)
        pe1_list=[x.lower() for x in pe_list]
        temp_pe='\t'.join(pe1_list)
        vo1_list=[x.lower() for x in vo_list]
        temp_vol='\t'.join(vo1_list)
        
        score = 0
        msg = []
        edu=0
        ed=0
        ex=0
        sk=0
        aw=0
        ce=0
        pe=0
        vo=0
        ed_date_format_list=[0,0]
        ex_date_format_list=[0,0]
        ach_msg = 0 #achievement variable message
        cert_msg = 0 #certification message flag
        sections['edu_year']=""
        sections['exp_year']=""
        sections['paragraph']=0
        checkfornos=0
        alphanum=""
        checkfornos2=0
        
        for key in sections.keys():
            
            for i in ed1_list:
                if(i in key.lower() and ed==0 and key.lower()!='n'):
                    score +=10
                    pres+=10
                    edu = 1
                    ed=1
                    edu_msg =1
                    ed_date_format_list=date_format(sections[key])
                    if ed_date_format_list>0:
                        score-=10
                        pres-=10
                    
                    sections['edu_year']=extract(sections[key])
                    sections['paragraph']+=paragraph_check(sections[key])
                    
                    msg.append("Education Section is Present")
                    break
                
            for i in ex1_list:    
                if(i in key.lower() and ex==0 and key.lower()!='n'):
                    score +=20
                    ex=1
                    sections['exp_year']=extract(sections[key])
                    ex_date_format_list=date_format(sections[key])
                    impact+=20
                    sections['paragraph']+=paragraph_check(sections[key])
                            
                    msg.append("Experience Section is Present")
                    
                    break
                
            for i in sk1_list:
                if(i in key.lower() and sk==0 and key.lower()!='n'):
                    score +=20
                    sk=1
                    msg.append("Skills Section is Present")
                    sections['paragraph']+=paragraph_check(sections[key])
                    break
            for i in aw1_list:    
                if(i in key.lower() and aw==0 and key.lower()!='n'):
                    score +=5
                    impact+=5
                    aw=1
                    ach_msg = 1
                    alpha_num = ['one','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen','twenty','thirty','fourty','fifty','sixty','seventy','eighty','ninety','hundred','thousand']
                    checkfornos = checknos(sections[key],alpha_num)
                    sections['paragraph']+=paragraph_check(sections[key])
                    msg.append("Awards/Achievement Section is Present")
                    
                    break
            for i in vo1_list:    
                if(i in key.lower() and vo==0 and key.lower()!='n'):
                    pres+=5
                    score +=5
                    vo=1
                    vol_msg =1
                    msg.append("Volunteering Section is Present")
                    
                    break
            for i in ce1_list:    
                if(i in key.lower() and ce==0 and key.lower()!='n'):
                    impact+=5
                    score +=10
                    cert_msg=1
                    ce=1
                    msg.append("Certificate Section is Present")
                    
                    break
            for i in pe1_list:    
                if(i in key.lower() and pe==0 and key.lower()!='n'):
                    pres+=10
                    pe=1
                    score +=10
                    pro_msg=1
                    sections['paragraph']+=paragraph_check(sections[key])
                    alpha_num = ['one','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen','twenty','thirty','fourty','fifty','sixty','seventy','eighty','ninety','hundred','thousand']
                    checkfornos2 = checknos(sections[key],alpha_num)
                    msg.append("Projects Section is Present")
                   
                    break
        list_present=[ed,ex,sk,aw,ce,pe,vo]
        fed=0
        fex=0
        fsk=0
        faw=0
        fce=0
        fpe=0
        fvo=0
        sect=[]
        
        
        
        for i in range(len(list_present)):
            if i ==0 and list_present[i]==0:
                
                for ik in ed1_list:
                    if ik in text_main.lower():
                        fed=1
                score+=5
            if i ==1 and list_present[i]==0:
                
                for ik in ex1_list:
                    if ik in text_main.lower():
                        fex=1
                score+=10
            if i ==2 and list_present[i]==0:
                
                for ik in sk1_list:
                    if ik in text_main.lower():
                        fsk=1
                score+=10
            if i ==3 and list_present[i]==0:
                
                for ik in aw1_list:
                    if ik in text_main.lower():
                        faw=1
                score+=2
            if i ==4 and list_present[i]==0:
                
                for ik in ce1_list:
                    if ik in text_main.lower():
                        fce=1
                score+=5
            if i ==5 and list_present[i]==0:
                
                for ik in pe1_list:
                    if ik in text_main.lower():
                        fpe=1
                score+=5
            if i ==6 and list_present[i]==0:
                
                for ik in vo1_list:
                    if ik in text_main.lower():
                        fvo=1
                score+=2
        
        improper_format=[]
        if(fed==1 and ed==0):
            improper_format.append('education')
        if(fex==1 and ex==0):
            improper_format.append('experience')
        if(fsk==1 and sk==0):
            improper_format.append('skill')
        if(faw==1 and aw==0):
            improper_format.append('achievement')
        if(fce==1 and ce==0):
            improper_format.append('certification')
        if(fpe==1 and pe==0):
            improper_format.append('project')
        if(fvo==1 and vo==0):
            improper_format.append('volunteer')
        
            
        
        sections['Message']=msg
        
        rev=""
        
                
        stop_words = set(stopwords.words('english')) 
        d=""
        skillsets=0
        filtered_sentence=[]
        
    
        for i in sections.keys():
            if(i.lower()=="work experience"):
                score +=5
            if(i.lower()=="core competencies"):
                score +=5            
            if 'skill' in i.lower():
                skillsets=len(sections[i])
                for j in sections[i]:
                     
                    d=d+" "+j
                d = word_tokenize(d)
                 
                for w in d: 
                    if w not in stop_words: 
                        if(len(w)>3):
                            filtered_sentence.append(w)
    
        sections['SkCount']=skillsets
        
        sections['linkedin']=Find(text_main)
        ck=sections['linkedin']
        link_msg=1
        if(len(ck) == 0):
            link_msg=0
        
        ac=0
        rd=0
        action_list=[]
        act_msg=0
        if actionwords(text_main)[0] > 5 :
            act_msg =1
            action_list=actionwords(text_main)[1]
            ac=10
            sections['action_word']="Your resume contains Action Verbs! Strong, unique action verbs show hiring managers that you have held different roles and skill sets. They also help your accomplishments stand out and make them more impactful."
        elif actionwords(text_main)[0]<=5:
            act_msg =0
            sections['action_word']="Your resume doesnt contain much Action Verbs! Strong, unique action verbs show hiring managers that you have held different roles and skill sets. They also help your accomplishments stand out and make them more impactful. "
        elif actionwords(text_main)[0]==0:
            
            act_msg =0
            sections['action_word']="Your resume doesnt contain any Action Verbs! Strong, unique action verbs show hiring managers that you have held different roles and skill sets. They also help your accomplishments stand out and make them more impactful. "
        fct_msg=0
        filler_list=[]
        if fillerwords(text_main)[0] > 1 :
            fct_msg =1
            filler_list=fillerwords(text_main)[1]
            
           
        
        elif fillerwords(text_main)[0]==0:
            
            fct_msg =0
            
        
        if redundancy(text_main) > 10:
            rd=5
            sections['redundancy']="1"
        elif redundancy(text_main)<=10:
            sections['redundancy']="0"
            
        
        
        sections['match']=match
        
        if(score == 100):
            rev="the score looks perfect but to get a more accurate comparison with the job you are looking for try analysing by adding Job Description"
        elif(score < 60):
            rev="this score suggests there is a lot of room for improvement. But don't worry! We have highlighted a number of quick fixes you can make to improve your resume's score and your success rate. Try adding more skills or experience into your resume to increase your resume score to 80% or above."
        else:
            rev="your score looks good however we have highlighted a number of quick fixes you can make to improve your resume's score. Try adding more skills or experience into your resume to increase your resume score."
        sections["Review"]=rev
        sections["Length"]=length
        sections["WordCount"]=word_count
        if sections["WordCount"] <= 600 and sections["WordCount"] > 1:
            score += 5
            sections['Message'].append("Word Count of the Resume is Optimal")
        else:
            sections['Message'].append("Word Count should be less than 600")

        if sections["Length"] and sections["WordCount"] > 1:
            score += 5
            sections['Message'].append("Length of Resume is Optimal")
        else:
            sections['Message'].append("Length of Resume should not exceed 2 pages")
        sections['Score']=round(((score/100)*100),2) #calculating score out of overall score.
        if(sections['Score'] >=90 and sections['Score'] <100):
            sections["Review"]="The Resume is correctly Parsed and Optimal. There may be some room for Improvement"
        if(sections['Score'] >=75 and sections['Score']<90):
            sections["Review"]="The Resume may be Correctly Parsed and Optimal. It is advised to pass DOCX Format in ATS Checker. There is certainly Some Room For Improvement"        
        count_passive1=[]
        count_passive=0
        co_pa=0
        for i in line1:
            if(is_passive(re.sub(r'[^\x00-\x7f]',r'', i))):
                count_passive += 1
                count_passive1.append(re.sub(r'[^\x00-\x7f]',r'', i))
        
                
        if(count_passive > 0):
            co_pa= 1
        elif(len(line1)==0):
            co_pa= 1
            
        else:
            co_pa=0
            ac += 5
        
        count_tense1=[]
        co_ta=0
        count_tenses=0
        for i in line1:
            if(tenses_res(re.sub(r'[^\x00-\x7f]',r'', i))):
                count_tenses += 1
                count_tense1.append(re.sub(r'[^\x00-\x7f]',r'', i))
                
        if(count_tenses >= 5):
            co_ta= 1
        elif(len(line1)==0):
            co_ta= 1
            
        else:
            co_ta=0
            ac += 5
            
        if(len(line1)==0):
            sections['paragraph']=0 
        elif sections['paragraph'] <= 2:
            ac += 5
            
        
        
        
        cont=[]
        contact_all=contact_details(text_main)
        for elem in contact_all:
            if elem:
                if len(contact_all[0]) == 0:
                    cont.append('email')
                if len(contact_all[1]) == 0:
                    cont.append('phone')
                if len(contact_all[2]) == 0:
                    cont.append('linkedin')
                if len(contact_all[0]) !=0 and len(contact_all[1])!=0 and len(contact_all[2])!=0:
                    cont.append('all')
                    break

            if elem not in contact_all:
                cont.append("none")
            
        

        analytical =['Research', 'collected', 'conducted', 'defined', 'detected', 'discovered', 'examined',
        'experimented', 'explored', 'extracted', 'found', 'gathered', 'identified', 'inquired', 'inspected',
        'investigated', 'located', 'measured', 'modelled', 'observed', 'researched', 'reviewed', 'searched',
        'studied',' surveyed', 'tested', 'tracked', 'Analyse', 'Evaluate', 'analysed', 'assessed', 'calculated',
        'catalogued', 'categorized', 'clarified', 'classified', 'compared', 'compiled', 'critiqued', 
        'derived', 'determined', 'diagnosed', 'estimated', 'evaluated', 'formulated', 'interpreted',
        'prescribed', 'organized', 'rated', 'recommended', 'reported', 'summarized', 'systematized', 
        'tabulated', 'assembled', 'built', 'coded', 'computed', 'constructed', 'converted', 'debugged',
        'designed', 'engineered', 'fabricated', 'installed', 'maintained', 'operated',
        'printed', 'programmed', 'proved', 'rectified', 'regulated', 'repaired', 'resolved',
        'restored', 'specified', 'standardized', 'upgraded', 'adjusted', 'allocated', 'appraised',
        'audited', 'balanced', 'budgeted', 'conserved', 'controlled', 'disbursed', 'figured', 'financed',
        'forecasted', 'netted', 'projected', 'reconciled']

        communication = ['addressed', 'articulated', 'authored', 'briefed', 'clarified', 
        'conveyed', 'composed', 'condensed', 'corresponded', 'debated', 'delivered', 'described',
        'discussed', 'drafted', 'edited', 'expressed', 'formulated', 'informed', 'instructed',
        'interacted', 'interpreted', 'lectured', 'negotiated', 'notified', 'outlined', 'reconciled',
        'reinforced', 'reported', 'presented', 'proposed', 'specified', 'spoke', 'translated',
        'wrote', 'advertised', 'influenced', 'marketed', 'solicited', 'contacted', 'convinced',
        'represented', 'persuaded', 'motivated',' communicated', 'elicited', 
        'recruited', 'promoted', 'publicized', 'enlisted', 'arbitrated', 'consulted', 'conferred',
        'interviewed', 'mediated', 'moderated', 'listened', 'responded', 'suggested']

        leadership = ['administered', 'appointed', 'approved', 'assigned', 'authorized', 'chaired',
        'conducted', 'contracted', 'controlled', 'coordinated', 'decided', 'delegated', 'directed',
        'developed', 'enforced', 'ensured', 'evaluated', 'executed', 'headed', 'hired', 'hosted', 
        'implemented', 'instituted', 'led', 'managed', 'overhauled', 'oversaw', 'prioritized', 
        'recruited', 'represented', 'strategized', 'supervised', 'trained', 'anticipated', 'arranged',
        'contacted', 'convened', 'logged', 'obtained', 'ordered', 'planned',
        'prepared', 'processed', 'purchased', 'recorded', 'registered', 'reserved', 'scheduled', 
        'verified', 'consolidated', 'distributed', 'eliminated', 'filed', 'grouped', 'incorporated',
        'merged', 'monitored', 'organized', 'regulated', 'reviewed', 'routed', 'standardized',
        'structured', 'submitted', 'systematized', 'updated']

        teamwork = ['aided', 'answered', 'arranged', 'catalogued', 'categorized', 'collated', 'collected',
        'coordinated', 'distributed', 'emailed', 'ensured', 'expedited', 'explained', 'filed', 'greeted',
        'handled', 'informed', 'implemented', 'maintained', 'offered', 'ordered', 'organized', 'performed',
        'prepared', 'processed', 'provided', 'purchased', 'recorded', 'received', 'resolved', 'scheduled', 'served',
        'supported', 'tabulated', 'collaborated', 'consulted', 'cooperated', 'liaised', 'reached', 
        'out']

        initiative = ['authored', 'began', 'built', 'changed', 'combined', 'conceived', 'constructed',
        'created', 'customized', 'designed', 'developed', 'devised', 'established', 'formed',
        'formulated', 'founded', 'generated', 'initiated', 'integrated', 'introduced', 'invented',
        'launched', 'originated', 'produced', 'shaped', 'staged', 'visualized', 'modified', 'revamped',
        'revised', 'updated', 'advocated', 'aided', 'assisted', 'cared', 'contributed', 'cooperated',
        'coordinated', 'ensured', 'furthered', 'guided', 'intervened', 'offered', 'referred',
        'rehabilitated', 'supplied', 'supported', 'volunteered', 'served', 'adapted', 'advised',
        'clarified', 'coached', 'counselled', 'demonstrated', 'educated', 'enabled',
        'encouraged', 'evaluated', 'explained', 'facilitated', 'familiarized', 'individualized',
        'instructed', 'mentored', 'modelled' ] 


        ab = text_main.lower()
        sentence = nltk.tokenize.sent_tokenize(ab)
        comp1 = check(sentence,analytical)
        
        try:
            comp1_count = len(comp1)
        except:
            comp1_count = 0
        comp2 = check(sentence,communication)
        try:
            comp2_count = len(comp2)
        except:
            comp2_count = 0
        
        comp3 = check(sentence,leadership)
        try:
            comp3_count = len(comp3)
        except:
            comp3_count = 0
        
        comp4 = check(sentence,teamwork)
        try:
            comp4_count = len(comp4)
        except:
            comp4_count = 0
        
        comp5 = check(sentence,initiative)
        try:
            comp5_count = len(comp5)
        except:
            comp5_count = 0
       
        
        
        
        match_dict = {'analytical' : comp1, 'communication': comp2, 'leadership': comp3, 'teamwork': comp4,
                    'initiative': comp5} 
        
        count_dict = {'analytical' : comp1_count, 'communication': comp2_count, 'leadership': comp3_count, 
                    'teamwork': comp4_count, 'initiative': comp5_count}


        count_competancies=[]
        for i in count_dict.keys():
            if(count_dict[i]!=0):
                count_competancies.append(i)
        sumaa=0
        for key in count_dict.keys():
            sumaa+=count_dict[key]

        nl=[]
        quant=0
        if checkfornos==1 or checkfornos2==1:
            quant=1
        elif checkfornos!=1 and checkfornos2!=1:
            nl=quan(text_main,aw1_list+pe1_list )
        if(nl[1]):
            quant=1
                
        
        ab = text_main.lower()
        sentence = nltk.tokenize.sent_tokenize(ab)

        
        
        session['bared'] = count_dict
        count_dict_dict={}
        stop_words = set(stopwords.words('english')) 
        filtered_sentence = [w for w in sentence if not w in stop_words] 
        for i in filtered_sentence:
            count_dict_dict[i]=filtered_sentence.count(i)

      
        if ed_date_format_list==1:
            pres-=5
      
        skillmatch=skillsMatch(text_main)

        namee=extract_name(text_main)
        empty_competency=""
        cot=0
        for i in match_dict.keys():
            cot=cot+len(match_dict[i])

        if(cot==0):
            empty_competency = "You might want to add few competencies in your resume as it's an efficient way to provide comprehensive proof that you are qualified for a certain job. "

       
       
        a_list = nltk.tokenize.sent_tokenize(text_main)

       
        hardskill = hardskills(a_list)
        phonenumber = phone1(text_main)
        emailid = email1(text_main)
        LinkedIn = linkedin1(text_main)
   
        job_description = session['data']
        job_description = job_description.lower()
        jd = nltk.tokenize.sent_tokenize(job_description)
        
        hardskill_jd = hardskills(jd)
   
        common_hs=list(set(hardskill).intersection(set(hardskill_jd)))
        matching_hs=[hardskill,hardskill_jd,common_hs]
        
        
        matching_ed=matching(edmatch(text_main),edmatch(job_description))

        a_l=edmatch(text_main)
        b_l=edmatch(session['data'])
        c_l=list(set(hardskill).intersection(set(hardskill_jd)))
        comp1_jd = check(jd,analytical)
        
        try:
            comp1_jd_count = len(comp1_jd)
        except:
            comp1_jd_count = 0
        comp2_jd = check(jd,communication)
        try:
            comp2_jd_count = len(comp2_jd)
        except:
            comp2_jd_count = 0
        
        comp3_jd = check(jd,leadership)
        try:
            comp3_jd_count = len(comp3_jd)
        except:
            comp3_jd_count = 0
        
        comp4_jd = check(jd,teamwork)
        try:
            comp4_jd_count = len(comp4_jd)
        except:
            comp4_jd_count = 0
        
        comp5_jd = check(jd,initiative)
        try:
            comp5_jd_count = len(comp5_jd)
        except:
            comp5_jd_count = 0

        match_dict_jd = {'analytical' : [comp1,comp1_jd], 'communication': [comp2,comp2_jd], 'leadership': [comp3,comp3_jd], 'teamwork': [comp4,comp4_jd],
                    'initiative': [comp5,comp5_jd]} 
        
        count_dict_jd = {'analytical' : comp1_jd_count, 'communication': comp2_jd_count, 'leadership': comp3_jd_count, 
                    'teamwork': comp4_jd_count, 'initiative': comp5_jd_count}

        
        s_list=[]
        for keys in match_dict.keys():
            for x in match_dict[keys]:
                s_list.append(x)
        s_list_jd=[]
        for keys in match_dict_jd.keys():
            try:
                for x in match_dict_jd[keys][1]:
                    s_list_jd.append(x)
            except:
                continue

        

        
        common_ss=list(set(s_list).intersection(set(s_list_jd)))
        ss_list=[s_list,s_list_jd,common_ss]
        try:

            ss_score=int(len(common_ss)/len(s_list_jd)*100)
            
        except:
            ss_score=0

        
        try:
            matcc=len(c_l)/len(matching_hs[1])*100
        except:
            matcc=0

        

        
        
        keys_chart = [k for k in count_dict]
    
        values_chart = [count_dict[k] for k in count_dict]
    
        values1_chart = [count_dict_jd[k] for k in count_dict_jd]


       
        
        
        return render_template('index36.html', results=sections, notr=user.count_used, ss_list=ss_list, ss_score=ss_score, matcc=int(matcc), jd_score = int(jd_score), c_l=c_l, matching_hs=matching_hs, phonenumber=phonenumber, emailid=emailid, linkedin=LinkedIn, typee=typee, pro_msg=pro_msg,edu_msg=edu_msg,matched_comment= rev,jd_msg=jd_msg,score= sections['Score'],email=email,education=edu,rud_mdg=sections['redundancy'],vol_msg=vol_msg,cert_msg=cert_msg,link_msg=link_msg,ach_msg = ach_msg,count_pass=co_pa,count_tense=co_ta,act_msg=act_msg,para=sections['paragraph'],depth=int(((ac+rd)/30*100)),pres=int(pres/25*100),impact=int(impact/45 *100), scor= (ac+rd+pres+impact), match_dict_jd=match_dict_jd, count_dict_jd=count_dict_jd, count_dict=count_dict, keys_chart=keys_chart, values_chart=values_chart, values1_chart=values1_chart )
           
    except Exception as e:
        print(e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return render_template('error_page.html')


@app.route('/jdservice',methods= ["GET",'POST'])
def jd_analyse1():
    ct=""
    if request.method == 'POST':
        session.pop('data', None)
        session['data'] = request.form['jd']
       
       
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No Selected File')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename= secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            return redirect (url_for('jd_file1',filename=filename))
    return render_template('jd1.html')



@app.route('/jdservice/<filename>')
def jd_file1(filename):
    try:
        

        f_name = os.path.join(app.config['UPLOAD_FOLDER'],filename)
        # return f_name
        global text_main,length,match,keyword
        file_name = f_name
        print(f_name)
        impact = 0
        pres =0
        text_main = ""
        edu_msg =0 
        vol_msg=0
        pro_msg=0
        jd_msg=""
        typee=0
        if(file_name[-3:]=="pdf"):
            
            jd_score=pdf(file_name)
            typee=0
            
        elif(file_name[-4:] == "docx"):
            
            jd_score=docx1(file_name)
            typee=1
 
            
        else:
            
            return render_template('unsupported.html')
        
        
        text_count=text_main.split(" ")
        word_count=len(text_count)
        liness=[]
        line=""
        line1=[]
        if(file_name[-4:] == "docx" ):
            for i in text_main:
                
                if(i!='\n'):
                    line+=i
                else:
                    liness.append(line)
                    line=""
            
            for line in liness:
                if len(line)!=0:
                    line1.append(line)
        elif(file_name[-3:]=="pdf"):
            liness=text_main.split("\\n")
    
                    
            
            for line in liness:
                if len(line)!=0:
                    line1.append(line)

        
        
        phone=re.findall(r"(?<!\d)\d{10}(?!\d)", text_main)
        email=re.findall(r"([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)",text_main)
        
        links= re.findall(r"(^(http\:\/\/|https\:\/\/)?([a-z0-9][a-z0-9\-]*\.)+[a-z0-9][a-z0-9\-]*)",text_main)
        mlink=[]
        for link in links:
            if 'facebook' in link:
                mlink.append(link)
            elif 'github' in link:
                mlink.append(link)
            elif 'linkedin' in link:
                mlink.append(link)
            else:
                links.remove(link)
        links=list(set(mlink))
        section=[]
        sections={}
        line2=[]
        titles=['education','Licensures', 'Professional Qualification', 'academic qualification', 'Educational Qualification', 'academia', 'education and professional development', 'academic credentials', 'educational summary', 'academic profile', 'Experience', 'work experience', 'Job Titles held', 'Position Description and purpose', 'Professional Experience', 'Professional Summary', 'Profile', 'Qualifications', 'Employment History', 'history', 'previous employment', 'organisational experience', 'employers', 'positions of responsibility','Position of Responsibilities', 'employment scan', 'past experience', 'organizational experience', 'career', 'experience and qualification summary', 'relevant experience', 'experience summary', 'career synopsis', 'career timeline', 'banking IT experience', 'AML & FCM Suite Experience', 'employment details', 'Skill','skills', 'Technical Skills', 'Soft Skills', 'Key Skills', 'Design Skills', 'Expertise', 'Abilities', 'Area of Expertise', 'Key attributes', 'Computer Skills', 'IT Skills', 'Technical Expertise', 'Technical Skills Set', 'Functional Skill Set', 'functional skills', 'strengths', 'areas of expertise', 'banking knowledge', 'Award', 'Honours and awards', 'Key achievements', 'Accomplishments', 'Highlights', 'Affiliations', 'Achievements', 'Extra Curricular activities and achievements', 'awards and recognition','awards/achievements', 'Certificate', 'Most proud of', 'Specialization', 'Certifications', 'Certification/training','Coursework','other credentials', 'professional accomplishments', 'certification & trainings', 'scholastics', 'professional credentials and certifications','Project','projects', 'Additional Activities', 'Activities', 'Major Tasks', 'Responsibilities', 'key accountabilities', 'Contributions', 'Personal Projects', 'Key Contributions', 'Strategic Planning and execution', 'Academic projects', 'Key projects', 'projects/trainings', 'key implementations','Volunteer', 'Volunteer Experience', 'Affiliations', 'Misc','Extra Curricular Activities', 'Community Service','EDUCATIONAL BACKGROUND','INTERNSHIPS EXPERIENCE','WINNING PORTFOLIO','AWARDS & RECOGNITIONS','CORE COMPETENCIES','PROJECTS ADMINISTERED','TECHNICAL SKILLS','CERTIFICATIONS','VOLUNTEERING','PERSONAL DOSSIER','Licensure', 'Professional Qualifications', 'academic qualifications', 'academics qualification', 'academics qualifications',  'Educational Qualifications', 'education and professional developments', 'academic credential', 'academics credential', 'academics credentials', 'educational summaries', 'academic profiles', 'academics profile','Experiences', 'work experiences', 'Position Descriptions and purpose', 'Positions Description and purpose', 'Positions Descriptions and purpose', 'Professional Experiences', 'Profiles', 'Qualification', 'Employment Histories', 'previous employments', 'organisational experiences', 'organizational experiences', 'organizational experience', 'employer', 'positions of responsibilities', 'position of responsibility', 'position of responsibilities', 'employment scans', 'past experiences', 'organizational experiences', 'organisational experience', 'organisational experiences', 'careers', 'experiences and qualifications summary', 'experience and qualifications summary', 'experiences and qualification summary', 'relevant experiences', 'career timelines', 'banking IT experiences', 'AML & FCM Suite Experiences', 'employment details', 'employment detail','Skills', 'Technical Skill', 'Soft Skill', 'Key Skill', 'Design Skill', 'Expertises', 'Ability', 'Areas of Expertises', 'Areas of Expertise', 'Area of Expertises', 'Key attribute', 'Computer Skill', 'IT Skill', 'Technical Expertises', 'Technical Skill Set', 'Technical Skill Sets', 'Functional Skills Set', 'Functional Skill Sets', 'Functional Skills Sets', 'functional skill', 'strength', 'area of expertise', 'area of expertises','Awards', 'Key achievement', 'Accomplishment', 'Highlight', 'Affiliation', 'Achievement', 'Extra Curricular activities and achievements',  'Extra Curricular activity and achievements',  'Extra Curricular activities and achievement',  'Extra Curricular activity and achievement', 'awards and recognitions',  'award and recognition',  'award and recognitions', 'Certificates', 'Specializations', 'Certification', 'Certifications/trainings', 'Certifications/training', 'Certification/trainings', 'other credential', 'professional accomplishment', 'certifications & trainings', 'certifications & training', 'certification & training', 'scholastic', 'professional credential and certification', 'professional credential and certifications', 'professional credentials and certification','Project', 'Additional Activity', 'Activity', 'Major Task', 'Responsibily', 'key accountability', 'Contribution', 'Personal Project', 'Key Contribution', 'Strategic Plannings and executions', 'Strategic Plannings and execution', 'Strategic Planning and executions', 'Academic project', 'Key project', 'project/training', 'projects/training', 'project/trainings', 'key implementation','Volunteer', 'Volunteer Experiences', 'Affiliation', 'Community Services' ]
        titles1=[x.lower() for x in titles]
        for i in line1:
            if i[-1]==" ":
                line2.append(i[:-1])
            else:
                line2.append(i)
        
        line1=line2
        temp = '\t'.join(titles1)
        for x in line1:
            
            global keyword
            if(x==line1[-1]):
            
                section.append(x)
                sections[keyword] = section
                keyword = x
                    
                section =[]
                break
            elif x.lower() not in temp:
                section.append(x)
               
            elif (len(x.split(" "))>=4):
                section.append(x)
                  
            
                
            else :
                if(len(section)!=0):
                    sections[keyword] = section
                    keyword = x
                    
                    section =[]
                else:
                    sections[keyword]=[]
                    keyword=x
                    section =[]
                    
        sections['phone']=list(set(phone))
        sections['links']=mlink
        if (len(mlink) != 0):
            impact+=5
        
        ed_list=['Education', 'Education Details','Licensures', 'Professional Qualification', 'academic qualification', 'Educational Qualification', 'academia', 'education and professional development', 'academic credentials', 'educational summary', 'academic profile','EDUCATIONAL BACKGROUND','Licensure', 'Professional Qualifications', 'academic qualifications', 'academics qualification', 'academics qualifications',  'Educational Qualifications', 'education and professional developments', 'academic credential', 'academics credential', 'academics credentials', 'educational summaries', 'academic profiles', 'academics profile']
        ex_list=['Experience', 'Experience Details','work experience', 'Job Titles held', 'Position Description and purpose', 'Professional Experience', 'Professional Summary', 'Profile', 'Qualifications', 'Employment History', 'history', 'previous employment', 'organisational experience', 'employers', 'positions of responsibility', 'employment scan','past experience', 'organizational experience', 'career', 'experience and qualification summary', 'relevant experience', 'experience summary', 'career synopsis', 'career timeline', 'banking IT experience', 'AML & FCM Suite Experience', 'employment details','INTERNSHIPS EXPERIENCE','Experiences', 'work experiences', 'Position Descriptions and purpose', 'Positions Description and purpose', 'Positions Descriptions and purpose', 'Professional Experiences', 'Profiles', 'Qualification', 'Employment Histories', 'previous employments', 'organisational experiences', 'organizational experiences', 'organizational experience', 'employer', 'positions of responsibilities', 'position of responsibility', 'position of responsibilities', 'employment scans', 'past experiences', 'organizational experiences', 'organisational experience', 'organisational experiences', 'careers', 'experiences and qualifications summary', 'experience and qualifications summary', 'experiences and qualification summary', 'relevant experiences', 'career timelines', 'banking IT experiences', 'AML & FCM Suite Experiences', 'employment details', 'employment detail', 'career progression']
        sk_list=['Skill', 'Technical Skills', 'Soft Skills', 'Key Skills', 'Design Skills', 'Expertise', 'Abilities', 'Area of Expertise', 'Key attributes', 'Computer Skills', 'IT Skills', 'Technical Expertise', 'Technical Skills Set', 'Functional Skill Set', 'functional skills', 'strengths', 'areas of expertise', 'banking knowledge','WINNING PORTFOLIO','CORE COMPETENCIES','TECHNICAL SKILLS','skills','Skills', 'Technical Skill', 'Soft Skill', 'Key Skill', 'Design Skill', 'Expertises', 'Ability', 'Areas of Expertises', 'Areas of Expertise', 'Area of Expertises', 'Key attribute', 'Computer Skill', 'IT Skill', 'Technical Expertises', 'Technical Skill Set', 'Technical Skill Sets', 'Functional Skills Set', 'Functional Skill Sets', 'Functional Skills Sets', 'functional skill', 'strength', 'area of expertise', 'area of expertises']
        aw_list=['Award' , 'Achievement Details','Honours and awards', 'Key achievements', 'Accomplishments', 'Highlights', 'Affiliations', 'Achievements', 'Extra Curricular activities and achievements', 'awards and recognition','AWARDS & RECOGNITIONS','awards','achievements','Awards', 'Key achievement', 'Accomplishment', 'Highlight', 'Affiliation', 'Achievement', 'Extra Curricular activities and achievements',  'Extra Curricular activity and achievements',  'Extra Curricular activities and achievement',  'Extra Curricular activity and achievement', 'awards and recognitions',  'award and recognition',  'award and recognitions']
        ce_list=['Certificate', 'Certification Details','Most proud of', 'Specialization', 'Certifications', 'Certification/training', 'other credentials', 'professional accomplishments', 'certification & trainings', 'scholastics', 'professional credentials and certifications','CERTIFICATION','coursework', 'competencies', 'Certificates', 'Specializations', 'Certification', 'Certifications/trainings', 'Certifications/training', 'Certification/trainings', 'other credential', 'professional accomplishment', 'certifications & trainings', 'certifications & training', 'certification & training', 'scholastic', 'professional credential and certification', 'professional credential and certifications', 'professional credentials and certification',  'key accountability', 'Contribution', 'Personal Project', 'Key Contribution', 'Strategic Plannings and executions', 'Strategic Plannings and execution', 'Strategic Planning and executions',]
        pe_list=['Project', 'Project Details','Additional Activities', 'Activities', 'Major Tasks', 'Responsibilities', 'key accountabilities', 'Contributions', 'Personal Projects', 'Key Contributions', 'Strategic Planning and execution', 'Academic projects', 'Key projects', 'projects/trainings', 'key implementations','PROJECTS ADMINISTERED','projects','Project', 'Additional Activity', 'Activity', 'Major Task', 'Responsibily', 'key accountability', 'Contribution', 'Personal Project', 'Key Contribution', 'Strategic Plannings and executions', 'Strategic Plannings and execution', 'Strategic Planning and executions', 'Academic project', 'Key project', 'project/training', 'projects/training', 'project/trainings', 'key implementation','Additional Activity', 'Activity', 'Major Task', 'Responsibily', 'Academic project', 'Key project', 'project/training', 'projects/training', 'project/trainings', 'key implementation']
        vo_list=['Volunteer', 'Volunteer Details','Volunteer Experience', 'Affiliations', 'Misc', 'Community Service','VOLUNTEERING','extra curricular activities','EXTRA-CURRICULAR INVOLVEMENT','Volunteer', 'Volunteer Experiences', 'Affiliation', 'Community Services']
        ed1_list=[x.lower() for x in ed_list]
        temp_ed= '\t'.join(ed1_list)
        ex1_list=[x.lower() for x in ex_list]
        temp_ex='\t'.join(ex1_list)
        sk1_list=[x.lower() for x in sk_list]
        temp_sk='\t'.join(sk1_list)
        aw1_list=[x.lower() for x in aw_list]
        temp_aw='\t'.join(aw1_list)
        ce1_list=[x.lower() for x in ce_list]
        temp_ce='\t'.join(ce1_list)
        pe1_list=[x.lower() for x in pe_list]
        temp_pe='\t'.join(pe1_list)
        vo1_list=[x.lower() for x in vo_list]
        temp_vol='\t'.join(vo1_list)
        
        score = 0
        msg = []
        edu=0
        ed=0
        ex=0
        sk=0
        aw=0
        ce=0
        pe=0
        vo=0
        ed_date_format_list=[0,0]
        ex_date_format_list=[0,0]
        ach_msg = 0 #achievement variable message
        cert_msg = 0 #certification message flag
        sections['edu_year']=""
        sections['exp_year']=""
        sections['paragraph']=0
        checkfornos=0
        alphanum=""
        checkfornos2=0
        
        for key in sections.keys():
            
            for i in ed1_list:
                if(i in key.lower() and ed==0 and key.lower()!='n'):
                    score +=10
                    pres+=10
                    edu = 1
                    ed=1
                    edu_msg =1
                    ed_date_format_list=date_format(sections[key])
                    if ed_date_format_list>0:
                        score-=10
                        pres-=10
                    
                    sections['edu_year']=extract(sections[key])
                    sections['paragraph']+=paragraph_check(sections[key])
                    
                    msg.append("Education Section is Present")
                    break
                
            for i in ex1_list:    
                if(i in key.lower() and ex==0 and key.lower()!='n'):
                    score +=20
                    ex=1
                    sections['exp_year']=extract(sections[key])
                    ex_date_format_list=date_format(sections[key])
                    impact+=20
                    sections['paragraph']+=paragraph_check(sections[key])
                            
                    msg.append("Experience Section is Present")
                    
                    break
                
            for i in sk1_list:
                if(i in key.lower() and sk==0 and key.lower()!='n'):
                    score +=20
                    sk=1
                    msg.append("Skills Section is Present")
                    sections['paragraph']+=paragraph_check(sections[key])
                    break
            for i in aw1_list:    
                if(i in key.lower() and aw==0 and key.lower()!='n'):
                    score +=5
                    impact+=5
                    aw=1
                    ach_msg = 1
                    alpha_num = ['one','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen','twenty','thirty','fourty','fifty','sixty','seventy','eighty','ninety','hundred','thousand']
                    checkfornos = checknos(sections[key],alpha_num)
                    sections['paragraph']+=paragraph_check(sections[key])
                    msg.append("Awards/Achievement Section is Present")
                    
                    break
            for i in vo1_list:    
                if(i in key.lower() and vo==0 and key.lower()!='n'):
                    pres+=5
                    score +=5
                    vo=1
                    vol_msg =1
                    msg.append("Volunteering Section is Present")
                    
                    break
            for i in ce1_list:    
                if(i in key.lower() and ce==0 and key.lower()!='n'):
                    impact+=5
                    score +=10
                    cert_msg=1
                    ce=1
                    msg.append("Certificate Section is Present")
                    
                    break
            for i in pe1_list:    
                if(i in key.lower() and pe==0 and key.lower()!='n'):
                    pres+=10
                    pe=1
                    score +=10
                    pro_msg=1
                    sections['paragraph']+=paragraph_check(sections[key])
                    alpha_num = ['one','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen','twenty','thirty','fourty','fifty','sixty','seventy','eighty','ninety','hundred','thousand']
                    checkfornos2 = checknos(sections[key],alpha_num)
                    msg.append("Projects Section is Present")
                   
                    break
        list_present=[ed,ex,sk,aw,ce,pe,vo]
        fed=0
        fex=0
        fsk=0
        faw=0
        fce=0
        fpe=0
        fvo=0
        sect=[]
        
        
        
        for i in range(len(list_present)):
            if i ==0 and list_present[i]==0:
                
                for ik in ed1_list:
                    if ik in text_main.lower():
                        fed=1
                score+=5
            if i ==1 and list_present[i]==0:
                
                for ik in ex1_list:
                    if ik in text_main.lower():
                        fex=1
                score+=10
            if i ==2 and list_present[i]==0:
                
                for ik in sk1_list:
                    if ik in text_main.lower():
                        fsk=1
                score+=10
            if i ==3 and list_present[i]==0:
                
                for ik in aw1_list:
                    if ik in text_main.lower():
                        faw=1
                score+=2
            if i ==4 and list_present[i]==0:
                
                for ik in ce1_list:
                    if ik in text_main.lower():
                        fce=1
                score+=5
            if i ==5 and list_present[i]==0:
                
                for ik in pe1_list:
                    if ik in text_main.lower():
                        fpe=1
                score+=5
            if i ==6 and list_present[i]==0:
                
                for ik in vo1_list:
                    if ik in text_main.lower():
                        fvo=1
                score+=2
        
        improper_format=[]
        if(fed==1 and ed==0):
            improper_format.append('education')
        if(fex==1 and ex==0):
            improper_format.append('experience')
        if(fsk==1 and sk==0):
            improper_format.append('skill')
        if(faw==1 and aw==0):
            improper_format.append('achievement')
        if(fce==1 and ce==0):
            improper_format.append('certification')
        if(fpe==1 and pe==0):
            improper_format.append('project')
        if(fvo==1 and vo==0):
            improper_format.append('volunteer')
        
            
        
        sections['Message']=msg
        
        rev=""
        
                
        stop_words = set(stopwords.words('english')) 
        d=""
        skillsets=0
        filtered_sentence=[]
        
    
        for i in sections.keys():
            if(i.lower()=="work experience"):
                score +=5
            if(i.lower()=="core competencies"):
                score +=5            
            if 'skill' in i.lower():
                skillsets=len(sections[i])
                for j in sections[i]:
                     
                    d=d+" "+j
                d = word_tokenize(d)
                 
                for w in d: 
                    if w not in stop_words: 
                        if(len(w)>3):
                            filtered_sentence.append(w)
    
        sections['SkCount']=skillsets
        
        sections['linkedin']=Find(text_main)
        ck=sections['linkedin']
        link_msg=1
        if(len(ck) == 0):
            link_msg=0
        
        ac=0
        rd=0
        action_list=[]
        act_msg=0
        if actionwords(text_main)[0] > 5 :
            act_msg =1
            action_list=actionwords(text_main)[1]
            ac=10
            sections['action_word']="Your resume contains Action Verbs! Strong, unique action verbs show hiring managers that you have held different roles and skill sets. They also help your accomplishments stand out and make them more impactful."
        elif actionwords(text_main)[0]<=5:
            act_msg =0
            sections['action_word']="Your resume doesnt contain much Action Verbs! Strong, unique action verbs show hiring managers that you have held different roles and skill sets. They also help your accomplishments stand out and make them more impactful. "
        elif actionwords(text_main)[0]==0:
            
            act_msg =0
            sections['action_word']="Your resume doesnt contain any Action Verbs! Strong, unique action verbs show hiring managers that you have held different roles and skill sets. They also help your accomplishments stand out and make them more impactful. "
        fct_msg=0
        filler_list=[]
        if fillerwords(text_main)[0] > 1 :
            fct_msg =1
            filler_list=fillerwords(text_main)[1]
            
           
        
        elif fillerwords(text_main)[0]==0:
            
            fct_msg =0
            
        
        if redundancy(text_main) > 10:
            rd=5
            sections['redundancy']="1"
        elif redundancy(text_main)<=10:
            sections['redundancy']="0"
            
        
        
        sections['match']=match
        
        if(score == 100):
            rev="the score looks perfect but to get a more accurate comparison with the job you are looking for try analysing by adding Job Description"
        elif(score < 60):
            rev="this score suggests there is a lot of room for improvement. But don't worry! We have highlighted a number of quick fixes you can make to improve your resume's score and your success rate. Try adding more skills or experience into your resume to increase your resume score to 80% or above."
        else:
            rev="your score looks good however we have highlighted a number of quick fixes you can make to improve your resume's score. Try adding more skills or experience into your resume to increase your resume score."
        sections["Review"]=rev
        sections["Length"]=length
        sections["WordCount"]=word_count
        if sections["WordCount"] <= 600 and sections["WordCount"] > 1:
            score += 5
            sections['Message'].append("Word Count of the Resume is Optimal")
        else:
            sections['Message'].append("Word Count should be less than 600")

        if sections["Length"] and sections["WordCount"] > 1:
            score += 5
            sections['Message'].append("Length of Resume is Optimal")
        else:
            sections['Message'].append("Length of Resume should not exceed 2 pages")
        sections['Score']=round(((score/100)*100),2) #calculating score out of overall score.
        if(sections['Score'] >=90 and sections['Score'] <100):
            sections["Review"]="The Resume is correctly Parsed and Optimal. There may be some room for Improvement"
        if(sections['Score'] >=75 and sections['Score']<90):
            sections["Review"]="The Resume may be Correctly Parsed and Optimal. It is advised to pass DOCX Format in ATS Checker. There is certainly Some Room For Improvement"        
        count_passive1=[]
        count_passive=0
        co_pa=0
        for i in line1:
            if(is_passive(re.sub(r'[^\x00-\x7f]',r'', i))):
                count_passive += 1
                count_passive1.append(re.sub(r'[^\x00-\x7f]',r'', i))
        
                
        if(count_passive > 0):
            co_pa= 1
        elif(len(line1)==0):
            co_pa= 1
            
        else:
            co_pa=0
            ac += 5
        
        count_tense1=[]
        co_ta=0
        count_tenses=0
        for i in line1:
            if(tenses_res(re.sub(r'[^\x00-\x7f]',r'', i))):
                count_tenses += 1
                count_tense1.append(re.sub(r'[^\x00-\x7f]',r'', i))
                
        if(count_tenses >= 5):
            co_ta= 1
        elif(len(line1)==0):
            co_ta= 1
            
        else:
            co_ta=0
            ac += 5
            
        if(len(line1)==0):
            sections['paragraph']=0 
        elif sections['paragraph'] <= 2:
            ac += 5
            
        
        
        
        cont=[]
        contact_all=contact_details(text_main)
        for elem in contact_all:
            if elem:
                if len(contact_all[0]) == 0:
                    cont.append('email')
                if len(contact_all[1]) == 0:
                    cont.append('phone')
                if len(contact_all[2]) == 0:
                    cont.append('linkedin')
                if len(contact_all[0]) !=0 and len(contact_all[1])!=0 and len(contact_all[2])!=0:
                    cont.append('all')
                    break

            if elem not in contact_all:
                cont.append("none")
            
        

        analytical =['Research', 'collected', 'conducted', 'defined', 'detected', 'discovered', 'examined',
        'experimented', 'explored', 'extracted', 'found', 'gathered', 'identified', 'inquired', 'inspected',
        'investigated', 'located', 'measured', 'modelled', 'observed', 'researched', 'reviewed', 'searched',
        'studied',' surveyed', 'tested', 'tracked', 'Analyse', 'Evaluate', 'analysed', 'assessed', 'calculated',
        'catalogued', 'categorized', 'clarified', 'classified', 'compared', 'compiled', 'critiqued', 
        'derived', 'determined', 'diagnosed', 'estimated', 'evaluated', 'formulated', 'interpreted',
        'prescribed', 'organized', 'rated', 'recommended', 'reported', 'summarized', 'systematized', 
        'tabulated', 'assembled', 'built', 'coded', 'computed', 'constructed', 'converted', 'debugged',
        'designed', 'engineered', 'fabricated', 'installed', 'maintained', 'operated',
        'printed', 'programmed', 'proved', 'rectified', 'regulated', 'repaired', 'resolved',
        'restored', 'specified', 'standardized', 'upgraded', 'adjusted', 'allocated', 'appraised',
        'audited', 'balanced', 'budgeted', 'conserved', 'controlled', 'disbursed', 'figured', 'financed',
        'forecasted', 'netted', 'projected', 'reconciled']

        communication = ['addressed', 'articulated', 'authored', 'briefed', 'clarified', 
        'conveyed', 'composed', 'condensed', 'corresponded', 'debated', 'delivered', 'described',
        'discussed', 'drafted', 'edited', 'expressed', 'formulated', 'informed', 'instructed',
        'interacted', 'interpreted', 'lectured', 'negotiated', 'notified', 'outlined', 'reconciled',
        'reinforced', 'reported', 'presented', 'proposed', 'specified', 'spoke', 'translated',
        'wrote', 'advertised', 'influenced', 'marketed', 'solicited', 'contacted', 'convinced',
        'represented', 'persuaded', 'motivated',' communicated', 'elicited', 
        'recruited', 'promoted', 'publicized', 'enlisted', 'arbitrated', 'consulted', 'conferred',
        'interviewed', 'mediated', 'moderated', 'listened', 'responded', 'suggested']

        leadership = ['administered', 'appointed', 'approved', 'assigned', 'authorized', 'chaired',
        'conducted', 'contracted', 'controlled', 'coordinated', 'decided', 'delegated', 'directed',
        'developed', 'enforced', 'ensured', 'evaluated', 'executed', 'headed', 'hired', 'hosted', 
        'implemented', 'instituted', 'led', 'managed', 'overhauled', 'oversaw', 'prioritized', 
        'recruited', 'represented', 'strategized', 'supervised', 'trained', 'anticipated', 'arranged',
        'contacted', 'convened', 'logged', 'obtained', 'ordered', 'planned',
        'prepared', 'processed', 'purchased', 'recorded', 'registered', 'reserved', 'scheduled', 
        'verified', 'consolidated', 'distributed', 'eliminated', 'filed', 'grouped', 'incorporated',
        'merged', 'monitored', 'organized', 'regulated', 'reviewed', 'routed', 'standardized',
        'structured', 'submitted', 'systematized', 'updated']

        teamwork = ['aided', 'answered', 'arranged', 'catalogued', 'categorized', 'collated', 'collected',
        'coordinated', 'distributed', 'emailed', 'ensured', 'expedited', 'explained', 'filed', 'greeted',
        'handled', 'informed', 'implemented', 'maintained', 'offered', 'ordered', 'organized', 'performed',
        'prepared', 'processed', 'provided', 'purchased', 'recorded', 'received', 'resolved', 'scheduled', 'served',
        'supported', 'tabulated', 'collaborated', 'consulted', 'cooperated', 'liaised', 'reached', 
        'out']

        initiative = ['authored', 'began', 'built', 'changed', 'combined', 'conceived', 'constructed',
        'created', 'customized', 'designed', 'developed', 'devised', 'established', 'formed',
        'formulated', 'founded', 'generated', 'initiated', 'integrated', 'introduced', 'invented',
        'launched', 'originated', 'produced', 'shaped', 'staged', 'visualized', 'modified', 'revamped',
        'revised', 'updated', 'advocated', 'aided', 'assisted', 'cared', 'contributed', 'cooperated',
        'coordinated', 'ensured', 'furthered', 'guided', 'intervened', 'offered', 'referred',
        'rehabilitated', 'supplied', 'supported', 'volunteered', 'served', 'adapted', 'advised',
        'clarified', 'coached', 'counselled', 'demonstrated', 'educated', 'enabled',
        'encouraged', 'evaluated', 'explained', 'facilitated', 'familiarized', 'individualized',
        'instructed', 'mentored', 'modelled' ] 


        ab = text_main.lower()
        sentence = nltk.tokenize.sent_tokenize(ab)
        comp1 = check(sentence,analytical)
        
        try:
            comp1_count = len(comp1)
        except:
            comp1_count = 0
        comp2 = check(sentence,communication)
        try:
            comp2_count = len(comp2)
        except:
            comp2_count = 0
        
        comp3 = check(sentence,leadership)
        try:
            comp3_count = len(comp3)
        except:
            comp3_count = 0
        
        comp4 = check(sentence,teamwork)
        try:
            comp4_count = len(comp4)
        except:
            comp4_count = 0
        
        comp5 = check(sentence,initiative)
        try:
            comp5_count = len(comp5)
        except:
            comp5_count = 0
       
        
        
        
        match_dict = {'analytical' : comp1, 'communication': comp2, 'leadership': comp3, 'teamwork': comp4,
                    'initiative': comp5} 
        
        count_dict = {'analytical' : comp1_count, 'communication': comp2_count, 'leadership': comp3_count, 
                    'teamwork': comp4_count, 'initiative': comp5_count}


        count_competancies=[]
        for i in count_dict.keys():
            if(count_dict[i]!=0):
                count_competancies.append(i)
        sumaa=0
        for key in count_dict.keys():
            sumaa+=count_dict[key]

        nl=[]
        quant=0
        if checkfornos==1 or checkfornos2==1:
            quant=1
        elif checkfornos!=1 and checkfornos2!=1:
            nl=quan(text_main,aw1_list+pe1_list )
        if(nl[1]):
            quant=1
                
        
        ab = text_main.lower()
        sentence = nltk.tokenize.sent_tokenize(ab)

        
        
        session['bared'] = count_dict
        count_dict_dict={}
        stop_words = set(stopwords.words('english')) 
        filtered_sentence = [w for w in sentence if not w in stop_words] 
        for i in filtered_sentence:
            count_dict_dict[i]=filtered_sentence.count(i)

      
        if ed_date_format_list==1:
            pres-=5
      
        skillmatch=skillsMatch(text_main)

        namee=extract_name(text_main)
        empty_competency=""
        cot=0
        for i in match_dict.keys():
            cot=cot+len(match_dict[i])

        if(cot==0):
            empty_competency = "You might want to add few competencies in your resume as it's an efficient way to provide comprehensive proof that you are qualified for a certain job. "

       
       
        a_list = nltk.tokenize.sent_tokenize(text_main)

       
        hardskill = hardskills(a_list)
        phonenumber = phone1(text_main)
        emailid = email1(text_main)
        LinkedIn = linkedin1(text_main)
   
        job_description = session['data']
        job_description = job_description.lower()
        jd = nltk.tokenize.sent_tokenize(job_description)
        
        hardskill_jd = hardskills(jd)
   
        common_hs=list(set(hardskill).intersection(set(hardskill_jd)))
        matching_hs=[hardskill,hardskill_jd,common_hs]
        
        
        matching_ed=matching(edmatch(text_main),edmatch(job_description))

        a_l=edmatch(text_main)
        b_l=edmatch(session['data'])
        c_l=list(set(hardskill).intersection(set(hardskill_jd)))
        comp1_jd = check(jd,analytical)
        
        try:
            comp1_jd_count = len(comp1_jd)
        except:
            comp1_jd_count = 0
        comp2_jd = check(jd,communication)
        try:
            comp2_jd_count = len(comp2_jd)
        except:
            comp2_jd_count = 0
        
        comp3_jd = check(jd,leadership)
        try:
            comp3_jd_count = len(comp3_jd)
        except:
            comp3_jd_count = 0
        
        comp4_jd = check(jd,teamwork)
        try:
            comp4_jd_count = len(comp4_jd)
        except:
            comp4_jd_count = 0
        
        comp5_jd = check(jd,initiative)
        try:
            comp5_jd_count = len(comp5_jd)
        except:
            comp5_jd_count = 0

        match_dict_jd = {'analytical' : [comp1,comp1_jd], 'communication': [comp2,comp2_jd], 'leadership': [comp3,comp3_jd], 'teamwork': [comp4,comp4_jd],
                    'initiative': [comp5,comp5_jd]} 
        
        count_dict_jd = {'analytical' : comp1_jd_count, 'communication': comp2_jd_count, 'leadership': comp3_jd_count, 
                    'teamwork': comp4_jd_count, 'initiative': comp5_jd_count}

        
        s_list=[]
        for keys in match_dict.keys():
            for x in match_dict[keys]:
                s_list.append(x)
        s_list_jd=[]
        for keys in match_dict_jd.keys():
            try:
                for x in match_dict_jd[keys][1]:
                    s_list_jd.append(x)
            except:
                continue

        

        
        common_ss=list(set(s_list).intersection(set(s_list_jd)))
        ss_list=[s_list,s_list_jd,common_ss]
        try:

            ss_score=int(len(common_ss)/len(s_list_jd)*100)
            
        except:
            ss_score=0

        
        try:
            matcc=len(c_l)/len(matching_hs[1])*100
        except:
            matcc=0

        

        
        
        keys_chart = [k for k in count_dict]
    
        values_chart = [count_dict[k] for k in count_dict]
    
        values1_chart = [count_dict_jd[k] for k in count_dict_jd]


       
        
        
        return render_template('index34.html', results=sections, ss_list=ss_list, ss_score=ss_score, matcc=int(matcc), jd_score = int(jd_score), c_l=c_l, matching_hs=matching_hs, phonenumber=phonenumber, emailid=emailid, linkedin=LinkedIn, typee=typee, pro_msg=pro_msg,edu_msg=edu_msg,matched_comment= rev,jd_msg=jd_msg,score= sections['Score'],email=email,education=edu,rud_mdg=sections['redundancy'],vol_msg=vol_msg,cert_msg=cert_msg,link_msg=link_msg,ach_msg = ach_msg,count_pass=co_pa,count_tense=co_ta,act_msg=act_msg,para=sections['paragraph'],depth=int(((ac+rd)/30*100)),pres=int(pres/25*100),impact=int(impact/45 *100), scor= (ac+rd+pres+impact), match_dict_jd=match_dict_jd, count_dict_jd=count_dict_jd, count_dict=count_dict, keys_chart=keys_chart, values_chart=values_chart, values1_chart=values1_chart )
           
    except Exception as e:
        print(e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return render_template('error_page.html')


@app.route('/about',methods= ["GET",'POST'])
def about():
    return render_template('about.html')

@app.route('/admin_resume_audit_confidential_link_dont_disclose_verify')
def admin1():
    return render_template("login-admin.html")

@app.route('/admin_resume_audit_confidential_link_dont_disclose', methods=['POST'])
def admin():
    name=request.form.get('usrname')
    password=request.form.get('pass')
    if name == "admin" and password=="admin":
        return render_template("admin_content.html")
    else:
        flash('Wrong Username or Password entered. Please Contact Admin')
        return render_template('login-admin.html')

@app.route('/submit', methods=['POST'])
def admin2():
    email=request.form.get('email')
    user=User.query.filter_by(email=email).first()
    if user:
        user.status="true"
        db.session.commit()
        flash("Email Activated Successfully")
        return render_template("admin_content.html")
    else:
        flash('User Doesnot exist')
        return render_template('admit_content.html')


    #return render_template("login-admin.html")
@app.route('/hi',methods= ["GET",'POST'])

def hi():
    return render_template('unsupported.html')

@app.route('/blogs',methods= ["GET",'POST'])
@login_required
def blogs():
    return render_template('blog.html')

@app.route('/blogdet1',methods= ["GET",'POST'])
@login_required
def blogdet1():
    return render_template('blog1.html')


@app.route('/blogdet2',methods= ["GET",'POST'])
@login_required
def blogdet2():
    return render_template('blog2.html')    

@app.route('/blogdet3',methods= ["GET",'POST'])
@login_required
def blogdet3():
    return render_template('blog3.html')
    

@app.route('/contact',methods= ["GET",'POST'])
def contact():
    return render_template('contact.html')




@app.route('/download')
def downloadFile ():
    #For windows you need to use drive name [ex: F:/Example.pdf]
    path = "wheel.xlsx"
    return send_file(path, as_attachment=True)

@app.route('/wheel1')
@login_required
def swot1():
    return render_template('swot.html')

@app.route('/swotdig')
@login_required
def swotdig():
    return render_template('swotdig.html')

@app.route('/reset_pass')
def respass():
    return render_template('forgetpass.html')


@app.route('/opt_verification', methods=['POST'])
def otpver():
    email=request.form.get('email')
    email1=request.form.get('email-confirm')
    range_start=""
    range_end=""
    number=""
    if email==email1:
        user = User.query.filter_by(email=email).first()
        if not user: 
            flash('Please check your login details and try again.')
            return render_template("forgetpass.html")
        else:

            range_start = 10**(7)
            range_end = (10**8)-1
            number=randint(range_start, range_end)
            message = Mail(
                from_email='aryasekharbandopadhyay@gmail.com',
                to_emails=email,
                subject='OTP for Password Reset',
                html_content='<strong>Your Otp is </strong>'+str(number))

            sg = SendGridAPIClient('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')
            response = sg.send(message)
            print(response)
            session['number']=number
            session['email']=email
            return render_template('otp_enter_page.html')

@app.route('/opt_check', methods=['POST'])
def otpver1():
    otp=request.form.get('otp')
    otp1=request.form.get('otp-confirm')
    if otp==otp1 and otp==str(session['number']):
        return render_template('respas.html')

    else:
        flash('Wrong OTP entered')
        return render_template('otp_enter_page.html')

@app.route('/pass_set', methods=['POST'])
def passet():
    pass1=request.form.get('pass')
    pass2=request.form.get('pass-confirm')
    if pass1==pass2:
        user = User.query.filter_by(email=session['email']).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
        user.password=generate_password_hash(pass1, method='sha256')
        db.session.commit()
        flash('Password set successfully')
        return render_template("login.html")


    
#Routes end here



#Functions Start Here


#Function to parse docx file
def docx1(name):
    global text_main,length
    resume= docx2txt.process(name)
       
    jd=session['data']
    
    res = len(resume.split())
    page = math.ceil(res/700)
    length = page
    
    
        
    text =[resume, jd]
        
    text_main = resume
    kk = analyser(text)
    return kk
    

#Function to parse pdf file
def pdf(name):
    global text_main,length
    c=repr(extract_text(name))
        
        
    jd= session['data']  
        
    text =[c, jd]
        
    pdf = PdfFileReader(open(name,'rb'))
    page = pdf.getNumPages()
    length = page
    
    
    
    kk = analyser(text)
    text_main = c
    return kk
        
    

#Optional Function to analyze
def analyser(text):
    cv =CountVectorizer()
    count_matrix = cv.fit_transform(text)
    matched= cosine_similarity(count_matrix)[0][1]*100
    matched= round(matched,2)
    doc1 = nlp(text[0])
    doc2 = nlp(text[1])
    sim = doc1.similarity(doc2)*100
    sim= round(sim,1)
    
    if(sim > 80):
        sim=sim*0.9

    l = sim
    return l


#Function to find url
def Find(string): 
    regex = r"(?:https?:)?\/\/(?:[\w]+\.)?linkedin\.com\/in\/(?P<permalink>[\w\-\_À-ÿ%]+)\/?"
    url = re.findall(regex,string)
    return url

#Function to find action words
def actionwords(string):
    
    No_of_actionVerbs=[]
    test_list = ['accelerated', 'achieved', 'attained', 'completed', 'conceived', 'convinced',
             'discovered', 'doubled', 'effected', 'eliminated', 'expanded', 'expedited', 
             'founded', 'improved', 'increased', 'initiated', 'innovated', 'introduced', 
             'invented', 'launched', 'mastered', 'overcame', 'overhauled', 'pioneered', 
             'reduced', 'resolved', 'revitalized', 'spearheaded', 'strengthened', 
             'transformed', 'upgraded', 'tripled', 'addressed', 'advised', 'arranged', 
             'authored', 'co-authored', 'co-ordinated', 'communicated', 'corresponded', 
             'counselled', 'developed', 'demonstrated', 'directed', 'drafted', 'enlisted',
             'facilitated', 'formulated', 'guided', 'influenced', 'interpreted',
             'interviewed', 'instructed', 'lectured', 'liased', 'mediated', 
             'moderated', 'motivated', 'negotiated', 'persuaded', 'presented', 'promoted', 
             'proposed', 'publicized', 'recommended', 'reconciled', 'recruited', 
             'resolved', 'taught', 'trained', 'translated', 'composed','conceived','created',
             'designed', 'developed', 'devised', 'established', 'founded', 'generated', 
             'implemented', 'initiated', 'instituted', 'introduced', 'launched','opened',
             'originated','pioneered', 'planned', 'prepared', 'produced','promoted', 
             'started', 'released', 'administered', 'analyzed', 'assigned', 'chaired', 
             'consolidated', 'contracted', 'co-ordinated', 'delegated', 'developed',
             'directed', 'evaluated', 'executed', 'organized', 'planned', 'prioritized',
             'produced', 'recommended', 'reorganized', 'reviewed', 'scheduled', 'supervised', 
             'managed', 'guided', 'advised', 'coached', 'conducted', 'directed', 'guided',
             'demonstrated', 'illustrated','managed', 'organized', 'performed', 
             'presented', 'taught', 'trained', 'mentored', 'spearheaded', 'authored', 
             'accelerated', 'achieved', 'allocated', 'completed', 'awarded', 'persuaded',
             'revamped', 'influenced', 'assessed', 'clarified', 'counseled', 'diagnosed',
             'educated', 'facilitated', 'familiarized', 'motivated', 'referred', 
             'rehabilitated', 'reinforced', 'represented', 'moderated', 'verified', 
             'adapted', 'coordinated', 'developed', 'enabled', 'encouraged', 'evaluated',
             'explained', 'informed', 'instructed', 'lectured', 'stimulated', 'analyzed',
             'assessed', 'classified', 'collated', 'defined', 'devised', 'established', 
             'evaluated', 'forecasted', 'identified', 'interviewed', 'investigated', 
             'researched', 'tested', 'traced', 'designed', 'interpreted', 'verified', 
             'uncovered', 'clarified', 'collected', 'critiqued', 'diagnosed', 'examined',
             'extracted', 'inspected', 'inspired', 'organized', 'reviewed', 'summarized', 
             'surveyed', 'systemized', 'arranged', 'budgeted', 'composed', 'conceived', 
             'conducted', 'controlled', 'co-ordinated', 'eliminated', 'improved', 'investigated', 
             'itemised', 'modernised', 'operated', 'organised', 'planned', 'prepared', 'processed', 
             'produced', 'redesigned', 'reduced', 'refined', 'researched', 'resolved', 'reviewed',
             'revised', 'scheduled', 'simplified', 'solved', 'streamlined', 'transformed', 
             'examined', 'revamped', 'combined', 'consolidated', 'converted', 'cut', 'decreased', 
             'developed', 'devised', 'doubled', 'tripled', 'eliminated', 'expanded', 'improved', 
             'increased', 'innovated', 'minimised', 'modernised', 'recommended', 'redesigned', 
             'reduced', 'refined', 'reorganised', 'resolved', 'restructured', 'revised', 'saved', 
             'serviced', 'simplified', 'solved', 'streamlined', 'strengthened', 'transformed', 
             'trimmed', 'unified', 'widened', 'broadened', 'revamped', 'administered', 'allocated', 
             'analyzed', 'appraised', 'audited', 'balanced', 'budgeted', 'calculated', 'computed', 'developed', 
             'managed', 'planned', 'projected', 'researched', 'restructured', 'modelled', 'acted',
             'conceptualized', 'created', 'customized', 'designed', 'developed', 'directed', 'redesigned',
             'established', 'fashioned', 'illustrated', 'instituted', 'integrated', 'performed', 'planned', 
             'proved', 'revised', 'revitalized', 'set up', 'shaped', 'streamlined', 'structured', 'tabulated',
             'validated', 'approved', 'arranged', 'catalogued', 'classified', 'collected', 
             'compiled', 'dispatched', 'executed', 'generated', 'implemented', 'inspected',
             'monitored', 'operated', 'ordered', 'organized', 'prepared', 'processed', 'purchased', 
             'recorded', 'retrieved', 'screened', 'specified', 'systematized']
    test_string=string.lower()
    res = [ele for ele in test_list if(ele in test_string)]
    No_of_actionVerbs.append(len(res))
    No_of_actionVerbs.append(res)
    return(No_of_actionVerbs)


#Function to find filler words
def fillerwords(string):
    No_of_fillerwords=[]
    test_list = ['capable','scalable', 'hard-work', 'hard work', 'problem-solve', 'creative', 'problem solve', 'innovative','motivated', 'skillful', 'communication-skill','coommunication skill','highly qualified', 'highly-qualified', 'results-focussed', 'result-focussed','results focussed', 'result focussed', 'effectual leader', 'effectual-leader','energetic','confident','professional','successfully', 'team player', 'team-player','responsible for','entrepreunerial','best of breed','detail oriented','detail-oreinted','seasoned','referances available by request','ambitious','punctual','go-getter','go getter','honest','strategic thinker','synnergy']
    test_string=string.lower()
    res = [ele for ele in test_list if(ele in test_string)]
    No_of_fillerwords.append(len(res))
    No_of_fillerwords.append(res)
    return(No_of_fillerwords)


#Function to check for redundancy
def redundancy(string):
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    text=string.lower()
    no_punct = ""
    for char in text:
        if char not in punctuations:
            no_punct = no_punct + char
    text_tokens = word_tokenize(no_punct)

    text = [word for word in text_tokens if not word in stopwords.words()]
    dictOfElems = RedundancyCheck(text)
    redundant_words = list(dictOfElems.values())
    count = sum(redundant_words) - len(redundant_words)
    return count
    
    
def RedundancyCheck(listOfElems):
    dictOfElems = dict()
    for elem in listOfElems:
        if elem in dictOfElems:
            dictOfElems[elem] += 1
        else:
            dictOfElems[elem] = 1    
 
    dictOfElems = { key:value for key, value in dictOfElems.items() if value > 5}
    return dictOfElems


#Function to extract year
def extract(text):
    c=""
    year=[]
    for i in text:
        c+=i+" "
    for key in c:
        year = re.findall('((?:19|20)\d\d)', c)
    year.sort()
    return(year)

#Function to check passive form
def is_passive(sentence):
    matcher = Matcher(nlp.vocab)
    doc = nlp(sentence)
    passive_rule = [{'DEP': 'nsubjpass'}, {'DEP': 'aux', 'OP': '*'}, {'DEP': 'auxpass'}, {'TAG': 'VBN'}]
    matcher.add('Passive', None, passive_rule)
    matches = matcher(doc)
    count =0
    if matches:
        return True
    else:
        return False
    

#Function to check wrong use of tense
def check_for_tense(sentence):
    text = word_tokenize(sentence)
    tagged = pos_tag(text)

    tense = dict()
    tense["future"] = len([word for word in tagged if word[1] == "MD"])
    tense["present"] = len([word for word in tagged if word[1] in ["VBP", "VBZ","VBG"]])
    tense["past"] = len([word for word in tagged if word[1] in ["VBD", "VBN"]]) 
    return(tense)

#Function to check consistency of tense
def tenses_res(str):
    tenses_check = check_for_tense(str)
    new_list = list(tenses_check.values())
    if new_list[0] == 0 and new_list[1] == 0:
        return False
    elif new_list[1] == 0 and new_list[2] == 0:
        return False
    elif new_list[0] == 0 and new_list[2] == 0:
        return False
    else:
        return True
    

#Function to Check for paragraph
def paragraph_check(str):
    Counter = 0
    for i in str: 
        if i: 
            Counter += 1
            
    if Counter > 5:
        return 0
    else:
        return 1
    

#Function to check for contact details
def contact_details(string):
    contact = []
    phone=re.findall('(?:\+[1-9]\d{0,2}[- ]?)?[1-9]\d{9}', string)
    email=re.findall(r"([a-zA-Z0-9.-]+@[a-zA-Z0-9.-]+\.[a-zA-Z0-9_-]+)",string)
    linkedin_username = re.findall(r"(?:https?:)?\/\/(?:[\w]+\.)?linkedin\.com\/in\/(?P<permalink>[\w\-\_À-ÿ%]+)\/?",string)
    if len(linkedin_username) != 0:
        linkedin_username[0] = 'https://www.linkedin.com/in/'+ linkedin_username[0]
    contact.append(email)
    contact.append(phone)
    contact.append(linkedin_username)
    return contact




#Function to extract names
def extract_name(resume_text):
    nlp_text = nlp(resume_text)
    matcher = Matcher(nlp.vocab)
    
    # First name and Last name are always Proper Nouns
    pattern = [[{'POS': 'PROPN'}, {'POS': 'PROPN'}]]
    
    matcher.add('NAME', None, *pattern)
    
    matches = matcher(nlp_text)
    
    for match_id, start, end in matches:
        span = nlp_text[start:end]
        return span.text    


#Function to verify correct date format
def date_format(str1): 
    c=""
    for i in str1:
        c+=i+" "
    
    keywords = ['jan', 'feb', 'mar','apr', 'may','jun', 'jul', 'aug', 'sep', 'oct','nov', 'dec']
    string = '20'
    punctuations = '''!()-[]{;:'"}\,<>./?@#$%^&*_~'''
    
    text=c
    lii = list(text.split(" "))
    Text = ""
    for char in text:
        if char not in punctuations:
            Text = Text + char
            
    two_dig = re.findall(r"\b\d{2}\b", Text)
    four_dig = re.findall(r'((?:19|20)\d\d)', text)
    current_time=datetime.datetime.now()
    
    
    month_yyyy = []
    month_yy = []
    only_year = []

    # declaring flag variables for different date formats
    correct_format = 0
    wrong_mmyy = 0
    wrong_year = 0
    
    yyyy_mm1 = re.findall(r'\d{4}-\d{2}', text)
    mm_yyyy1 = re.findall(r'\d{2}-\d{4}', text)
    mm_yyyy2 = re.findall(r'\d{2}/\d{4}', text)
    yyyy_mm2 = re.findall(r'\d{4}/\d{2}', text)
    

    
    
    try:
        if four_dig:
            for i in four_dig:
                var = i
                li = list(Text.split(" "))
                
    
                if var in li:
                    indexx = li.index(var)
                    prev = li[indexx-1]
                    
                    li.remove(i)
                    for j in keywords:

                         
                        if j in prev:

                            month_yyyy.append(var)
                             
                            break
                        else:
                            wrong_format=1
                            continue
    
        
        
        if two_dig:
            for i in two_dig:
                a = i
                
                li = list(Text.split(" "))
    
                indexx = li.index(a)
                prev = li[indexx-1]
                
                li.remove(i)
                for j in keywords:
                    
                    if j in prev:
                        if a>int(str(current_time)[2:4]):
                            month_yy.append('19' + a)
                            
                            break
                        else:
                            month_yy.append(string + a)
                     
                    else:
                        continue
   
    except:
        correct_format = 0
        wrong_mmyy = 0          
    

    if four_dig:
        only_year.append(four_dig)
    only_year = [ item for elem in only_year for item in elem]
    
    year_only = []
    if only_year:
        for elem in only_year:
            if elem not in month_yyyy and elem in lii:
                year_only.append(elem)
   
    if yyyy_mm1 or yyyy_mm2 or mm_yyyy1 or mm_yyyy2 or month_yyyy:
        correct_format = 1
    if month_yy:
        wrong_mmyy = 1
    if year_only:
        wrong_year = 1

    c=[]
    c.append(correct_format)
    c.append(wrong_mmyy)
    c.append(wrong_year)

    #identify the format of dates present
    if(c[0] == 0 and c[1]==0 and c[2] == 0):
        
        k=2
        
    else:
        if(c[0] == 1):
            if (c[1] == 1 and c[2] == 1) or (c[1] == 1 and c[2] == 0) or (c[1] == 0 and c[2] == 1):
                
                k=1
                
            else:
                
                k=0
                
        
        else:
            
            k=2
            

    return k    
    # return correct_format,wrong_mmyy,wrong_year,not_present


#Check for quantifiable impact
def quan(sent_text,list_):
    sent = nltk.tokenize.sent_tokenize(sent_text)
    alpha_num = ['one','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen','twenty','thirty','fourty','fifty','sixty','seventy','eighty','ninety','hundred','thousand']
    ress=[]
    keyw=0
    keyw_no=0
    s=""
    for i in sent:
        for j in list_:
             
            s = i.split(" ")
            for k in s:
                 
                if(k==j):
                    keyw = 1
                    keyw_no = checknos(i,alpha_num)
                     
            continue
    ress.append(keyw)
    ress.append(keyw_no)
    return ress


#Function to check numbers
def checknos(tex,noslist):
    sa = tex
    res = [int(i) for i in sa if i.isdigit()]
    with_num=0
    if res:
        with_num = 1
        return with_num
    else:
        with_num = 0

    for h in noslist:
        for a in sa:
            if (a==h):
                with_num = 1
                return with_num
        continue
    with_num = 0


def check(sent,wrd):
    c=[]
    for i in sent:
        for j in wrd:
            if j in i:
                c.append(j)
    
    return list(set(c))


#Check for hardskills match
def skillsMatch(text):
    df = pd.read_excel('Hard skill keywords.xlsx')

    l = df.values.tolist()
    skills = [item for sublist in l for item in sublist]
    res_words = list(text.split(" "))
    matched = []
    for i in res_words:
        if i in skills:
            matched.append(i)
    
################to remove duplicate matched skills#########################
    matched = list(dict.fromkeys(matched))
    
    return matched


#Function to check for hardskill        
def hardskills(text):
    m = ['.net', 'fashion', 'process improvement', 'account management', 'fda', 'process improvements', 'accounting', 'field sales', 'procurement', 'accounts payable', 'filing', 'product design', 'accounts receivable', 'finance', 'product development', 'acquisition', 'financial analysis', 'product knowledge', 'acquisitions', 'financial management', 'product line', 'administrative support', 'financial performance', 'product management', 'admissions', 'financial reporting', 'product marketing', 'Adobe', 'financial reports', 'product quality', 'Adobe Creative Suite', 'financial services', 'program development', 'advertising', 'financial statements', 'program management', 'affiliate', 'financing', 'programming', 'agile', 'fitness', 'project delivery', 'algorithms', 'Flex', 'project management', 'alliances', 'forecasting', 'project management skills', 'analysis', 'forecasts', 'project plan', 'analytical', 'frameworks', 'project planning', 'analytical skills', 'front-end', 'proposal', 'analytics', 'fulfillment', 'prospecting', 'analyze data', 'fundraising', 'protocols', 'analyzing data', 'GAAP', 'prototype', 'android', 'general ledger', 'psychology', 'annual budget', 'German', 'public health', 'API', 'GIS', 'public policy', 'APIs', 'governance', 'public relations', 'architecture', 'graphic design', 'publications', 'architectures', 'hardware', 'publishing', 'assembly', 'health', 'purchase orders', 'asset management', 'healthcare', 'purchasing', 'audio', 'help desk', 'Python', 'audit', 'higher education', 'QA', 'auditing', 'quality assurance', 'AutoCAD', 'hospital', 'quality control', 'automation', 'hospitality', 'quality management', 'aviation', 'hotel', 'quality standards', 'AWS', 'hotels', 'R (programming language)', 'banking', 'HRIS', 'raw materials', 'benchmark', 'HTML', 'real estate', 'beverage', 'HTML5', 'real-time', 'BI', 'human resource', 'reconcile', 'big data', 'I-DEAS', 'reconciliation', 'billing', 'IBM', 'recruit', 'biology', 'immigration', 'recruiting', 'brand', 'in-store', 'recruitment', 'branding', 'InDesign', 'regulations', 'broadcast', 'industry experience', 'regulatory', 'budget', 'industry trends', 'regulatory compliance', 'budget management', 'information management', 'regulatory requirements', 'budgeting', 'information security', 'relationship building', 'build relationships', 'information system', 'relationship management', 'business administration', 'information systems', 'repairs', 'business analysis', 'information technology', 'reporting', 'business cases', 'installation', 'research', 'business continuity', 'instructional design', 'research projects', 'business development', 'instrumentation', 'researching', 'business intelligence', 'internal audit', 'resource management', 'business issues', 'internal communications', 'retail', 'business management', 'internal controls', 'retention', 'business planning', 'internal customers', 'revenue growth', 'business plans', 'internal stakeholders', 'RFP', 'business process', 'international', 'RFPs', 'business requirements', 'internship', 'risk assessment', 'business stakeholders', 'intranet', 'risk assessments', 'business strategy', 'inventory', 'risk management', 'business systems', 'inventory management', 'root cause', 'C\xa0(programming language)', 'investigate', 'root cause', 'C#', 'investigation', 'routing', 'C++', 'investigations', 'SaaS', 'CAD', 'invoices', 'safety', 'call center', 'invoicing', 'sales', 'case management', 'iOS', 'sales experience', 'cash flow', 'iPhone', 'sales goals', 'certification', 'ISO', 'sales management', 'CFA', 'IT infrastructure', 'sales operations', 'change management', 'ITIL', 'Salesforce', 'chemicals', 'Java', 'SAP', 'chemistry', 'Javascript', 'SAS', 'circuits', 'JIRA', 'scheduling', 'Cisco', 'journal entries', 'SCI', 'client relationships', 'journalism', 'scripting', 'client service', 'key performance indicators', 'scrum', 'client services', 'KPI', 'SDLC', 'cloud', 'KPIs', 'security clearance', 'CMS', 'LAN', 'segmentation', 'co-op', 'law enforcement', 'SEO', 'coaching', 'leadership development', 'service delivery', 'coding', 'lean', 'SharePoint', 'commissioning', 'legal', 'six sigma', 'complex projects', 'legislation', 'small business', 'compliance', 'licensing', 'social media', 'computer applications', 'life cycle', 'software development', 'computer science', 'lifecycle', 'software development life cycle', 'computer software', 'lighting', 'software engineering', 'construction', 'Linux', 'SolidWorks', 'consulting', 'litigation', 'SOPs', 'consulting experience', 'logistics', 'sourcing', 'consulting services', 'machine learning', 'specifications', 'consumers', 'man resources', 'spelling', 'content', 'manage projects', 'sports', 'continuous improvement', 'management consulting', 'spreadsheets', 'contract management', 'management experience', 'SQL', 'contracts', 'market research', 'SQL server', 'controls', 'marketing', 'staffing', 'conversion', 'marketing materials', 'stakeholder management', 'correspondence', 'marketing plans', 'standard operating procedures', 'cost effective', 'marketing programs', 'standardization', 'cost reduction', 'marketing strategy', 'start-up', 'counsel', 'mathematics', 'startup', 'counseling', 'MATLAB', 'statistical analysis', 'CPG', 'matrix', 'statistics', 'CPR', 'mechanical engineering', 'status reports', 'CRM', 'media relations', 'strategic direction', 'cross-functional team', 'medical device', 'strategic initiatives', 'CSS', 'merchandising', 'strategic planning', 'customer experience', 'metrics', 'strategic plans', 'customer facing', 'Microsoft Office', 'strategy', 'customer requirements', 'Microsoft Office Suite', 'strong analytical skills', 'customer service', 'Microsoft Word', 'supervising', 'customer-facing', 'migration', 'supervisory experience', 'D (programming language)', 'mining', 'supply chain', 'daily operations', 'MIS', 'supply chain management', 'data analysis', 'mobile', 'support services', 'data center', 'modeling', 'Tableau', 'data collection', 'mortgage', 'tablets', 'data entry', 'MS Excel', 'talent acquisition', 'data management', 'MS Office', 'talent management', 'data quality', 'MS Project', 'tax', 'database', 'negotiation', 'technical', 'datasets', 'networking', 'technical issues', 'deposits', 'non-profit', 'technical knowledge', 'design', 'nursing', 'technical skills', 'development activities', 'office software', 'technical support', 'digital marketing', 'on-boarding', 'telecom', 'digital media', 'on-call', 'test cases', 'distribution', 'operating systems', 'test plans', 'DNS', 'operational excellence', 'testing', 'documentation', 'operations', 'therapeutic', 'documenting', 'operations management', 'trade shows', 'drafting', 'oracle', 'training', 'drawings', 'ordering', 'transactions', 'driving record', 'OS', 'transport', 'due diligence', 'outreach', 'transportation', 'dynamic environment', 'outsourcing', 'travel', 'e-commerce', 'partnership', 'travel arrangements', 'ecommerce', 'partnerships', 'troubleshooting', 'economics', 'payments', 'TV', 'editing', 'payroll', 'Twitter', 'editorial', 'PeopleSoft', 'UI', 'electrical', 'performance improvement', 'underwriting', 'electrical engineering', 'performance management', 'Unix', 'electronics', 'performance metrics', 'usability', 'EMEA', 'pharmaceutical', 'user experience', 'employee engagement', 'pharmacy', 'UX', 'employee relations', 'phone calls', 'valid drivers license', 'end user', 'photography', 'value proposition', 'engagement', 'Photoshop', 'variances', 'engineering', 'physical security', 'vendor management', 'ERP', 'physics', 'vendors', 'ETL', 'PMP', 'video', 'event planning', 'policies', 'VMware', 'expenses', 'portfolio management', 'warehouse', 'experimental', 'positioning', 'web services', 'experiments', 'PR', 'windows', 'external partners', 'presentation', 'workflows', 'fabrication', 'presentations', 'writing', 'Facebook', 'process development']
    matched=[]
    for i in text:
        li = [e for e in m if(e in i)]
        if li:
            matched.append(li)
    result = [item for sublist in matched for item in sublist]
    return result


#Function to extract phone numbers
def phone1(string):
    phone=re.findall(r"(?<!\d)\d{10}(?!\d)", string)
    phn=0
    if phone:
        phn = 1
    else:
        phn =0
    return phn



#Function to find email
def email1(string):
    email_=re.findall(r"([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)",string)
    mail=0
    if email_:
        mail =1
    else:
        mail=0
    return mail

#Function to find linkedin link
def linkedin1(string):
    linkedin_username = re.findall(r"(?:https?:)?\/\/(?:[\w]+\.)?linkedin\.com\/in\/(?P<permalink>[\w\-\_À-ÿ%]+)\/?",string)

    if linkedin_username:
        linkedIn = 1
    else:
        linkedIn = 0
    return linkedIn


#Function to find matching keywords in two dicts
def matching(li1,li2):
    common = []
    for i in li1:
        if i in li2:
            common.append(i)
    final_list = [] 
    for x in common: 
        if x not in final_list: 
            final_list.append(x) 
    
    count_res = {}
    count_jd ={}
    for i in final_list:
        if i not in count_res:
            count_res.update({i: li1.count(i)})
        if i not in count_jd:
            count_jd.update({i: li2.count(i)})
   
    return [count_res,count_jd]
#     return count_res, count_jd


#function to find educational degree match
def edmatch(text):
   
    m = ['AA','AS','AAS','AE','AB','AAA','ALM','AGS','AMIE','ASN','AF','AT','AAB','AAS','AAT','ABS','ABA','AES','ADN','AET','AFA','APE','AIT','AOS','ASPT-APT','APS',
    'BE', 'BS', 'BFA','BAS','BSBA','BFA','BCom', 'BMOS','BComm','B.Acy','B.Acc','B. Accty','BBusSc','BSN', 'BBus','BSC','BSET','BCOM','BMS','BA','BIBE','BCA','BBA','BBM','BIBE','BTECH','BARCH','BAA','BAAS','BAppSc(IT)','BDES','BENG','BSE','BESC','BSEng', 'BASc','BAccSci''BCompt', 'BEc', 'BEconSc' , 'BAOM', 'BCompSc','BComp','BCA','BBIS','BMedSci','BSPH','BMedBiol','BN', 'BNSc', 'BScN', 'BSN', 'BNurs', 'BSN', 'BHSc',
    'BHS','BHSc','BKin', 'BHK','BAT','BAvn','BD', 'BDiv','BTh','Th.B.','BTech' 'BTheol','BRE','BRS','BIS','BJ', 'BAJ', 'BSJ','BJourn','BLArch','B.L.A.','BGS', 'BSGS','BAPSY','BSocSc','BMathSc','BURP','BPlan',
    'BPAPM','B.S.F.', 'B.Sc.F.','BMus',
    'CA','CDCS','CBSE',
    'DDS','DELF','DBA',
    'EdD',
    'GED','GradIETE',
    'HSC','HSSC',
    'ICSE',
    'JD',
    'MD','MCA','ME','MS','MTECH', 'MBA','MCOM','MA','MFA','MCAT','MAcc', 'MAc', 'MAcy',
    'MAS','MEcon','MArch','MASc', 'MAppSc', 'MApplSc', 'MASc', 'MAS','MA', 'MAT','MLA', 'MLS', 'MALS',
    'MBus','MBA','MBI','MChem','MCom','MCA','MCJ','MDes', 'MDesign','MDiv','MEcon','MEd', 'EdM', 'MAEd', 'MSEd', 'MSE', 'MEdL',
    'MEnt','MEng', 'ME', 'MEM','MFin','MFA','MHA','MHS','MH','MILR','MIS','MISM', 'MSIM', 'MIS','MSIT', 'MScIT', 'MJ','MJur',
    'LLM','MSL','MArch','MLitt','MA', 'ALM', 'MLA', 'MLS', 'MALS','MLIS','MM','MMath','MMus','MPharm','MPhil','MPhys','MPS',
    'MPA','MPAff','MPH','MPP','MRb','MSc','STM','MSM','MSc','MSci', 'MSi', 'ScM', 'MS', 'MSHS','SM','MSE','MFin','HRD','MSHRD',
    'MSMIS','MSIS','MSIT', 'MScIT', 'MSN','MSPM','MSc','MSM','MSL','SCM','MSSCM','MST','MSW','MSSc','ChM','MS','MCh','MChir',
    'MSt','ThM', 'MTh','MTS','MVSC','MVSc'
    'PGD','PGDB','PFDFM','PGDIM','PGDBO','PHD','PharmD',
    'SSC','SCB','SB','SDes'
    'X', 'XII']
    matched=[]
    li = [e for e in m if(e.lower() in text.lower())]
    if li:
        matched.append(li)
    result = [item for sublist in matched for item in sublist]
    return result


   




    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80) #app.run(host='0.0.0.0', port=80) 
