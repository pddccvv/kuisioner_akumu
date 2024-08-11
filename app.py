from flask import Flask, render_template, request, redirect, url_for
import qrcode
import pymysql

app = Flask(__name__)

# Database connection
connection = pymysql.connect(host="localhost", user="root", password="", db="survey_db")

# Generate QR Code
url = "http://your-domain.com/survey"
qr = qrcode.make(url)
qr.save("static/qr_code.png")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/survey", methods=["GET", "POST"])
def survey():
    if request.method == "POST":
        name = request.form["name"]
        answers = [request.form[f"question{i}"] for i in range(1, 10)]  # Update here
        suggestion = request.form["suggestion"]

        # Save the survey response to MySQL
        try:
            with connection.cursor() as cursor:
                sql = """INSERT INTO survey_responses (name, question1, question2, question3, 
                        question4, question5, question6, question7, question8, question9, 
                        suggestion) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(sql, (name, *answers, suggestion))
            connection.commit()
        except Exception as e:
            print(f"Error: {e}")
            connection.rollback()

        return redirect(url_for("thanks"))

    return render_template("survey.html")


@app.route("/thanks")
def thanks():
    return render_template("thanks.html")


if __name__ == "__main__":
    app.run(debug=True)
