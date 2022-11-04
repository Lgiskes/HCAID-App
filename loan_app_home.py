import streamlit as st
import pickle
from sklearn.tree import DecisionTreeClassifier
import matplotlib

CurrentPage = ''

def getContent(args = [''], page = "Home"):
    if (page == "Home"):
        home_page(args)

    elif (page == "About"):
        about_page(args)

    elif (page == "Predict Page"):
        predict_page(args)


def home_page(args = ['']):
    global CurrentPage
    st.title("See if your ideal loan is possible!")
    st.write("Have you wanted to buy yourself a house or a new car but don't have the money? \nThis website will calculate if your ideal loan is possible using artificial intelligence!")

    if st.button("Want to know more?"):
        send_args = ["Hello", 1]
        getContent(args = send_args, page="About")

    if st.button('Get started here!'):
        st.write("Click on the get started page on the left side of the screen to begin")
        getContent(page="Form Page")

def about_page(args = ['']):
    global CurrentPage
    st.write("This app uses artificial intelligence to calculate if your wanted loan will get accepted. The AI has been trained to find patterns in a database of loan requests. \n Please note that this app does not guarantee your loan will get accepted by banks.")
    if st.button("Collapse"):
        CurrentPage = "Home"
        getContent(page = "Home")

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



