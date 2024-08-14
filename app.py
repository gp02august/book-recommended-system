import os
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
import joblib
import numpy as np
import pandas as pd
import smtplib
from email.mime.text import MIMEText

# Load the data using joblib
popular_df = pd.read_pickle('popular.pkl')
pt = joblib.load('pt.pkl')
books = joblib.load('Books.pkl')
similarity_scores = joblib.load('similarity_scores.pkl')

app = Flask(__name__)
app.secret_key = 'your_random_secret_key'

# Temporarily hardcode email credentials for debugging purposes
MAIL_USERNAME = 'august2001gyanendra@gmail.com'
MAIL_PASSWORD = 'Ravi@221306'
MAIL_DEFAULT_SENDER = 'august2001gyanendra@gmail.com'

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
app.config['MAIL_DEFAULT_SENDER'] = MAIL_DEFAULT_SENDER

mail = Mail(app)

# Custom function to send email using smtplib
def send_email(subject, sender, recipients, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ", ".join(recipients)

    with smtplib.SMTP(app.config['MAIL_SERVER'], app.config['MAIL_PORT']) as server:
        server.starttls()
        server.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        server.sendmail(sender, recipients, msg.as_string())

@app.route('/')
def index():
    return render_template(
        'index.html',
        book_name=list(popular_df['Book-Title'].values),
        author=list(popular_df['Book-Author'].values),
        image=list(popular_df['Image-URL-M'].values),
        votes=list(popular_df['num_ratings'].values),
        rating=list(popular_df['avg_ratings'].values)
    )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    try:
        index = np.where(pt.index == user_input)[0][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]

        data = []
        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

            data.append(item)

        print(f"Recommendation data: {data}")
        return render_template('recommend.html', data=data)
    except IndexError:
        print("Book not found")
        return render_template('recommend.html', data=[], error="Book not found")

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Print debug information
        print(f"MAIL_USERNAME: {MAIL_USERNAME}")
        print(f"MAIL_DEFAULT_SENDER: {MAIL_DEFAULT_SENDER}")

        # Send email using custom function
        send_email('Contact Form Submission',
                   sender=MAIL_DEFAULT_SENDER,
                   recipients=[MAIL_USERNAME],
                   body=f"Name: {name}\nEmail: {email}\nMessage: {message}")

        flash('Message sent successfully!')
        return redirect(url_for('contact'))

    return render_template('contact.html')

if __name__ == '__main__':
    # Print debug information
    print("MAIL_USERNAME:", MAIL_USERNAME)
    print("MAIL_DEFAULT_SENDER:", MAIL_DEFAULT_SENDER)
    app.run(debug=True)