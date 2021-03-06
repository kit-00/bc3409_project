#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask


# In[ ]:


app = Flask(__name__)


# In[ ]:


from flask import request, render_template
import pickle

MAX_EMPLOYEE_AGE: int = 70
MAX_YEARS_AT_COMPANY: int = 70-18

def validateAge(age):
    return age <= MAX_EMPLOYEE_AGE and age >= 18

def validateNumber(num):
    return num > 0
    
def validateYears(years):
    return years <= MAX_YEARS_AT_COMPANY

def invalidParameters(errorMsg=" "):
    s2 = errorMsg + " "
    return render_template("index.html", result = s2)

@app.route("/", methods=["GET","POST"])
def index():
    model = pickle.load(open("RF_model.sav", 'rb'))
    if request.method=="POST":
        Age = float(request.form.get("age") or 0)
        MonthlyIncome = float(request.form.get("monthlyincome") or 0)
        DistanceFromHome = float(request.form.get("distance") or 0)
        YearsAtCompany = float(request.form.get("years") or 0)

        if not (validateNumber(Age) and validateNumber(MonthlyIncome) and validateNumber(DistanceFromHome) and validateNumber(YearsAtCompany)):
            return invalidParameters("Please try again!")

        if not validateAge(Age):
            return invalidParameters("Age of employee must be in the range of 18-70. Please try again!")

        if not validateYears(YearsAtCompany):
            return invalidParameters("Years in company must be less than " + str(MAX_YEARS_AT_COMPANY) + ". Please try again!")

        print(Age, MonthlyIncome, DistanceFromHome, YearsAtCompany)
        pred = model.predict([[Age, MonthlyIncome, DistanceFromHome, YearsAtCompany]])
        s = str(pred)
        
        if s == "[0]":
            s1 = "Based on the above factors, this employee is unlikely to resign."
        else: 
            s1 = "Based on the above factors, this employee is likely to resign."
        
        return render_template("index.html", result = s1)

    return invalidParameters()


# In[ ]:


@app.route("/recommendations", methods=["GET"])
def recommendations():
    return render_template("recommendations.html")


# In[ ]:


@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")


# In[ ]:


if __name__ == "__main__":
    app.run()

