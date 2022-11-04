import webbrowser

import streamlit as st
import pickle
import shap
import matplotlib.pyplot as plt
import pandas as pd

def form_to_input(items):
    input = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    input2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]
    input[0] = items[4]
    input[1] = items[5]
    input[2] = items[6] != 1
    input[3] = items[2]
    input[4] = items[0] != 1
    input[5] = items[0] == 1
    input[6] = items[1] == 0
    input[7] = items[1] == 1
    input[8] = items[1] == 2
    input[9] = items[1] == 3
    input[10] = items[3] != 1
    input[11] = items[3] == 1
    input[12] = items[7] == 0
    input[13] = items[7] == 1
    input[14] = items[7] == 2

    input2[0] = items[5]
    input2[1] = items[6] != 1
    input2[2] = items[2]
    input2[3] = items[0] != 1
    input2[4] = items[0] == 1
    input2[5] = items[1] == 0
    input2[6] = items[1] == 1
    input2[7] = items[1] == 2
    input2[8] = items[1] == 3
    input2[9] = items[3] != 1
    input2[10] = items[3] == 1
    input2[11] = items[7] == 0
    input2[12] = items[7] == 1
    input2[13] = items[7] == 2
    return input, input2

def form_page(args = ['']):
    global CurrentPage
    st.write("Please answer the questions below to find out if your loan will get accepted!\nYour data will not be saved or used for other purposes")
    form = st.form('loan_form')
    with form:
        married_check = st.checkbox("Are you married? (check if yes)")
        dependants_no = st.selectbox("How many people on your household are directly dependant on your income?", ['0', '1', '2', '3+'])
        income = st.number_input("How much euro does your total household make a month?", 0, 20000)
        self_employed_check = st.checkbox("Are you self employed? (check if yes)")
        loan_amount = st.number_input("How much do you want to loan? (in thousand euro)", 1 ,1000)
        loan_length = st.number_input("How long do you want the term of the loan to be in months?", 1, 1000)
        credit_check = st.checkbox("Have you had an bad credit history in the past? (check if yes)")
        area_box = st.selectbox("In what kind of area do you live?", ["Urban","Semi Urban", "Rural"])

        if st.form_submit_button("Make your loan come true!"):
            form_items = [married_check, dependants_no, income, self_employed_check, loan_amount, loan_length, credit_check, area_box]
            input, input2 = form_to_input(form_items)
            #st.write(input)
            approval_model = pickle.load(open("approval_model.sav", 'rb'))
            newloan_model = pickle.load(open("newloan_model.sav", 'rb'))
            approve_predict = approval_model.predict([input])

            xtest = pd.read_csv("pages/xtest.csv")
            xtest = xtest.append(input)
            explainer = shap.Explainer(approval_model.predict, xtest)
            #shap_values = explainer(xtest)


            #st.write(shap.plots.force(shap_values[len(xtest)-1]))
            if(approve_predict[0] == 'N'):
                st.write("Unfortunatly, this loan is not possible ")
                loan_predict = newloan_model.predict([input2])
                st.write("However if you change your loan amount to the amount below, it will be possible!")
                st.write(loan_predict[0])
            else:
                st.write("Your loan is possible")


    if(st.button("Get your loan here!")):
        url = "https://www.independer.nl/geld-lenen/intro.aspx?&refer=adwordslenen-des-TS49&gclid=CjwKCAjw8JKbBhBYEiwAs3sxN80Fh_5Oew35x2EkwMX9_ar59oJZxWsLnXnH_S0I-AapXLFd9u3KuhoCQEIQAvD_BwE&gclsrc=aw.ds"
        webbrowser.open_new_tab(url)
        st.write("If the link button does not work, use the following link instead:")
        st.write(url)




form_page()