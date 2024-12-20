




# import os
# from flask import Flask, render_template, request, redirect, url_for, session, flash
# from werkzeug.utils import secure_filename
# from collections import OrderedDict

# import mysql.connector as sk
# from transformers import GPT2LMHeadModel, GPT2Tokenizer
# from model import main  # Import main function from model.py

# app = Flask(__name__)
# app.secret_key = 'your_secret_key'

# UPLOAD_FOLDER = 'static/uploads/'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # Initialize GPT-2 model and tokenizer
# model_name = r'./models'
# tokenizer = GPT2Tokenizer.from_pretrained(model_name)
# model = GPT2LMHeadModel.from_pretrained(model_name)

# # Database connection
# connection = sk.connect(
#     host="localhost",
#     user="root",
#     password="29164",
#     database="final_year_project"
# )
# sql = connection.cursor()

# # Function to generate a report using GPT-2
# # def generate_report(severity_level):
# #     prompt = ""
# #     if severity_level == 'Mild':
# #         prompt = "Based on the image analysis, the severity of diabetic retinopathy is classified as Mild DR..."
# #     elif severity_level == 'Moderate':
# #         prompt = "Based on the image analysis, the severity of diabetic retinopathy is classified as Moderate DR..."
# #     elif severity_level == 'Severe':
# #         prompt = "Based on the image analysis, the severity of diabetic retinopathy is classified as Severe DR..."
# #     elif severity_level == 'No DR':
# #         prompt = "Based on the image analysis, no diabetic retinopathy (No DR) is detected..."
# #     elif severity_level == 'Proliferative DR':
# #         prompt = "Based on the image analysis, the severity of diabetic retinopathy is classified as Proliferative DR..."
    
# #     # Generate the text using GPT-2
# #     inputs = tokenizer.encode(prompt, return_tensors='pt')
# #     outputs = model.generate(inputs, max_length=300, num_return_sequences=1, no_repeat_ngram_size=2)
    
# #     # Decode the output and return it as the report
# #     report = tokenizer.decode(outputs[0], skip_special_tokens=True)
# #     return report

# def generate_report(severity_level):
#     # Structured prompt for GPT-2 to ensure clear sections
#     prompt = f"""
#     The severity of diabetic retinopathy is classified as: {severity_level}.
#     Please provide a detailed analysis with the following sections:
    
#     Risks:
#     - Describe the potential risks associated with this severity level of diabetic retinopathy.
    
#     Suggestions:
#     - Provide actionable suggestions for managing this severity level of diabetic retinopathy.
    
#     Recommendation:
#     - Provide specific recommendations for the patient or healthcare provider.
#     """
    
#     # Generate text using GPT-2
#     inputs = tokenizer.encode(prompt, return_tensors='pt')
#     outputs = model.generate(
#         inputs,
#         max_length=300, 
#         num_return_sequences=1, 
#         no_repeat_ngram_size=2,
#         temperature=0.7,  # Adjust for creativity
#         pad_token_id=tokenizer.eos_token_id
#     )
    
#     # Decode and return the generated report
#     report = tokenizer.decode(outputs[0], skip_special_tokens=True)
#     return report


# # Function to extract sections (Risks, Suggestions, Recommendations) from the report
# import re
# def extract_sections(report):
#     sections = {
#         "Risks": "",
#         "Suggestions": "",
#         "Recommendation": ""
#     }
    
#     # Regular expressions to match the sections
#     risks_pattern = r"Risks:([\s\S]*?)(?=(Suggestions|Recommendation|$))"
#     suggestions_pattern = r"Suggestions:([\s\S]*?)(?=(Recommendation|$))"
#     recommendation_pattern = r"Recommendation:([\s\S]*?)(?=$)"
    
#     # Extract each section
#     risks_match = re.search(risks_pattern, report)
#     if risks_match:
#         sections["Risks"] = risks_match.group(1).strip()
        
#     suggestions_match = re.search(suggestions_pattern, report)
#     if suggestions_match:
#         sections["Suggestions"] = suggestions_match.group(1).strip()
        
