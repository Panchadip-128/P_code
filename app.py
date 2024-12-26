from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import os

# Flask app setup
app = Flask(__name__)
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

# Create tables if they don't exist (outside of app context)
with app.app_context():
    db.create_all()  # Only create tables, don't drop existing ones

# Routes
@app.route("/", methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        try:
            name = request.form['name']
            email = request.form['email']
            subject = request.form['subject']
            contact_number = request.form.get('contact_number', '')
            message = request.form['message']
            
            new_contact = Contact(
                name=name,
                email=email,
                subject=subject,
                contact_number=contact_number,
                message=message
            )
            
            db.session.add(new_contact)
            db.session.commit()
            flash("Form successfully submitted. We will contact you soon.", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {str(e)}", "error")
            print(f"Error details: {str(e)}")
        return redirect("/")
    return render_template("index.html")

@app.route("/view_messages")
def view_messages():
    contacts = Contact.query.all()
    return render_template("view_messages.html", contacts=contacts)

@app.route('/download_cv')
def download_cv():
    return render_template('index1.html')

@app.route("/check_db")
def check_db():
    try:
        # Get the database metadata
        inspector = db.inspect(db.engine)
        
        # Get all table names
        tables = inspector.get_table_names()
        
        # Get columns for the contact table
        columns = []
        if 'contact' in tables:
            columns = [column['name'] for column in inspector.get_columns('contact')]
        
        return {
            'database_uri': DATABASE_URI,
            'tables': tables,
            'contact_columns': columns,
            'exists': os.path.exists(DATABASE_URI)
        }
    except Exception as e:
        return {'error': str(e)}

if __name__ == "__main__":
    app.run(debug=True)
