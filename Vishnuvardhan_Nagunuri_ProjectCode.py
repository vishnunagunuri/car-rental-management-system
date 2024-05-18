# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 17:32:42 2024

@author: nagun
"""
import mysql.connector as connector
import decimal;
from datetime import datetime
import streamlit as st

class CarRental:
    def __init__(self):
        self.con = connector.connect(
            host="localhost",
            port="3306",
            user="root",
            password="Vishnu123!",
            database="car_rental"
        )
        # create table
        query = 'create table if not exists CAR(REGISTRATION_NUMBER CHAR(7) NOT NULL,MODEL_NAME VARCHAR(25) NOT NULL,MAKE VARCHAR(25) NOT NULL,MODEL_YEAR DECIMAL(4) NOT NULL,MILEAGE INTEGER NOT NULL,CAR_CATEGORY_NAME VARCHAR(25) NOT NULL,LOC_ID CHAR(4) NOT NULL,AVAILABILITY_FLAG CHAR(1) NOT NULL,CONSTRAINT CARPK PRIMARY KEY (REGISTRATION_NUMBER))'
        cur = self.con.cursor()
        cur.execute(query)
    
    def insert_car(self, REGISTRATION_NUMBER, MODEL_NAME, MAKE, MODEL_YEAR, MILEAGE, CAR_CATEGORY_NAME, LOC_ID, AVAILABILITY_FLAG):
        try:
            # Check if the car with the given registration number already exists
            cur = self.con.cursor()
            cur.execute("SELECT 1 FROM CAR WHERE REGISTRATION_NUMBER = %s", (REGISTRATION_NUMBER,))
            if cur.fetchone():
                return ("Car with the same registration number already exists.")
            
            # Insert the car data into the database
            query = "INSERT INTO CAR(REGISTRATION_NUMBER, MODEL_NAME, MAKE, MODEL_YEAR, MILEAGE, CAR_CATEGORY_NAME, LOC_ID, AVAILABILITY_FLAG) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            values = (REGISTRATION_NUMBER, MODEL_NAME, MAKE, MODEL_YEAR, MILEAGE, CAR_CATEGORY_NAME, LOC_ID, AVAILABILITY_FLAG)
            cur.execute(query, values)
            self.con.commit()
            return "Car added to database successfully."
        except connector.Error as e:
            return "An error occurred while inserting the car into the database:", e


    # read data
    def read_car(self):
        try:
            query = "SELECT * FROM CAR"
            cur = self.con.cursor()
            cur.execute(query)
            cars = cur.fetchall()  # Fetch all rows from the result set
            # for row in cars:
            #     print(row[0])
            return cars
        except Exception as e:
            print("An error occurred while reading car data:", e)
            return None  # Return None in case of error
   
    # delete car
    def delete_car(self, REGISTRATION_NUMBER):
        try:
            query = "DELETE FROM CAR WHERE REGISTRATION_NUMBER = %s"
            cur = self.con.cursor()
            cur.execute(query, (REGISTRATION_NUMBER,))
            self.con.commit()
            if cur.rowcount > 0:
                return "Car with registration number {} deleted successfully".format(REGISTRATION_NUMBER)
            else:
                return "No car found with registration number {}".format(REGISTRATION_NUMBER)
        except connector.Error as e:
            print("An error occurred:", e)

    # update car details
    def update_car(self, REGISTRATION_NUMBER, MODEL_NAME=None, MAKE=None, MODEL_YEAR=None, MILEAGE=None, CAR_CATEGORY_NAME=None, LOC_ID=None, AVAILABILITY_FLAG=None):
        try:
            update_fields = []
            values = []

            if MODEL_NAME is not None:
                update_fields.append("MODEL_NAME = %s")
                values.append(MODEL_NAME)
            if MAKE is not None:
                update_fields.append("MAKE = %s")
                values.append(MAKE)
            if MODEL_YEAR is not None:
                update_fields.append("MODEL_YEAR = %s")
                values.append(MODEL_YEAR)
            if MILEAGE is not None:
                update_fields.append("MILEAGE = %s")
                values.append(MILEAGE)
            if CAR_CATEGORY_NAME is not None:
                update_fields.append("CAR_CATEGORY_NAME = %s")
                values.append(CAR_CATEGORY_NAME)
            if LOC_ID is not None:
                update_fields.append("LOC_ID = %s")
                values.append(LOC_ID)
            if AVAILABILITY_FLAG is not None:
                update_fields.append("AVAILABILITY_FLAG = %s")
                values.append(AVAILABILITY_FLAG)

            if not update_fields:
                return "No fields provided for update"

            query = "UPDATE CAR SET {} WHERE REGISTRATION_NUMBER = %s".format(", ".join(update_fields))
            values.append(REGISTRATION_NUMBER)

            cur = self.con.cursor()
            cur.execute(query, tuple(values))
            self.con.commit()
            
            if cur.rowcount > 0:
                return "Car details updated successfully"
            else:
                return "No car found with registration number {}".format(REGISTRATION_NUMBER)
        except connector.Error as e:
            print("An error occurred:", e)


class Billing:
    def __init__(self):
        self.con = connector.connect(
            host="localhost",
            port="3306",
            user="root",
            password="Vishnu123!",
            database="car_rental"
        )
        # create table
    def get_all_bills(self):
        try:
            query="SELECT * FROM BILLING_DETAILS"
            cur=self.con.cursor()
            cur.execute(query)
            bills=cur.fetchall()
            return bills
        except Exception as e:
            print("An error occurred while reading bills:", e)
            return None  # Return None in case of error
    def create_final_bill(self, booking_id):
        try:
            # Check if the database connection is available
            if not self.con:
                print("Error: MySQL Connection not available.")
                return
             # Check if a bill with the same booking ID already exists
            cur = self.con.cursor()
            cur.execute("SELECT COUNT(*) FROM billing_details WHERE booking_id = %s", (booking_id,))
            existing_bills_count = cur.fetchone()[0]
            if existing_bills_count > 0:
                print("Bill already exists for the booking ID:", booking_id)
                return
            # Generate bill ID
            def generate_bill_ID():
                try:
                    # Query to get the last bill number from billing_details table
                    query = "SELECT bill_ID FROM billing_details ORDER BY bill_ID DESC LIMIT 1"
                    cur = self.con.cursor()
                    cur.execute(query)
                    last_bill_ID = cur.fetchone()

                    if last_bill_ID:
                        # Extract numeric part of the last bill number
                        last_bill_ID_numeric = int(last_bill_ID[0][2:])
                        # Increment the numeric part
                        new_bill_ID_numeric = last_bill_ID_numeric + 1
                        # Generate the new bill number by concatenating "BL" with the incremented numeric part
                        new_bill_ID = f"BL{new_bill_ID_numeric:04d}"  # Format to ensure 4 digits after "BL"
                    else:
                        # If no previous bill numbers exist, start with BL1001
                        new_bill_ID = "BL1001"

                    return new_bill_ID
                
                except Exception as e:
                    print("Error generating bill number:", e)
                    return None
            bill_id=generate_bill_ID()
            # Get current date for bill_date
            bill_date = datetime.now().date()

            # Fetch necessary values
            def fetch_booking_data():
                try:
                    query = "SELECT amount, RET_DT_TIME, ACT_RET_DT_TIME, discount_code FROM booking_details WHERE Booking_id = %s"
                    cur = self.con.cursor()
                    cur.execute(query, (booking_id,))
                    return cur.fetchone()
                except Exception as e:
                    print("Error fetching booking data:", e)
                    return None

            booking_data = fetch_booking_data()

            if not booking_data:
                print("No booking data found.")
                return

            initial_amount = decimal.Decimal(booking_data[0])
            Return_Date = booking_data[1]
            Act_Return_Date = booking_data[2]
            discount_code = booking_data[3]

            # Calculate discount amount
            def calculate_discount_amount():
                try:
                    if not discount_code:
                        return decimal.Decimal('0.00')

                    query = "SELECT Discount_percentage FROM discount_details WHERE discount_code = %s"
                    cur = self.con.cursor()
                    cur.execute(query, (discount_code,))
                    discount_percentage = cur.fetchone()


                    return initial_amount * (decimal.Decimal(discount_percentage[0]) / 100)
                except Exception as e:
                    print("Error calculating discount amount:", e)
                    return None

            discount_amount = calculate_discount_amount()

            # Calculate late fee
            def calculate_late_fee():
                try:
                    # Fetch Return Date, Actual Return Date, and Late fee per hour
                    query = "SELECT BD.RET_DT_TIME, BD.ACT_RET_DT_TIME, CC.LATE_FEE_PER_HOUR FROM BOOKING_DETAILS AS BD JOIN CAR AS C ON BD.REG_NUM = C.REGISTRATION_NUMBER JOIN CAR_CATEGORY AS CC ON C.CAR_CATEGORY_NAME = CC.CATEGORY_NAME WHERE BD.Booking_id = %s"
                    cur = self.con.cursor()
                    cur.execute(query, (booking_id,))
                    result = cur.fetchone()
                    if result:
                        Return_Date = result[0]
                        Act_Return_Date = result[1]
                        LatefeePerHR = float(result[2])
                    else:
                        print("No Details Found")
                        return None
            
                    # Check if Return_Date and Act_Return_Date are not None
                    if Return_Date and Act_Return_Date:
                    # Calculate late fee if actual return is later than expected return
                        if Act_Return_Date > Return_Date:
                            hour_difference = (Act_Return_Date - Return_Date).total_seconds() / 3600
                            late_fee = hour_difference * LatefeePerHR
                            return late_fee
                        else:
                            late_fee = decimal.Decimal(0.0)
                            return late_fee
                    else:
                        print("Error: Return date or actual return date is None")
                        return None
                except Exception as e:
                    print("Error calculating late fee:", e)
                    return None
            # Calculate amount before tax
            late_fee=calculate_late_fee()
            amount_before_tax = decimal.Decimal(initial_amount) + decimal.Decimal(late_fee) - decimal.Decimal(discount_amount)
            amount_before_tax=round(amount_before_tax,2)

            # Calculate total tax
            def calculate_total_tax():
                try:
                    tax_rate = decimal.Decimal('0.065')  # Tax rate of 6.5%
                    return amount_before_tax * tax_rate
                except Exception as e:
                    print("Error calculating total tax:", e)
                    return None

            total_tax = calculate_total_tax()
            total_tax=round(total_tax,2)


            # Calculate final amount
            final_amount = amount_before_tax + total_tax
            final_amount=round(final_amount,2)
            try:
                query="SELECT CD.FNAME,CD.MNAME,CD.LNAME FROM BOOKING_DETAILS AS BD JOIN CUSTOMER_DETAILS AS CD ON CD.DL_NUMBER=BD.DL_NUM WHERE BOOKING_ID=%s"
                cur=self.con.cursor()
                cur.execute(query,(booking_id,))
                result=cur.fetchone()
                if result:
                    f_name=result[0]
                    m_name=result[1]
                    l_name=result[2]
                else:
                    return "Name Not Found" 
                full_name = f"{f_name} {' ' + m_name if m_name else ''} {l_name}"
            except Exception as e:
                    print("Error calculating late fee:", e)
                    return None


            # Insert into billing_details table
            query = "INSERT INTO billing_details (bill_ID, bill_date,full_name, booking_id,amount, discount_amount, total_late_fee, total_tax, final_amount) VALUES (%s, %s, %s,%s, %s, %s, %s, %s, %s)"
            values = (bill_id, bill_date,full_name, booking_id,initial_amount, discount_amount, late_fee, total_tax, final_amount)
            cur = self.con.cursor()
            cur.execute(query, values)
            self.con.commit()
            
            bill_details = {
            'Bill_ID': bill_id,  # Example bill ID
            'Bill_Date': bill_date,  # Example bill date
            'Full_Name':full_name,
            'Booking_ID': booking_id,
            'Amount':initial_amount,
            'Discount_Amount': discount_amount,  # Example initial amount
            'Total_Late_Fee': late_fee,  # Example late fee
            'Total_Tax': total_tax,  # Example total tax
            'Final_Amount': final_amount  # Example final amount
            }

            return bill_details
        except Exception as e:
            print("Error generating bill:", e)
            return None

billing=Billing()
billing.get_all_bills()


car_rental = CarRental()
bill_generate = Billing()

def index():
    st.title("Car Rental Management System")

def generate_bill():
    st.title("Manage Bills")
    booking_id = st.text_input("Enter Booking ID")
    if st.button("Generate Bill"):
        output = bill_generate.create_final_bill(booking_id)
        if output:
            st.write(output)
        else:
            st.error(f"Bill already exists for Booking ID: {booking_id}")
    bills=bill_generate.get_all_bills()
    if bills:
        bill_table=[]
        for bill in bills:
            bill_row = [bill[0], bill[1], bill[2], bill[3], bill[4],bill[5],bill[6],bill[7],bill[8]]
            bill_table.append(bill_row)
        
        bill_table.insert(0,['Bill ID','Bill Date','full_name','Booking ID','Amount','Discount Amount','Late Fee','Total Tax','Final Amount'])    
        st.table(bill_table)
    else:
        st.write("No Bills Available")    


import streamlit as st

def manage_cars():
    st.title("Manage Cars")
    cars = car_rental.read_car()
    filtered_cars = None  # Initialize filtered_cars variable

    if cars:
        filter_option = st.selectbox(
            "Filter cars by:",
            ["Brand", "Type"]
        )

        if filter_option == "Brand":
            brand = st.text_input("Enter brand:")
            filtered_cars = [car for car in cars if car[2].lower() == brand.lower()]
            # if filtered_cars:
            #     st.table(filtered_cars)
            # else:
            #     st.write("No cars found with the specified brand.")
        elif filter_option == "Type":
            car_type = st.text_input("Enter car type:")
            filtered_cars = [car for car in cars if car[5].lower() == car_type.lower()]
            # if filtered_cars:
            #     st.table(filtered_cars)
            # else:
            #     st.write("No cars found with the specified type.")
    else:
        st.write("No cars available.")

    # Option to clear search and display all rows
    if st.button("Clear Search"):
        filtered_cars = None

    # Display filtered cars or all cars
    if filtered_cars:
        st.header("Filtered Cars")
        st.table(filtered_cars)
    elif cars:
        st.header("All Available Cars")
        st.table(cars)

    st.header("Manage Cars Options")

    option = st.selectbox(
        "Select an option:",
        ["Add Car", "Update Car", "Delete Car"]
    )

    if option == "Add Car":
        add_car()
    elif option == "Update Car":
        update_car()
    elif option == "Delete Car":
        delete_car()


    
def add_car():
    st.title("Add Car")
    registration_number = st.text_input("Registration Number")
    model_name = st.text_input("Model Name")
    make = st.text_input("Make")
    model_year = st.text_input("Model Year")
    mileage = st.text_input("Mileage")
    car_category_name = st.text_input("Car Category Name")
    loc_id = st.text_input("Location ID")
    availability_flag = st.text_input("Availability Flag")
    if st.button("Add Car"):
        output = car_rental.insert_car(registration_number, model_name, make, model_year, mileage, car_category_name, loc_id, availability_flag)
        st.write(output)

def display_cars():
    st.title("Manage Cars")
    st.header("Available Cars")
    cars = car_rental.read_car()
    if cars:
        # Display the list of cars in a tabular format
        st.table(cars)
    else:
        st.write("No cars available.")


def delete_car():
    st.title("Delete Car")
    registration_number = st.text_input("Enter Registration Number")
    if st.button("Delete Car"):
        output=car_rental.delete_car(registration_number)
        st.write(output)

def update_car():
    st.title("Update Car")
    registration_number = st.text_input("Registration Number")
    model_name = st.text_input("Model Name")
    make = st.text_input("Make")
    model_year = st.text_input("Model Year")
    mileage = st.text_input("Mileage")
    car_category_name = st.text_input("Car Category Name")
    loc_id = st.text_input("Location ID")
    availability_flag = st.text_input("Availability Flag")
    if st.button("Update Car"):
        output=car_rental.update_car(registration_number, model_name, make, model_year, mileage, car_category_name, loc_id, availability_flag)
        st.write(output)

def main():
    pages = {
        "Index": index,
        "Manage Bills": generate_bill,
        "Manage Cars": manage_cars,
    }
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(pages.keys()))
    pages[selection]()

if __name__ == "__main__":
    main()