#     recommendation_match = re.search(recommendation_pattern, report)
#     if recommendation_match:
#         sections["Recommendation"] = recommendation_match.group(1).strip()
    
#     return sections


# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         query = "SELECT * FROM THEGREAT WHERE USERNAME = %s AND PASSWORD = %s"
#         sql.execute(query, (username, password))
#         user = sql.fetchone()

#         if user:
#             session['username'] = username
#             flash('Login successful!', 'success')
#             return redirect(url_for('dashboard'))
#         else:
#             flash('Invalid username or password.', 'danger')

#     return render_template('login.html')

# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         query = "SELECT * FROM THEGREAT WHERE USERNAME = %s"
#         sql.execute(query, (username,))
#         user = sql.fetchone()

#         if user:
#             flash('Username already exists. Please choose another.', 'warning')
#         else:
#             query = "INSERT INTO THEGREAT (USERNAME, PASSWORD) VALUES (%s, %s)"
#             sql.execute(query, (username, password))
#             connection.commit()
#             flash('Signup successful! You can now login.', 'success')
#             return redirect(url_for('login'))

#     return render_template('signup.html')

# @app.route('/dashboard')
# def dashboard():
#     if 'username' not in session:
#         flash('Please login to access the dashboard.', 'danger')
#         return redirect(url_for('login'))

#     return render_template('dashboard.html')

# @app.route('/upload', methods=['GET', 'POST'])
# def upload():
#     if 'username' not in session:
#         flash('Please login to access this page.', 'danger')
#         return redirect(url_for('login'))

#     if request.method == 'POST':
#         if 'file' not in request.files:
#             flash('No file part', 'danger')
#             return redirect(request.url)
        
#         file = request.files['file']
#         if file.filename == '':
#             flash('No selected file', 'danger')
#             return redirect(request.url)
        
#         if file:
#             filename = secure_filename(file.filename)
#             filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             file.save(filepath)
            
#             # Get severity prediction using the model
#             severity_value, severity_class = main(filepath)  # Call the model's main function
            
#             # Generate the full report using GPT-2
#             report = generate_report(severity_class)
            
#             # Extract sections from the report
#             sections = extract_sections(report)

#             # Extract risk, suggestions, and recommendations based on the severity
#             risk = sections["Risks"]
#             suggestion = sections["Suggestions"]
#             recommendation = sections["Recommendation"]

#             # Update the database with the predicted severity
#             query = 'UPDATE THEGREAT SET PREDICT = %s WHERE USERNAME = %s'
#             sql.execute(query, (severity_class, session['username']))
#             connection.commit()
#             print("Severity Class:", severity_class)
            
#             print("Risk:", risk)
#             print("Suggestion:", suggestion)
#             print("Recommendation:", recommendation)

#             # Pass consistent variables to the result template
#             severity_descriptions = {
#                 "Mild": "mild",
#                 "Moderate": "moderate",
#                 "Severe": "severe",
#                 "No DR": "no detectable",
#                 "Proliferative DR": "proliferative"
#             }
#             severity_description = severity_descriptions.get(severity_class, "unknown")

#             return render_template(
#                     'result.html',
#                     image_filename=filename,  
#                     value=severity_class,  
#                     severity_description=severity_description,
#                     risk=risk,  
#                     suggestion=suggestion,  
#                     recommendation=recommendation  
# )



#     return render_template('upload.html')


# @app.route('/logout')
# def logout():
#     session.pop('username', None)
#     flash('You have been logged out.', 'info')
#     return redirect(url_for('home'))

# if __name__ == '__main__':
#     if not os.path.exists(UPLOAD_FOLDER):
#         os.makedirs(UPLOAD_FOLDER)
#     app.run(debug=True)
   



# import os
# from flask import Flask, render_template, request, redirect, url_for, session, flash
# from werkzeug.utils import secure_filename
# from collections import OrderedDict

# import mysql.connector as sk
# # from transformers import GPT2LMHeadModel, GPT2Tokenizer
# from transformers import AutoModelForCausalLM, AutoTokenizer
# from model import main  # Import main function from model.py

# app = Flask(__name__)
# app.secret_key = 'your_secret_key'

