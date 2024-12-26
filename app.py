from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import os

# Flask app setup
app = Flask(__name__)

# Secret key for session management (replace with a more secure key in production)
app.secret_key = 'your_secret_key'

# Database URI (consider using environment variables for deployment)
# Adjust the path based on your project structure and database choice
DATABASE_URI = os.path.join(os.getcwd(), 'tmp', 'contact.db')
# DATABASE_URI = os.environ.get('DATABASE_URL')  # If using environment variable

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_URI}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Contact model
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    contact_number = db.Column(db.String(20))
    message = db.Column(db.Text, nullable=False)

# Routes

@app.route("/", methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        # Collect form data
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        contact_number = request.form.get('contact_number', '')
        message = request.form['message']

        # Create a new Contact instance
        new_contact = Contact(
            name=name,
            email=email,
            subject=subject,
            contact_number=contact_number,
            message=message
        )

        # Add to the database and commit
        try:
            db.session.add(new_contact)
            db.session.commit()
            flash("Form successfully submitted. We will contact you soon.", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {str(e)}", "error")

        return redirect("/")  # Redirect to the same page after form submission

    return render_template("index.html")  # Render the form page


@app.route("/view_messages")
def view_messages():
    # Fetch all messages from the Contact model
    contacts = Contact.query.all()
    return render_template("view_messages.html", contacts=contacts)


@app.route('/download_cv')
def download_cv():
    return render_template('index1.html')  # Render the index1.html template


if __name__ == "__main__":
    app.run(debug=True)



