import streamlit as st
import mysql.connector
import pandas as pd
import datetime

st.set_page_config(page_title = "EMPLOYEE MANAGEMENT SYSTEM", page_icon = "https://cdn-icons-png.flaticon.com/512/2553/2553157.png")
st.title("EMPLOYEE MANAGEMENT SYSTEM")

#creating a dropdown menu in the website
#st.video("https://youtube.com/shorts/v1RU0kvHczc?si=XvgBbbKuq49HP8aV")
choice = st.sidebar.selectbox("My Menu", ("Home", "Employee Login", "Admin Login","Read books of ems", "Help & Documentation"))
if (choice == "Home"):
    st.write("Welcome to the Employee Management Web Portal")
    st.markdown("<center><h1>WELCOME</h1><center>", unsafe_allow_html=True)
    st.image("https://dengsolutions.com/deng_A478Erd/images/employee.png")
elif (choice == "Employee Login"):
    if 'login' not in st.session_state:
        st.session_state['login'] = False
    uid = st.selectbox("Are you an existing user: ", ("Yes","No"))
    if (uid == "Yes"):
        user_id = st.text_input("Enter your employee id: ")
        user_pwd = st.text_input("Enter your password: ")
        btn = st.button("Login")
            
        if btn:
            mydb = mysql.connector.connect(host = "localhost", user = "root", password = "12345", database = "ems")
            c = mydb.cursor()
            c.execute("select * from userss")
            for r in c:
                if (r[0] == user_id and r[1] == user_pwd):
                    st.session_state['login'] = True
                    break

            if (not st.session_state['login']):
                st.write("Incorrect ID or Password")
        if (st.session_state['login']):
            st.write("Login Successful")
            choice2 = st.selectbox("Features", ("None", "View all employees", "Search for an employee", "Mark Attendance"))
            if (choice2== "View all employees"):
                mydb = mysql.connector.connect(host = "localhost", user = "root", password = "12345", database = "ems")
                e = mydb.cursor()
                df = pd.read_sql("select * from employee", mydb)
                st.dataframe(df)
            elif (choice2 == "Search for an employee"):
            
                user_idd = st.text_input("Enter the employee ID you want to search for")
                first_name = st.text_input("Enter the employee first name you want to search for")
                btn3 = st.button("Search For The Employee")
                if btn3:
                    iid = str(datetime.datetime.now())
                    mydb = mysql.connector.connect(host = "localhost", user = "root", password = "12345", database = "ems")
                    f = mydb.cursor()
                    f.execute("select * from employee")
                    for h in f:
                        if (h[2] == user_idd and h[0] == first_name):
                            st.session_state['login'] = True
                            break
                            
                        if (not st.session_state['login']):
                            st.write("Employee Not Found")
                            
                    if (st.session_state['login']):
                        st.write("Employee Found")

            elif (choice2 == "Mark Attendance"):
                st.subheader("Attendance System")

                today = datetime.date.today()
                now_time = datetime.datetime.now().time()

                # Check In
                if st.button("Check In"):
                    mydb = mysql.connector.connect(host="localhost", user="root", password="12345", database="ems")
                    c = mydb.cursor()

                    # Check if already checked in today
                    c.execute(
                        "SELECT * FROM attendance WHERE employee_id=%s AND date=%s",(user_id, today))
                    record = c.fetchone()

                    if record:
                        st.warning("Already checked in today.")
                    else:
                        c.execute("INSERT INTO attendance (employee_id, date, check_in) VALUES (%s, %s, %s)",(user_id, today, now_time))
                        mydb.commit()
                        st.success("Checked in successfully!")

                # Check Out
                if st.button("Check Out"):
                    mydb = mysql.connector.connect(host="localhost", user="root", password="12345", database="ems")
                    c = mydb.cursor()

                    # Check if already checked in
                    c.execute("SELECT * FROM attendance WHERE employee_id=%s AND date=%s",(user_id, today))
                    record = c.fetchone()

                    if record:
                        if record[4] is not None:
                            st.warning("Already checked out today.")
                        else:
                            c.execute("UPDATE attendance SET check_out=%s WHERE employee_id=%s AND date=%s",(now_time, user_id, today))
                            mydb.commit()
                            st.success("Checked out successfully!")
                    else:
                        st.warning("You must check in before checking out.")

                        
                    

elif (choice == "Admin Login"):
    st.subheader("View Employee Attendance Records")

    choice_admin = st.selectbox("Choose Admin Action",("None", "View Attendance Records"))
    btn_5 = st.button("View Attendance Records")
    

    if (btn_5):
        mydb = mysql.connector.connect(host="localhost", user="root", password="12345", database="ems")
        df = pd.read_sql("SELECT * FROM attendance", mydb)
        st.dataframe(df)


elif (choice == "Read books of ems"):
    choice3 = st.selectbox("Choose Book to read",("Employee Management System"))
    btn4 = st.button ("Read")
    if (btn4):
        st.markdown("<iframe src = 'https://lnu.diva-portal.org/smash/get/diva2:204828/FULLTEXT01.pdf ' width = '100%' height = '500px'></iframe>", unsafe_allow_html = True)
    
elif (choice == "Help & Documentation"):
    st.title("📖 Help & Documentation")

    st.markdown("""
    ## About This System
    The Employee Management System (EMS) is a web application designed to help employees and administrators manage employee-related data efficiently. It allows viewing employees, searching, marking attendance, and reading EMS resources.

    ---

    ## How to Login

    **Employee Login:**
    - Select "Employee Login" from the sidebar.
    - Choose "Yes" if you’re an existing user.
    - Enter your Employee ID and Password.
    - Click "Login."

    **Admin Login:**
    - Select "Admin Login" from the sidebar.

    ---

    ## Features Available

    **View All Employees:**
    - Displays a table of all employee records.

    **Search for an Employee:**
    - Search employees using Employee ID and Name.

    **Mark Attendance:**
    - Check in or check out for the current day.
    - Accessible after logging in as an employee.

    **Read Books of EMS:**
    - Access EMS resources and documentation in PDF format.

    ---

    ## Frequently Asked Questions

    **Q: I forgot my password. What do I do?**
    > Contact the administrator to reset your credentials.

    **Q: Can I edit my employee details?**
    > Not yet, but this feature is coming soon!

    **Q: How do I mark my attendance?**
    > Login as an employee, choose “Mark Attendance,” and click Check In or Check Out.

    ---

    ## Contact Information

    - Email: support@ems.com
    - Phone: +91-6725628891
    """)

    st.success("We’re here to help you navigate EMS smoothly!")