# UPLOAD_FOLDER = 'static/uploads/'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # Initialize GPT-2 model and tokenizer


# # Load the BioGPT model and tokenizer
# model_name = "microsoft/BioGPT"
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForCausalLM.from_pretrained(model_name)


# # Database connection
# connection = sk.connect(
#     host="localhost",
#     user="root",
#     password="29164",
#     database="final_year_project"
# )
# sql = connection.cursor()

# # Function to generate a report using GPT-2
# # def generate_report(severity_level):
# #     prompt = f"""
# #     The diabetic retinopathy severity is classified as {severity_level}.
# #     Please provide the following:
# #     - Risks:
# #     - Suggestions:
# #     - Recommendations:
# #     """
# #     # Generate the text using GPT-2
# #     inputs = tokenizer.encode(prompt, return_tensors='pt')
# #     outputs = model.generate(inputs, max_length=300, num_return_sequences=1, no_repeat_ngram_size=2)
    
# #     # Decode the output and return it as the report
# #     report = tokenizer.decode(outputs[0], skip_special_tokens=True)
# #     return report

# def generate_biomedical_report(severity_level):
#     # Define the input prompt based on the severity level
#     prompts = {
#         "No DR": "Generate a report for a patient with no signs of diabetic retinopathy. Include general eye health recommendations.",
#         "Mild": "Generate a report for a patient with mild diabetic retinopathy. Include risks, suggestions, and a treatment plan.",
#         "Moderate": "Generate a report for a patient with moderate diabetic retinopathy. Include risks, possible complications, and a follow-up plan.",
#         "Severe": "Generate a report for a patient with severe diabetic retinopathy. Include risks, urgency for treatment, and recommendations.",
#         "Proliferative DR": "Generate a report for a patient with proliferative diabetic retinopathy. Provide detailed risks, immediate treatment options, and recommendations."
#     }
#     prompt = prompts.get(severity_level, "Provide a general report for diabetic retinopathy.")
    
#     # Tokenize the prompt
#     inputs = tokenizer.encode(prompt, return_tensors="pt")
    
#     # Generate text using BioGPT
#     outputs = model.generate(inputs, max_length=300, num_return_sequences=1, no_repeat_ngram_size=2)
    
#     # Decode and return the report
#     report = tokenizer.decode(outputs[0], skip_special_tokens=True)
#     return report


# # Function to extract sections (Risks, Suggestions, Recommendations) from the report
# import re
# def extract_sections(report):
#     sections = {
#         "Risks": "",
#         "Suggestions": "",
#         "Recommendation": ""
#     }
    
#     # Flexible regular expressions to capture variations
#     risks_pattern = r"(?i)risks?:([\s\S]*?)(?=(Suggestions?|Recommendations?|$))"
#     suggestions_pattern = r"(?i)suggestions?:([\s\S]*?)(?=(Recommendations?|$))"
#     recommendation_pattern = r"(?i)recommendations?:([\s\S]*?)(?=$)"
    
#     risks_match = re.search(risks_pattern, report)
#     if risks_match:
#         sections["Risks"] = risks_match.group(1).strip()
        
#     suggestions_match = re.search(suggestions_pattern, report)
#     if suggestions_match:
#         sections["Suggestions"] = suggestions_match.group(1).strip()
        
#     recommendation_match = re.search(recommendation_pattern, report)
#     if recommendation_match:
#         sections["Recommendation"] = recommendation_match.group(1).strip()
    
#     return sections
#  # Debugging statement


# # Debugging helper: Print all available routes
# @app.before_first_request
# def print_routes():
#     print("Available Routes:")
#     for rule in app.url_map.iter_rules():
#         print(rule)

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         query = "SELECT * FROM THEGREAT WHERE USERNAME = %s AND PASSWORD = %s"
#         sql.execute(query, (username, password))
#         user = sql.fetchone()

#         if user:
#             session['username'] = username
#             flash('Login successful!', 'success')
#             return redirect(url_for('dashboard'))
#         else:
#             flash('Invalid username or password.', 'danger')

#     return render_template('login.html')

# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         query = "SELECT * FROM THEGREAT WHERE USERNAME = %s"
#         sql.execute(query, (username,))
#         user = sql.fetchone()

#         if user:
#             flash('Username already exists. Please choose another.', 'warning')
#         else:
#             query = "INSERT INTO THEGREAT (USERNAME, PASSWORD) VALUES (%s, %s)"
#             sql.execute(query, (username, password))
#             connection.commit()
#             flash('Signup successful! You can now login.', 'success')
#             return redirect(url_for('login'))

#     return render_template('signup.html')

# @app.route('/dashboard')
# def dashboard():
#     if 'username' not in session:
#         flash('Please login to access the dashboard.', 'danger')
#         return redirect(url_for('login'))

#     return render_template('dashboard.html')

# @app.route('/upload', methods=['GET', 'POST'])
# def upload():
#     if 'username' not in session:
#         flash('Please login to access this page.', 'danger')
#         return redirect(url_for('login'))

#     if request.method == 'POST':
#         if 'file' not in request.files:
#             flash('No file part', 'danger')
#             return redirect(request.url)
        
#         file = request.files['file']
#         if file.filename == '':
#             flash('No selected file', 'danger')
#             return redirect(request.url)
        
#         if file:
#             # File handling
#             filename = secure_filename(file.filename)
#             filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             file.save(filepath)
            
#             # Call main function from model.py (ensure main is defined and imported)
#             severity_value, severity_class = main(filepath)  
            
#             # Generate report
#             report = generate_report(severity_class)  # Call the fixed generate_report
#             sections = extract_sections(report)
            
#             # Debug prints (to check in terminal)
#             print("Generated Report:", report)
#             print("Extracted Risks:", sections["Risks"])
#             print("Extracted Suggestions:", sections["Suggestions"])
#             print("Extracted Recommendation:", sections["Recommendation"])
            
#             # Pass results to result.html
#             return render_template(
#                 'result.html',
#                 image_filename=filename,
#                 value=severity_class,
#                 risk=sections["Risks"],
#                 suggestion=sections["Suggestions"],
#                 recommendation=sections["Recommendation"]
#             )
#     return render_template('upload.html')


# @app.route('/upload', methods=['GET', 'POST'])
# def upload():
#     if 'username' not in session:
#         flash('Please login to access this page.', 'danger')
#         return redirect(url_for('login'))

#     if request.method == 'POST':
#         if 'file' not in request.files:
#             flash('No file part', 'danger')
#             return redirect(request.url)
        
#         file = request.files['file']
#         if file.filename == '':
#             flash('No selected file', 'danger')
#             return redirect(request.url)
        
#         if file:
#             filename = secure_filename(file.filename)
#             filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             file.save(filepath)
            
#             # Call your ML model's `main()` function to predict severity
#             severity_value, severity_class = main(filepath)  # This should return severity (e.g., "Mild")

#             # Generate the report using BioGPT
#             report = generate_biomedical_report(severity_class)
            
#             # Extract sections if necessary
#             sections = extract_sections(report)
#             risk = sections["Risks"]
#             suggestion = sections["Suggestions"]
#             recommendation = sections["Recommendation"]

#             # Pass variables to the result page
#             return render_template(
#                 'result.html',
#                 image_filename=filename,
#                 value=severity_class,
#                 severity_description=severity_class,
#                 risk=risk,
#                 suggestion=suggestion,
#                 recommendation=recommendation
#             )

#     return render_template('upload.html')

# @app.route('/logout')
# def logout():
#     session.pop('username', None)
#     flash('You have been logged out.', 'info')
#     return redirect(url_for('home'))

# if __name__ == '__main__':
#     if not os.path.exists(UPLOAD_FOLDER):
#         os.makedirs(UPLOAD_FOLDER)
#     app.run(debug=True)


# import os
# from flask import Flask, render_template, request, redirect, url_for, session, flash
# from werkzeug.utils import secure_filename
# from collections import OrderedDict
# import re
# import mysql.connector as sk
# from transformers import AutoModelForCausalLM, AutoTokenizer
# from model import main  # Import main function from model.py

# app = Flask(__name__)
# app.secret_key = 'your_secret_key'

