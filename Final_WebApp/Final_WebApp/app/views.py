from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    form = LoginForm()







    user = {'nickname': 'Miguel'}
    posts = [
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('FirstPage.html',
                           title='Home',
                           form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="%s", remember_me=%s' %
              (form.openid.data, str(form.remember_me.data)))
        return redirect('/index')
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])


@app.route('/submit', methods=['POST'])
def submit():
    form = LoginForm()
    print('============')
    print(form.state.data)
    print(form.indicator.data)
    print(form.startyear.data)
    print(form.nextyear.data)
    dataResponse = restCall(form.startyear.data,form.nextyear.data,form.state.data,form.indicator.data)
    finalData = splitArray(dataResponse)
    return render_template('Results.html',
                           output=finalData,
                           StateName=form.state.data,
                           Indicator=form.indicator.data)



    if form.validate_on_submit():
        print('Submitted')

def splitArray(dataResponse):
    count = len(dataResponse)
    newData = []
    newCount = int(count / 3)
    for i in range(0,newCount):
        tempCount = i * 3
        temp = []
        temp.append(dataResponse[tempCount])
        temp.append(dataResponse[tempCount+1])
        temp.append(dataResponse[tempCount+2])
        newData.append(temp)
    return newData

def restCall(StartYear,EndYear,State,Indicator):
    import urllib
    from urllib.error import HTTPError
    from urllib.request import Request, urlopen
    # If you are using Python 3+, import urllib instead of urllib2

    import json

    data = {

        "Inputs": {

            "input1":
                {
                    "ColumnNames": ["StartYear", "EndYear", "State", "Indicator"],
                    "Values": [[StartYear,EndYear,State,Indicator], ]
                },
            "input3":
                {
                    "ColumnNames": ["StartYear", "EndYear", "State", "Indicator"],
                    "Values": [[StartYear,EndYear,State,Indicator], ]
                },
            "input2":
                {
                    "ColumnNames": ["StartYear", "EndYear", "State", "Indicator"],
                    "Values": [[StartYear,EndYear,State,Indicator], ]
                },
            "input4":
                {
                    "ColumnNames": ["StartYear", "EndYear", "State", "Indicator"],
                    "Values": [[StartYear,EndYear,State,Indicator], ]
                },
            "input5":
                {
                    "ColumnNames": ["StartYear", "EndYear", "State", "Indicator"],
                    "Values": [[StartYear,EndYear,State,Indicator], ]
                },
            "input6":
                {
                    "ColumnNames": ["StartYear", "EndYear", "State", "Indicator"],
                    "Values": [[StartYear,EndYear,State,Indicator], ]
                }, },
        "GlobalParameters": {
        }
    }

    body = str.encode(json.dumps(data))

    if Indicator == 'GDP':
        url = 'https://ussouthcentral.services.azureml.net/workspaces/338268e0005b48f09e88c611a2835a2f/services/623f891372b34931a0747125d41a3416/execute?api-version=2.0&details=true'
        api_key = 'APIKey'  # Replace this with the API key for the web service
        headers = {'Content-Type': 'application/json', 'Authorization': ('Bearer ' + api_key)}
    elif Indicator == 'TotalPersonalIncome':
        url = 'https://ussouthcentral.services.azureml.net/workspaces/338268e0005b48f09e88c611a2835a2f/services/725d1c92be264d759013a74aaa555345/execute?api-version=2.0&details=true'
        api_key = 'APIKey'  # Replace this with the API key for the web service
        headers = {'Content-Type': 'application/json', 'Authorization': ('Bearer ' + api_key)}
    elif Indicator == 'HousePriceIndex':
        url = 'https://ussouthcentral.services.azureml.net/workspaces/338268e0005b48f09e88c611a2835a2f/services/01c1fff6b4dd42fe8ec6f8d6bd591946/execute?api-version=2.0&details=true'
        api_key = 'APIKey'  # Replace this with the API key for the web service
        headers = {'Content-Type': 'application/json', 'Authorization': ('Bearer ' + api_key)}
    elif Indicator == 'UnemploymentRate':
        url = 'https://ussouthcentral.services.azureml.net/workspaces/338268e0005b48f09e88c611a2835a2f/services/4aaf9b2f98c844d58f7c5b9814714099/execute?api-version=2.0&details=true'
        api_key = 'APIKey'  # Replace this with the API key for the web service
        headers = {'Content-Type': 'application/json', 'Authorization': ('Bearer ' + api_key)}

    req = Request(url, body, headers)

    try:
        response = urlopen(req)

        # If you are using Python 3+, replace urllib2 with urllib.request in the above code:
        # req = urllib.request.Request(url, body, headers)
        # response = urllib.request.urlopen(req)

        # result = response.readall().decode('utf-8')
        result = response.read().decode('utf-8')
        print(type(result))
        print(result)
        import codecs

        # reader = codecs.getreader("utf-8")
        # obj = json.load(reader(response))
        final_result = json.loads(result)
        res = final_result['Results']['output1']['value']['Values'][0];
        print(res)
        return res
    except HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())

        print(json.loads(error.read().decode('utf-8')))
