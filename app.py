import os
from flask import Flask, render_template, request
import google.generativeai as genai

# --- 1. THE BRAIN ---
# Paste the key you just got from Google AI Studio inside the quotes
API_KEY = "AIzaSyB-slnlcLliAGv6_ttcZh-VozfWahaqXOA" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

app = Flask(__name__)

def generate_full_app(user_prompt):
    # This instruction tells Gemini exactly how to format the code
    system_instruction = (
        "You are an expert full-stack developer. Write a SINGLE-FILE HTML app "
        "that includes CSS and JavaScript. Use modern styling (like Tailwind CSS). "
        "Output ONLY the raw code, no conversation or markdown formatting."
    )
    
    try:
        response = model.generate_content(f"{system_instruction}\n\nApp Idea: {user_prompt}")
        # Clean up any markdown formatting (like ```html) the AI might add
        clean_code = response.text.replace("```html", "").replace("```", "").strip()
        return clean_code
    except Exception as e:
        return f"<h1>Error</h1><p>{str(e)}</p>"

@app.route('/', methods=['GET', 'POST'])
def home():
    user_input = ""
    generated_app = None
    
    if request.method == 'POST':
        user_input = request.form.get('user_input')
        if user_input:
            # This triggers the AI call
            generated_app = generate_full_app(user_input)

    return render_template('index.html', 
                           generated_app=generated_app, 
                           user_input=user_input)

if __name__ == '__main__':
    app.run(debug=True)