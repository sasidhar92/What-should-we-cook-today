import streamlit as st
import google.generativeai as genai
import os
import random




os.environ['API_KEY'] = st.secrets['API_KEY']
genai.configure(api_key=os.getenv('API_KEY'))

# Initialize Gemini model
model = genai.GenerativeModel('gemini-1.5-flash')


surprise_recipe_names = [
    'Tomato Pappu with Aloo Fry',
    'Beetroot Thoran with Meen Kulambu',
    'Coconut Chutney Spinach Dosa',
    'Lemon Rice with Peanut Masala Vadai',
    'Rava Idli with Coconut Chutney',
    'Gongura Chicken Curry with Bagara Rice',
    'Ulli Theeyal with Kerala Matta Rice',
    'Mango Pachadi with Mor Kuzhambu',
    'Masala Dosa with Aloo Masala',
    'Gutti Vankaya Kura with Jonna Roti'
]

def generate_recipe(recipe_name):
    prompt = "Generate a south indian recipe for {recipe_name}. Provide the recipe name on the first line, followed by a newline, then the full recipe details including ingredients, instructions, and cooking time."
    response = model.generate_content(prompt)
    lines = response.text.split('\n', 1)
    recipe_name = lines[0].strip()
    full_recipe = lines[1].strip() if len(lines) > 1 else ""
    return full_recipe

def generate_recipes_from_vegetables(selected_vegetables):
    prompt = f"Generate 2 South Indian recipes using these vegetables or a combination of these vegetables: {', '.join(selected_vegetables)}. Include ingredients, instructions, and cooking time for each recipe."
    response = model.generate_content(prompt)
    return response.text

st.title("What should I cook today?")

if 'recipe_dict' not in st.session_state:
    st.session_state.recipe_dict = {}

if 'show_recipe' not in st.session_state:
    st.session_state.show_recipe = False

if st.button("Surprise Me!"):
    selected_recipe = random.choice(surprise_recipe_names)
    st.session_state.selected_recipe = selected_recipe
    st.subheader("Here's a surprise recipe for you:")
    st.write(selected_recipe)
    st.session_state.show_recipe = False

if 'selected_recipe' in st.session_state:
    if st.button("Show/Hide Recipe"):
        st.session_state.show_recipe = not st.session_state.show_recipe
        if st.session_state.show_recipe and st.session_state.selected_recipe not in st.session_state.recipe_dict:
            recipe_text = generate_recipe(st.session_state.selected_recipe)
            st.session_state.recipe_dict[st.session_state.selected_recipe] = recipe_text

    if st.session_state.show_recipe:
        st.subheader(st.session_state.selected_recipe)
        st.write(st.session_state.recipe_dict[st.session_state.selected_recipe])

st.subheader("Select 2-3 South Indian vegetables:")
vegetables = ["Tomato", "Onion", "Okra", "Eggplant", "Cucumber", "Carrot", "Green Beans", "Spinach", "Potato", "Bell Pepper"]
selected_vegetables = st.multiselect("Choose vegetables", vegetables)

if len(selected_vegetables) >= 2 and len(selected_vegetables) <= 3:
    if st.button("Generate Recipes"):
        recipes = generate_recipes_from_vegetables(selected_vegetables)
        st.subheader("Here are 2 recipes based on your selection:")
        st.write(recipes)
else:
    st.write("Please select 2-3 vegetables.")
