from flask import Flask,render_template,request
app=Flask(__name__)

data=[{
    'name':'ganesh',
    'regdno':'y23cs001',
    'branch':'CSE'
},{
    'name':'ramesh',
    'regdno':'y23cs002',
    'branch':'AIML'
}]
@app.route('/home')
def home():
    return render_template('home.html',posts=data,title='abcd')

@app.route('/about')
def about():
    return render_template('about.html',title='abcd')


@app.route('/get',methods=['POST','GET'])
def getData():
    temp=request.form
    return 'success'

if __name__=='__main__':
    app.run(debug=True)

