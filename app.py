from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import os

# Flask app setup
app = Flask(__name__)

# Secret key for session management
app.secret_key = 'your_secret_key'

# Create the tmp directory if it doesn't exist
os.makedirs(os.path.join(os.getcwd(), 'tmp'), exist_ok=True)

# Database URI
DATABASE_URI = os.path.join(os.getcwd(), 'tmp', 'contact.db')
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
        try:
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
            db.session.add(new_contact)
            db.session.commit()
            flash("Form successfully submitted. We will contact you soon.", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {str(e)}", "error")
            print(f"Error details: {str(e)}")  # Added for debugging
        return redirect("/")
    return render_template("index.html")

@app.route("/view_messages")
def view_messages():
    contacts = Contact.query.all()
    return render_template("view_messages.html", contacts=contacts)

@app.route('/download_cv')
def download_cv():
    return render_template('index1.html')

# Create the database tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
