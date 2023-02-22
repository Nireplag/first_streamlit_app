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
# create functions 
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
  
stm.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = stm.text_input('What fruit would you like information about?')
  if not fruit_choice:
    stm.error("Please select a fruit to get information.")
  else:
    stm.dataframe(get_fruityvice_data(fruit_choice))
    
except URLError as e:
  stm.error()

stm.header("The fruit load list contains:")
# snowflake related functions

def get_fruit_loaded_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from fruity_load_list")
    return my_cur.fetchall()
  
# add a button to load fruit
if stm.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**stm.secrets["snowflake"])
  my_data_rows = get_fruit_loaded_list()
  my_cnx.close()
  stm.dataframe(my_data_rows)

# Allow user to enter fruits to the list
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("INSERT INTO fruit_load_list values ('"+ new_fruit +"')")
    return "Thanks for adding " + new_fruit
  
add_my_fruit = stm.txt_input('What fruit would you like to add?')
if stm.button('Add a fruit to the List'):
  my_cnx = snowflake.connector.connect(**stm.secrets["snowflake"])
  stm.text(insert_row_snowflake(add_my_fruit))
  my_cnx.close()