# UPLOAD_FOLDER = 'static/uploads/'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # Load the BioGPT model and tokenizer
# model_name = "microsoft/BioGPT"
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForCausalLM.from_pretrained(model_name)

# # Database connection
# connection = sk.connect(
#     host="localhost",
#     user="root",
#     password="29164",
#     database="final_year_project"
# )
# sql = connection.cursor()


# def generate_biomedical_report(severity_level):
#     # Define the input prompt based on the severity level
#     prompts = {
#     "No DR": "Generate a detailed report for a patient with no signs of diabetic retinopathy. Include risks (if any), eye health recommendations, and follow-up plans.",
#     "Mild": "Generate a detailed report for a patient with mild diabetic retinopathy. Include risks, early symptoms, suggestions for lifestyle changes, and follow-up plans.",
#     "Moderate": "Generate a detailed report for a patient with moderate diabetic retinopathy. Include risks of progression, possible treatments, and lifestyle suggestions.",
#     "Severe": "Generate a detailed report for a patient with severe diabetic retinopathy. Describe the risks, complications, urgency of treatment, and specific recommendations for intervention.",
#     "Proliferative DR": "Generate a comprehensive report for a patient with proliferative diabetic retinopathy. Highlight serious risks, immediate treatment options, and detailed follow-up recommendations."
#     }

#     prompt = prompts.get(severity_level, "Provide a general report for diabetic retinopathy.")
    
#     # Tokenize the prompt
#     inputs = tokenizer.encode(prompt, return_tensors="pt")
    
#     # Generate text using BioGPT
#     outputs = model.generate(
#                     inputs, 
#                     max_length=150,  # Reduce the output length
#                     temperature=0.7,  # Lower temperature for balanced outputs
#                     top_p=0.9,        # Use nucleus sampling for efficient generation
#                     num_return_sequences=1,
#                     no_repeat_ngram_size=2
#                 )


#     print("Input Prompt: ", prompt)

#     # Decode and return the report
#     report = tokenizer.decode(outputs[0], skip_special_tokens=True)
#     print("Generated Report:", report)
#     return report


# # Function to extract sections (Risks, Suggestions, Recommendations) from the report
# def extract_sections(report):
#     sections = {
#         "Risks": "",
#         "Suggestions": "",
#         "Recommendation": ""
#     }
    
#     # Flexible regular expressions to capture variations
#     risks_pattern = r"(?i)risks?:([\s\S]*?)(?=(Suggestions?|Recommendations?|$))"
#     suggestions_pattern = r"(?i)suggestions?:([\s\S]*?)(?=(Recommendations?|$))"
#     recommendation_pattern = r"(?i)recommendations?:([\s\S]*?)(?=$)"
    
#     risks_match = re.search(risks_pattern, report)
#     if risks_match:
#         sections["Risks"] = risks_match.group(1).strip()
        
#     suggestions_match = re.search(suggestions_pattern, report)
#     if suggestions_match:
#         sections["Suggestions"] = suggestions_match.group(1).strip()
        
#     recommendation_match = re.search(recommendation_pattern, report)
#     if recommendation_match:
#         sections["Recommendation"] = recommendation_match.group(1).strip()
    
#     return sections


# @app.before_first_request
# def print_routes():
#     print("Available Routes:")
#     for rule in app.url_map.iter_rules():
#         print(rule)

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         query = "SELECT * FROM THEGREAT WHERE USERNAME = %s AND PASSWORD = %s"
#         sql.execute(query, (username, password))
#         user = sql.fetchone()

#         if user:
#             session['username'] = username
#             flash('Login successful!', 'success')
#             return redirect(url_for('dashboard'))
#         else:
#             flash('Invalid username or password.', 'danger')

#     return render_template('login.html')

# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         query = "SELECT * FROM THEGREAT WHERE USERNAME = %s"
#         sql.execute(query, (username,))
#         user = sql.fetchone()

#         if user:
#             flash('Username already exists. Please choose another.', 'warning')
#         else:
#             query = "INSERT INTO THEGREAT (USERNAME, PASSWORD) VALUES (%s, %s)"
#             sql.execute(query, (username, password))
#             connection.commit()
#             flash('Signup successful! You can now login.', 'success')
#             return redirect(url_for('login'))

