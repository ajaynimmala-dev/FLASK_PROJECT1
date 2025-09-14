from app import create_app,db

app = create_app()

@app.before_first_request
#TODO this needs to be removed later
def create_table():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)