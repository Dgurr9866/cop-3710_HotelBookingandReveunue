import oracledb
from pathlib import Path

# --- SETUP FOR TEXT PROMPTS---
Table_names = ["Hotel",
               "Guest",
               "Room Type",
               "Cancellation Reason",
               "Reservation",
               "Rate Plan",
               "Reservation Room",
               "Reservation Cancellation",
               "Rate Calendar",
               "Payment Transaction"
               ]

Table_contents = ["hotel_id, hotel_name, hotel_type, city, is_active",
                  "guest_id, first_name, last_name, email, phone, country_code, created_at",
                  "room_type_id, hotel_id, room_type_code, room_type_name, max_occupancy, total_inventory, is_active",
                  "cancellation_reason_id, reason_code, reason_description, active_flag",
                  "reservation_id, guest_id, hotel_id, booking_date, check_in_date, check_out_date, reservation_status, lead_time_days, market_segment, distribution_channel, adr_booked, customer_type",
                  "rate_plan_id, room_type_id, rate_plan_name, meal_plan, deposit_type, refundable_flag, is_active",
                  "reservation_id, room_type_id, qty_rooms, adults_count, babies_count, booked_unit_rate, special_requests_count",
                  "reservation_id, cancellation_reason_id, canceled_at, canceled_by_user_group, cancellation_note",
                  "rate_plan_id, rate_date, nightly_rate, min_stay, max_sell_rooms, closed_to_arrival",
                  "payment_id, reservation_id, payment_datetime, amount, payment_type, payment_status, reference_no"
                  ]

# File locations
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

conn = None
cursor = None


def connect_to_db():
    global conn, cursor
    try:
        # Connection
        # Initialize Thick Mode (Required for FreeSQL/Cloud)
        LIB_DIR ="/Users/gabrielagurr/Downloads/instantclient_23_3"
        oracledb.init_oracle_client(lib_dir=LIB_DIR)

        connection = oracledb.connect(
            user=input("Please Enter Your Username: "),
            password=input("Please Enter Your Password: "),
            host="db.freesql.com",
            port=1521,
            service_name="23ai_34ui2"
        )

        print("Successfully connected to Oracle Database")
        cursor = connection.cursor()

        # start user interface loop
        interface_options_text()
        while interface(input("Select a feature 1-5: ")):
            pass

    except Exception as e:
        print(f"Error during connection: {e}")
        if 'conn' in locals():
            conn.rollback()  # Undo changes if an error occurs

    #finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

def execute_query(query):
    pass

# call to match user_input into the function that will provide the chose feature
def interface(user_input):

    match user_input:
        case "1":
            interface_option_1()
        case "2":
            interface_option_2()
        case "3":
            interface_option_3()
        case "4":
            interface_option_4()
        case "5":
            interface_option_5()
        case _:
            return False

    #return true to continue the interface loop
    return True


def interface_options_text():
    print("Select an option: \n", "1. Room types at every hotel\n", "2. Reservations between two dates\n", "3. Total visits per guest\n", "4. Cancellations grouped by hotel\n", "5. Gross income per hotel\n", "Any other input to exit\n")

def interface_option_1():
    # Room Types at every Hotel
    option_sql = "SELECT rt.room_type_name, rt.room_type_code, ht.hotel_name FROM room_type rt JOIN hotel ht ON rt.hotel_id = ht.hotel_id GROUP BY ht.hotel_name, rt.hotel_id, rt.room_type_name, rt.room_type_code"

    global cursor
    cursor.execute(option_sql)

    # Fetch results
    print(f"Room Type,      Room Code,      Hotel Name")
    for row in cursor:
        print(f"{row[0]:<15} {row[1]:<15} {row[2]:<15}")

def interface_option_2():
    start_range = input("Please enter the start of the date range (YYYY-MM-DD): ")
    end_range = input("Please enter the end of the date range (YYYY-MM-DD): ")

    option_sql = "SELECT rv.reservation_id, rv.hotel_id FROM reservation rv WHERE rv.check_in_date BETWEEN TO_DATE('"
    option_sql += start_range
    option_sql += "', 'YYYY-MM-DD') AND TO_DATE('"
    option_sql += end_range
    option_sql += "', 'YYYY-MM-DD')"

    global cursor
    cursor.execute(option_sql)

        # Fetch results
    print(f"Reservation ID, Hotel ID Between {start_range} and {end_range}")
    for row in cursor:
        print(f"{row[0]:<15} {row[1]:<15}")

def interface_option_3():
    option_sql = "SELECT gt.first_name, gt.last_name, count(rv.reservation_id) AS visits FROM guest gt JOIN reservation rv ON gt.guest_id = rv.guest_id GROUP BY gt.first_name, gt.last_name"

    global cursor
    cursor.execute(option_sql)

    # Fetch results
    print(f"First Name,     Last Name,      Visit Count")
    for row in cursor:
        print(f"{row[0]:<15} {row[1]:<15} {row[2]:<15}")

def interface_option_4():
    option_sql = "SELECT ht.hotel_name, COUNT(rc.cancellation_reason_id) AS cancel_reason FROM hotel ht JOIN reservation rv ON ht.hotel_id = rv.hotel_id JOIN reservation_cancellation rc ON rv.reservation_id = rc.reservation_id GROUP BY ht.hotel_name ORDER BY cancel_reason DESC"

    global cursor
    cursor.execute(option_sql)

    # Fetch results
    print(f"Hotel Name,                    Cancellation Count")
    for row in cursor:
        print(f"{row[0]:<30} {row[1]:<20}")

def interface_option_5():
    option_sql = "SELECT ht.hotel_name, SUM(pt.amount) AS gross_income FROM hotel ht JOIN reservation rv ON ht.hotel_id = rv.hotel_id JOIN payment_transaction pt ON rv.reservation_id = pt.reservation_id GROUP BY ht.hotel_name ORDER BY gross_income DESC"

    global cursor
    cursor.execute(option_sql)

    # Fetch results
    print(f"Hotel Name,                    Gross Income")
    for row in cursor:
        print(f"{row[0]:<30} {row[1]:<15}")

#Start
connect_to_db()


