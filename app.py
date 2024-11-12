from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail, Message
# pip install flask flask-sqlalchemy pymysql

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://your_username:your_password@localhost/your_database'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS']

app.config['SECRET_KEY'] = 'mypass'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'jeevasathappan2000@gmail.com'
app.config['MAIL_PASSWORD'] = 'ksxjfunpqbjyyrzs'
db = SQLAlchemy(app)
mail = Mail(app)


class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    date = db.Column(db.String(80))
    occupation = db.Column(db.String(80))


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        date = request.form['date']
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        occupation = request.form['occupation']

        form = Form(first_name=first_name, last_name=last_name, email=email,
                    date=date_obj, occupation=occupation)
        db.session.add(form)
        db.session.commit()
        if email:  # Check if the email is not empty
            message_body = f'Thank you for the submission {first_name} {last_name}.'
            message = Message(subject='New Form Submission',
                              sender=app.config['MAIL_USERNAME'],
                              recipients=[email], body=message_body)
            mail.send(message)
            flash(f'{first_name} Your form submitted successfully!', 'success')
        else:
            flash('Email field is empty. Form submission failed.', 'error')
    return render_template('index.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5000)
