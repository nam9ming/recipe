from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Flask 앱 초기화
app = Flask(__name__)

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')

# Google Gemini API 설정
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

cuisines=[
    "",
    "Korean",
    "Italian",
    "Mexican",
    "Chinese",
    "Indian",
    "Japanese",
    "Thai",
    "French",
    "Mediterranean",
    "American",
    "Greek",
]

# create a dictionary to store the languages and their corresponding codes
languages = {
    'English': 'en',
    'Spanish': 'es',
    'French': 'fr',
    'German': 'de',
    'Russian': 'ru',
    'Chinese (Simplified)': 'zh-CN',
    'Chinese (Traditional)': 'zh-TW',
    'Japanese': 'ja',
    'Korean': 'ko',
    'Italian': 'it',
    'Portuguese': 'pt',
    'Arabic': 'ar',
    'Dutch': 'nl',
    'Swedish': 'sv',
    'Turkish': 'tr',
    'Greek': 'el',
    'Hebrew': 'he',
    'Hindi': 'hi',
    'Indonesian': 'id',
    'Thai': 'th',
    'Filipino': 'tl',
    'Vietnamese': 'vi'
    # ... potentially more based on actual Whisper support
}

dietary_restrictions = [
    "Gluten-Free",
    "Dairy-Free",
    "Vegan",
    "Pescatarian",
    "Nut-Free",
    "Kosher",
    "Halal",
    "Low-Crab",
    "Organic",
    "Locally Sourced",
]


@app.route('/')
def index():
    # Display the main ingredient input page
    return render_template('index.html', cuisines=cuisines,
                           dietary_restrictions=dietary_restrictions, languages=languages)


@app.route('/generate_recipe', methods=['POST'])
def generate_recipe():
    # Extract the three ingredients from the user's input
    ingredients = request.form.getlist('ingredient')

    # Extract cuisine, restrictions, and language
    selected_cuisine = request.form.get('cuisine')
    selected_restrictions = request.form.getlist('restrictions')
    selected_language = request.form.get('language')

    print('selected_cuisine: ' + selected_cuisine)
    print('selected_restrictions: ' + str(selected_restrictions))
    print('selected_language: ' + selected_language)

    if len(ingredients) != 3:
        return "Kindly provide exactly 3 ingredients."

    # Craft a conversational prompt for ChatGPT, specifying our needs
    prompt = f"Craft a recipe in HTML in {selected_language} using {', '.join(ingredients)}. It's okay to use some other necessary ingredients. Ensure the recipe ingredients appear at the top, followed by the step-by-step instructions."


    if selected_cuisine:
        prompt += f"The cuisine should be {selected_cuisine}."

    if selected_restrictions and len(selected_restrictions) > 0:
        prompt += f"The recipe should have the following restrictions: {','.join(selected_restrictions)}."

    # Gemini API 호출
    try:
        response = model.generate_content(prompt)
        recipe = response.text  # Gemini 응답에서 텍스트 추출
    except Exception as e:
        recipe = f"Error generating recipe: {str(e)}"

    return render_template('recipe.html', recipe=recipe)


        


if __name__ == '__main__':
    app.run(debug=True)
