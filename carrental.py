# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 17:32:42 2024

@author: nagun
"""

""
import mysql.connector as connector


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

