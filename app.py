from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Set the secret key for Flask's session management (important for flash messages)
app.secret_key = 'your_secret_key'  # Replace this with a more secure key in production

# Setup the SQLite database URI to use the /tmp directory (writable in Vercel)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join('/tmp', 'contact.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking for performance

# Initialize the database object
db = SQLAlchemy(app)

# Define the Contact model for storing form submissions
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    contact_number = db.Column(db.String(20))
    message = db.Column(db.Text, nullable=False)

# Home route to handle form submission and display the form
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
    contacts = Contact.query.all()  # This retrieves all contact submissions
    return render_template("view_messages.html", contacts=contacts)

@app.route('/download_cv')
def download_cv():
    return render_template('index1.html')  # Render the index1.html template


if __name__ == "__main__":
    app.run(debug=True)  # Run the app in debug mode for development

