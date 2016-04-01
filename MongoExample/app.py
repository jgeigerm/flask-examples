#!flask/bin/python
from flask import Flask,render_template,redirect, request, url_for
from pymongo import MongoClient

#Initialize the application, import config, setup database, setup CSRF protection
app = Flask(__name__)

#Initialize the database connection
client = MongoClient()
db = client.Movies

#form to submit data
@app.route('/')
def main():
	return render_template('form_submit.html')

#form to take action on data
@app.route('/submit/',methods=['POST'])
def submit():
	#Variables
	inputSearch = request.form['dbSearch']		#Search query
	inputName = request.form['movieName']		#Movie name to enter into database
	movieLst = []					#List of movies

	#Mongo insert
	if inputSearch == "":
		print "insert"
		db.Movies.insert({"Name":inputName})

	#mongo search
	else:
		#add each entry in database that contains string to a list
		for document in  db.Movies.find({'Name':inputSearch}):	
			movieLst.append(document)
		
	return render_template('form_submit.html',dataEntered=inputName,searchQuery=movieLst)

# Run the app :)
if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)