#     return render_template('signup.html')

# @app.route('/dashboard')
# def dashboard():
#     if 'username' not in session:
#         flash('Please login to access the dashboard.', 'danger')
#         return redirect(url_for('login'))

#     return render_template('dashboard.html')

# @app.route('/upload', methods=['GET', 'POST'])
# def upload():
#     if 'username' not in session:
#         flash('Please login to access this page.', 'danger')
#         return redirect(url_for('login'))

#     if request.method == 'POST':
#         if 'file' not in request.files:
#             flash('No file part', 'danger')
#             return redirect(request.url)
        
#         file = request.files['file']
#         if file.filename == '':
#             flash('No selected file', 'danger')
#             return redirect(request.url)
        
#         if file:
#             filename = secure_filename(file.filename)
#             filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             file.save(filepath)
            
#             # Call your ML model's `main()` function to predict severity
#             severity_value, severity_class = main(filepath)  # This should return severity (e.g., "Mild")

#             # Generate the report using BioGPT
#             report = generate_biomedical_report(severity_class)
            
#             # Extract sections if necessary
#             sections = extract_sections(report)
#             risk = sections["Risks"]
#             suggestion = sections["Suggestions"]
#             recommendation = sections["Recommendation"]

#             # Pass variables to the result page
#             return render_template(
#                 'result.html',
#                 image_filename=filename,
#                 value=severity_class,
#                 severity_description=severity_class,
#                 report=report,  # Pass the full report here
#                 risk=risk,
#                 suggestion=suggestion,
#                 recommendation=recommendation
#             )

#     return render_template('upload.html')

# @app.route('/logout')
# def logout():
#     session.pop('username', None)
#     flash('You have been logged out.', 'info')
#     return redirect(url_for('home'))

# if __name__ == '__main__':
#     if not os.path.exists(UPLOAD_FOLDER):
#         os.makedirs(UPLOAD_FOLDER)
#     app.run(debug=True)





import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from collections import OrderedDict
import re
import mysql.connector as sk

from model import main  # Import main function from model.py

app = Flask(__name__)
app.secret_key = 'your_secret_key'

UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load the lightweight T5 model and tokenizer
# model_name = "t5-small"  # Use "t5-small" for lightweight processing
# tokenizer = T5Tokenizer.from_pretrained(model_name)
# model = T5ForConditionalGeneration.from_pretrained(model_name)

# Database connection
connection = sk.connect(
    host="localhost",
    user="root",
    password="29164",
    database="final_year_project"
)
sql = connection.cursor()


# from transformers import T5Tokenizer, T5ForConditionalGeneration

# # Load T5 model and tokenizer
# tokenizer = T5Tokenizer.from_pretrained("t5-small")
# model = T5ForConditionalGeneration.from_pretrained("t5-small")

# def generate_biomedical_report(severity_level):
#     # Define the input prompt based on the severity level
#     prompts = {
#         "No DR": "Generate a report for a patient with no signs of diabetic retinopathy. Include general eye health recommendations.",
#         "Mild": "Generate a report for a patient with mild diabetic retinopathy. Include risks, suggestions, and a treatment plan.",
#         "Moderate": "Generate a report for a patient with moderate diabetic retinopathy. Include risks, possible complications, and a follow-up plan.",
#         "Severe": "Generate a report for a patient with severe diabetic retinopathy. Include risks, urgency for treatment, and recommendations.",
#         "Proliferative DR": "Generate a report for a patient with proliferative diabetic retinopathy. Provide detailed risks, immediate treatment options, and recommendations."
#     }
#     prompt = prompts.get(severity_level, "Provide a general report for diabetic retinopathy.")
    
#     # Tokenize the input prompt
#     inputs = tokenizer.encode(prompt, return_tensors="pt", max_length=512, truncation=True)
    
#     # Generate the report
#     outputs = model.generate(inputs, max_length=300, num_return_sequences=1, no_repeat_ngram_size=2, early_stopping=True)
    
