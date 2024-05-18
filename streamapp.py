import streamlit as st
from carrental import CarRental
from billing import Billing

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
