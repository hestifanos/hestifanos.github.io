from flask import Flask, render_template, request
import secrets

# Create a Flask application instance
app = Flask(__name__)

# Generate a secret key for the Flask application
secret_key = secrets.token_hex(24)
app.secret_key = secret_key

# Define routes

@app.route('/')
def index():
    # Render the index.html template
    return render_template('index.html')

@app.route('/about')
def about():
    # Render the about.html template
    return render_template('about.html')

@app.route('/projects')
def projects():
    # Render the projects.html template
    return render_template('projects.html')

@app.route('/contact')
def contact():
    # Render the contact.html template
    return render_template('contact.html')

# Route to handle form submission from the contact page
@app.route('/submit_contact_form', methods=['POST'])
def submit_contact_form():
   
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    # Print form data to console
    print(f'Name: {name}, Email: {email}, Message: {message}')
    # Redirect to the contact page or any other page 
    return render_template('contact_confirmation.html', name=name)

# Error handling: Handle 404 errors (page not found)
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)

