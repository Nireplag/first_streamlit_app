import streamlit as stm
import pandas as pd
import requests

#import file
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

stm.title("My Parents New Healthy Diner")
stm.header("Breakfast Favorites")
stm.text("🥣 Omega 3 & Bluebarry Oatmeal")
stm.text("🥗 Kale, Spinach & Rocket Smoothie")
stm.text("🐔 Hard-Boiled Free-Range Egg")
stm.text('🥑🍞 Avocado Toast')

stm.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
fruits_selected = stm.multiselect('Pick some fruits:', list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

stm.dataframe(fruits_to_show)

stm.header('Fruityvice Fruit Advice!')
fruit_choice = stm.text_input('What fruit would you like information about?','Kiwi')
stm.write('The user entered ', fruit_choice)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
#stm.text(fruityvice_response.json()) # write json format in screen

# normalize json version of response
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())

# display response as a table
stm.dataframe(fruityvice_normalized)
