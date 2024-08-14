# Book Recommendation System

This is a Flask-based Book Recommendation System that suggests similar books based on user input. The project uses a combination of pre-trained models and data files to generate recommendations. It also includes a contact form that sends emails via SMTP.

## Features

- **Book Recommendations**: Suggests books similar to the one entered by the user.
- **Contact Form**: Allows users to send messages directly to the site admin.
- **Pre-Trained Models**: Uses pre-trained models to predict similar books.
- **Email Notifications**: Sends email notifications for contact form submissions.

## Project Structure

```plaintext
├── templates
│   ├── index.html          # Homepage template
│   ├── recommend.html      # Recommendation page template
│   ├── contact.html        # Contact form template
├── popular.pkl             # Pre-trained data for popular books
├── pt.pkl                  # Pre-trained pivot table for book recommendations
├── Books.pkl               # Pre-trained book data
├── similarity_scores.pkl   # Pre-trained similarity scores
├── app.py                  # Main Flask application file
└── README.md               # Project README file
```

Installation
-git clone https://github.com/gp02august/book-recommendation-system.git
-cd book-recommendation-system

Create Virtual Environnment
-python3 -m venv venv
-source venv/bin/activate  # On Windows use `venv\Scripts\activate`

Install Dependencies
-pip install -r requirements.txt

-Run The app
-python app.py
