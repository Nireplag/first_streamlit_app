import streamlit as stm
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

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
try:
  fruit_choice = stm.text_input('What fruit would you like information about?')
  if not fruit_choice:
    stm.error("Please select a fruit to get information.")
  else:
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    stm.dataframe(fruityvice_normalized)
    
execpt URLError as e:
  stm.error()

# do not run anything past here while we troubleshoot
stm.stop()

my_cnx = snowflake.connector.connect(**stm.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM fruit_load_list")
my_data_rows = my_cur.fetchall()
stm.header("The fruit load list contains:")
stm.dataframe(my_data_rows)

# allow the user to add a fruit to the list
add_my_fruit = stm.text_input('What fruit would you like to add?')
stm.write('Thanks for adding ', add_my_fruit)
