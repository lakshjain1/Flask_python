from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from pymongo.errors import PyMongoError

app = Flask(__name__)

client = MongoClient("mongodb+srv://laksh:1234@cluster1.fogvrve.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1")
db = client["mydatabase"]
collection = db["users"]

@app.route('/', methods=['GET', 'POST'])
def form():
    error_message = None

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')

        if not name or not email:
            error_message = "Both name and email are required."
        else:
            try:
                collection.insert_one({"name": name, "email": email})
                return redirect(url_for('success'))
            except PyMongoError as e:
                error_message = f"Database error: {str(e)}"

    return render_template('index.html', error=error_message)

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
