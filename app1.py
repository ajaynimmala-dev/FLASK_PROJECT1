from flask import Flask,render_template,request
app=Flask(__name__)
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/get',methods=['POST','GET'])
def getData():
    temp=request.form
    return 'success'

if __name__=='__main__':
    app.run(debug=True)

