from flask import Flask,render_template,request,url_for
app=Flask(__name__)

data=[{
    'name':'GANESH',
    'regdno':'Y23CS001',
    'branch':'CSE',
    'year':'2ND YEAR'
},{
    'name':'RAMESH',
    'regdno':'Y23CS002',
    'branch':'AIML',
    'year':'2ND YEAR'
}]
@app.route('/')
def home():
    return render_template('home.html',posts=data,title='website design')

@app.route('/about')
def about():
    return render_template('about.html',title='abcd')


@app.route('/get',methods=['POST','GET'])
def getData():
    temp=request.form
    return 'success'

if __name__=='__main__':
    app.run(debug=True)