#     # Decode and return the generated report
#     report = tokenizer.decode(outputs[0], skip_special_tokens=True)
#     return report

from transformers import pipeline

# Initialize Hugging Face GPT-2 text generation pipeline for feedback generation
generator = pipeline('text-generation', model='gpt2')

def generate_biomedical_report(severity_level):
    # Define the input prompt based on severity
    # prompts = {
    #     "No DR": "Generate for a patient with no signs of diabetic retinopathy. Include general eye health recommendations.",
    #     "Mild": "Generate a report for a patient with mild diabetic retinopathy. Include risks, suggestions, and a treatment plan.",
    #     "Moderate": "Generate a report for a patient with moderate diabetic retinopathy. Include risks, possible complications, and a follow-up plan.",
    #     "Severe": "Generate a report for a patient with severe diabetic retinopathy. Include risks, urgency for treatment, and recommendations.",
    #     "Proliferative DR": "Generate a report for a patient with proliferative diabetic retinopathy. Provide detailed risks, immediate treatment options, and recommendations."
    # }

    # Get the prompt for the severity level
    
    # prompt = prompts.get(severity_level, "Provide a general report for diabetic retinopathy.")
    
    # # Generate the initial report
    # generated_report = generator(prompt, max_length=150, num_return_sequences=1)[0]['generated_text']
    
    # Now, generate feedback based on the severity level
    feedback_prompt = f"PGenerate for a diabetic patient with {severity_level} (Diabetic Retinopathy). Include general eye health recommendations.."
    feedback = generator(feedback_prompt, max_length=50, num_return_sequences=1)[0]['generated_text']
    
    # Return both the report and feedback
    return  feedback


@app.before_first_request
def print_routes():
    print("Available Routes:")
    for rule in app.url_map.iter_rules():
        print(rule)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        query = "SELECT * FROM THEGREAT WHERE USERNAME = %s AND PASSWORD = %s"
        sql.execute(query, (username, password))
        user = sql.fetchone()

        if user:
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        query = "SELECT * FROM THEGREAT WHERE USERNAME = %s"
        sql.execute(query, (username,))
        user = sql.fetchone()

        if user:
            flash('Username already exists. Please choose another.', 'warning')
        else:
            query = "INSERT INTO THEGREAT (USERNAME, PASSWORD) VALUES (%s, %s)"
            sql.execute(query, (username, password))
            connection.commit()
            flash('Signup successful! You can now login.', 'success')
            return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash('Please login to access the dashboard.', 'danger')
        return redirect(url_for('login'))

    return render_template('dashboard.html')

# @app.route('/upload', methods=['GET', 'POST'])
# def upload():
#     if 'username' not in session:
#         flash('Please login to access this page.', 'danger')
#         return redirect(url_for('login'))

#     if request.method == 'POST':
#         if 'file' not in request.files:
#             flash('No file part', 'danger')
#             return redirect(request.url)
        
#         file = request.files['file']
#         if file.filename == '':
#             flash('No selected file', 'danger')
#             return redirect(request.url)
        
#         if file:
#             filename = secure_filename(file.filename)
#             filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             file.save(filepath)
            
#             # Call your ML model's `main()` function to predict severity
#             severity_value, severity_class = main(filepath)  # This should return severity (e.g., "Mild")

#             # Generate the report using T5
#             report = generate_biomedical_report(severity_class)

#             # Pass variables to the result page
#             return render_template(
#                 'result.html',
#                 image_filename=filename,
#                 value=severity_class,
#                 report=report
#             )

#     return render_template('upload.html')
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'username' not in session:
        flash('Please login to access this page.', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
        
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Call your ML model's `main()` function to predict severity
            severity_value, severity_class = main(filepath)  # This should return severity (e.g., "Mild")

            # Generate the report and feedback using GPT-2
            feedback = generate_biomedical_report(severity_class)
            
            # Pass both report and feedback to the result page
            return render_template(
                'result.html',
                image_filename=filename,
                value=severity_class,
                severity_description=severity_class,
                # report=report,  # Full generated report
                feedback=feedback  # Feedback generated from GPT-2
            )

    return render_template('upload.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
