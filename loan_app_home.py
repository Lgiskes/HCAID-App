import streamlit as st
import pickle
from sklearn.tree import DecisionTreeClassifier

CurrentPage = ''

def getContent(args = [''], page = "Home"):
    if (page == "Home"):
        home_page(args)

    elif (page == "About"):
        about_page(args)

    elif (page == "Predict Page"):
        predict_page(args)

    elif page == "Form Page":
        form_page(args)

    elif page == "Result Page":
        result_page(args)

def home_page(args = ['']):
    global CurrentPage
    st.title("See if your ideal loan is possible!")

    if st.button("Want to know more?"):
        send_args = ["Hello", 1]
        getContent(args = send_args, page="About")

    if st.button('Get started here!'):
        getContent(page="Form Page")

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


def about_page(args = ['']):
    global CurrentPage
    st.write("Some information about the app")
    if st.button("Go back"):
        CurrentPage = "Home"
        getContent(page = "Home")

def form_page(args = ['']):
    global CurrentPage
    st.write("Insert some data")
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
            st.write(input)
            approval_model = pickle.load(open("approval_model.sav", 'rb'))
            newloan_model = pickle.load(open("newloan_model.sav", 'rb'))
            approve_predict = approval_model.predict([input])

            st.write(approve_predict[0])

            if(approve_predict[0] == 'N'):
                loan_predict = newloan_model.predict([input2])
                st.write(loan_predict[0])






def result_page(args = ['']):
    approval_model = pickle.load(open("approval_model.sav", 'rb'))
    newloan_model = pickle.load(open("newloan_model.sav", 'rb'))
    st.write(args)

def predict_page(args = ['']):
    input_approval = args
    input_newloan = args
    approval_model = pickle.load(open("approval_model.sav", 'rb'))
    newloan_model = pickle.load(open("newloan_model.sav", 'rb'))
    #input_approval = [[165, 360, 0, 6567, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1]]
    result_approval = approval_model.predict([input_approval])
    st.write(input_approval)
    st.write(result_approval)

    if (result_approval[0] == 'N'):
        #input_newloan = [[360, 0, 6567, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1]]
        result_newloan = newloan_model.predict([input_newloan])
        st.write(input_newloan)
        st.write(result_newloan)

    if st.button("Go back"):
        CurrentPage = "Home"
        getContent()

home_page()
form_page()



