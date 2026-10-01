from flask import Flask,render_template,redirect,url_for,request

app=Flask(__name__)
@app.route('/')
def home():
    return"<h1 style='text-align:center'>Kishna Chidar</h1>"

@app.route('/welcome')
def welcome():
    return"<h1>Welcome to Flask Traning</h1>"

@app.route('/index')    
def index():
    return render_template('index.html')

@app.route('/sucess/<int:a>')
def sucess(a):
    return "The person is pass and the score is :"+str(a)

@app.route('/fail/<int:a>')
def fail(a):
    return "The person is fail :"+str(a)

@app.route('/calculate', methods=["GET", "POST"])
def calculate():
    if request.method == "POST":
        maths = int(request.form['maths'])
        physics = int(request.form['physics'])
        chemistry = int(request.form['chemistry'])
        total = maths + physics + chemistry
        average = total / 3
        if average >= 80:
            return render_template('calculate.html', total=total, average=average, flag='pass')
        else:
            return render_template('calculate.html', total=total, average=average, flag='fail')
    return render_template('calculate.html')
if __name__ == '__main__':
    app.run(debug=True)
