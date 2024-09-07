import streamlit as st
import google.generativeai as genai
import os
import random




os.environ['API_KEY'] = st.secrets['API_KEY']
genai.configure(api_key=os.getenv('API_KEY'))

# Initialize Gemini model
model = genai.GenerativeModel('gemini-1.5-flash')


def generate_surprise_recipe():
    prompt = "Generate a south indian recipe typically for lunch/ dinner. Provide the recipe name on the first line, followed by a newline, then the full recipe details including ingredients, instructions, and cooking time."
    response = model.generate_content(prompt)
    return response.text

def split_recipe(recipe_text):
    lines = recipe_text.split('\n', 1)
    recipe_name = lines[0].strip()
    full_recipe = lines[1].strip() if len(lines) > 1 else ""
    return recipe_name, full_recipe

def generate_recipes_from_vegetables(selected_vegetables):
    prompt = f"Generate 2 South Indian recipes using these vegetables, your recipe can just use one the vegetables selected or a combination of vegetables: {', '.join(selected_vegetables)}. Include ingredients, instructions, and cooking time for each recipe."
    response = model.generate_content(prompt)
    return response.text

# Streamlit app
st.title("What should I cook today?")

# Surprise Me button
if st.button("Surprise Me!"):
    full_recipe = generate_surprise_recipe()
    recipe_name, recipe_details = split_recipe(full_recipe)
    st.session_state['recipe_name'] = recipe_name
    st.session_state['recipe_details'] = recipe_details
    st.subheader("Here's a surprise recipe for you:")
    st.write(recipe_name)

# Show me recipe button
if 'recipe_name' in st.session_state and st.button("Show me recipe"):
    st.subheader(st.session_state['recipe_name'])
    st.write(st.session_state['recipe_details'])

# South Indian vegetables selection
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
