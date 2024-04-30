import os
import json
import pandas as pd
import traceback
from src.mcqgenerator.utils import read_file,get_table_data
from src.mcqgenerator.logger import logging
from src.mcqgenerator.MCQgenerator import generate_evaluate_chain
from langchain.callbacks import get_openai_callback
import streamlit as st


#loading json file
with open('C:/Users/sahil pandey/mcqgenr/Response.json','r') as file:
    RESPONSE_JSON=json.load(file)
    #creating teh title for the app
    st.title("MCQs Creator Application with Langchain✒️🍔")

    #create a form using st.form
    with st.form("user_inputs"):
        #file upload
        uploaded_file=st.file_uploader("Upload a PDF or txt file")
        #input fields
        mcq_counts=st.number_input("No.of MCQs",min_value=3,max_value=50)
        #Subject
        subject=st.text_input("Insert Subject",max_chars=20)
        #quiz Tone
        tone=st.text_input("Complexity level of questions",max_chars=20,placeholder="Simple")
        #Add button
        button=st.form_submit_button("Create MCQs")
        #check if the button is clicked and all fields have input

        if button and uploaded_file is not None and mcq_counts and subject and tone:
            with st.spinner("loading..."):
                try:
                    text=read_file(uploaded_file)
                    #count token and cost of API call
                    with get_openai_callback() as cb:
                      response=generate_evaluate_chain(
                      {
                        "text": text,
                        "number": mcq_counts,
                        "subject":subject,
                        "tone": tone,
                        "response_json": json.dumps(RESPONSE_JSON)
                      }
                     )
                      #st.write(response)
                except Exception as e:
                    traceback.print_exception(type(e), e,e.__traceback__)
                    st.error("Error")

                else:
                    print(f"Total Tokens:{cb.total_tokens}")
                    print(f"Prompt Tokens:{cb.prompt_tokens}")
                    print(f"Completion Tokens:{cb.completion_tokens}")
                    print(f"Total Cost:{cb.total_cost}")

                    if isinstance(response,dict):
                        #Extract the quiz data from the response
                        quiz=response.get("quiz",None)
                        if quiz is not None:
                              table_data=get_table_data(quiz)
                              if table_data is not None:
                                  df=pd.DataFrame(table_data)
                                  df.index=df.index+1
                                  st.table(df)
                                  #display the review in atext box as well
                                  st.text_area(label="Review",value=response["review"])
                              else:
                                  st.error("Error in the table data")

                        else:
                           st.write(response)

