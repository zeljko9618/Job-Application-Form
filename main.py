from datetime import datetime
from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Creating a sqlite database file with the name data.db
app.config["SECRET_KEY"] = "myapplication123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
db = SQLAlchemy(app)


# Creating a form of the database file data.db
class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    email = db.Column(db.String(30))
    available_date = db.Column(db.Date)
    current_position = db.Column(db.String(30))


# Homepage
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":  # weil der button "Submit aus der Datei index.html einen POST produziert"
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        date = request.form["available_date"]
        available_date = datetime.strptime(date, "%Y-%m-%d")
        current_position = request.form["current_position"]

        # Creating an instance and saving in data.db
        # Important: using parameters to create an instance, without them you will get an error
        form = Form(first_name=first_name, last_name=last_name, email=email, available_date=available_date, current_position=current_position)
        db.session.add(form)
        db.session.commit()

        flash(f"{last_name} {first_name} Your form was submitted successfully!", "success")

    return render_template("index.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5001)
