import streamlit as stm
import pandas as pd

stm.title("My Parents New Healthy Diner")
stm.header("Breakfast Favorites")
stm.text("🥣 Omega 3 & Bluebarry Oatmeal")
stm.text("🥗 Kale, Spinach & Rocket Smoothie")
stm.text("🐔 Hard-Boiled Free-Range Egg")
stm.text('🥑🍞 Avocado Toast')

stm.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
stm.dataframe(my_fruit_list)
