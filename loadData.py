import oracledb
import csv
from datetime import datetime
from pathlib import Path



# File locations

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"



# Connection

oracledb.init_oracle_client(
    lib_dir="/Users/gabrielagurr/Downloads/instantclient_23_3"
)

connection = oracledb.connect(
    user="DGURR9866_SCHEMA_DZNHL",
    password="6qAMCTW#2EFI1VW7SHEUEOL0LKVJQ6",
    host="db.freesql.com",
    port=1521,
    service_name="23ai_34ui2"
)

print("Successfully connected to Oracle Database")


# Helper functions

def parse_date(date_str):
    if not date_str or str(date_str).strip() == "":
        return None
    return datetime.strptime(date_str.strip(), "%Y-%m-%d").date()


def parse_timestamp(ts_str):
    if not ts_str or str(ts_str).strip() == "":
        return None
    return datetime.strptime(ts_str.strip(), "%Y-%m-%d %H:%M:%S")



# Load HOTEL

def load_hotel(cursor, filename):
    with open(filename, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute("""
                INSERT INTO HOTEL (
                    hotel_id, hotel_name, hotel_type, city, is_active
                ) VALUES (
                    :1, :2, :3, :4, :5
                )
            """, [
                int(row["hotel_id"]),
                row["hotel_name"],
                row["hotel_type"],
                row["city"],
                row["is_active"]
            ])
    print("HOTEL loaded")



# Load GUEST

def load_guest(cursor, filename):
    with open(filename, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute("""
                INSERT INTO GUEST (
                    guest_id, first_name, last_name, email,
                    phone, country_code, created_at
                ) VALUES (
                    :1, :2, :3, :4, :5, :6, :7
                )
            """, [
                int(row["guest_id"]),
                row["first_name"],
                row["last_name"],
                row["email"],
                row["phone"].strip() if row["phone"] else None,
                row["country_code"].strip() if row["country_code"] else None,
                parse_timestamp(row["created_at"])
            ])
    print("GUEST loaded")



# Load ROOM_TYPE

def load_room_type(cursor, filename):
    with open(filename, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute("""
                INSERT INTO ROOM_TYPE (
                    room_type_id, hotel_id, room_type_code, room_type_name,
                    max_occupancy, total_inventory, is_active
                ) VALUES (
                    :1, :2, :3, :4, :5, :6, :7
                )
            """, [
                int(row["room_type_id"]),
                int(row["hotel_id"]),
                row["room_type_code"],
                row["room_type_name"],
                int(row["max_occupancy"]),
                int(row["total_inventory"]),
                row["is_active"]
            ])
    print("ROOM_TYPE loaded")



# Load CANCELLATION_REASON

def load_cancellation_reason(cursor, filename):
    with open(filename, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute("""
                INSERT INTO CANCELLATION_REASON (
                    cancellation_reason_id, reason_code,
                    reason_description, active_flag
                ) VALUES (
                    :1, :2, :3, :4
                )
            """, [
                int(row["cancellation_reason_id"]),
                row["reason_code"],
                row["reason_description"],
                row["active_flag"]
            ])
    print("CANCELLATION_REASON loaded")


# Load RESERVATION

def load_reservation(cursor, filename):
    with open(filename, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute("""
                INSERT INTO RESERVATION (
                    reservation_id, guest_id, hotel_id, booking_date,
                    check_in_date, check_out_date, reservation_status,
                    lead_time_days, market_segment, distribution_channel,
                    adr_booked, customer_type
                ) VALUES (
                    :1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12
                )
            """, [
                int(row["reservation_id"]),
                int(row["guest_id"]),
                int(row["hotel_id"]),
                parse_date(row["booking_date"]),
                parse_date(row["check_in_date"]),
                parse_date(row["check_out_date"]),
                row["reservation_status"],
                int(row["lead_time_days"]) if row["lead_time_days"] else None,
                row["market_segment"].strip() if row["market_segment"] else None,
                row["distribution_channel"].strip() if row["distribution_channel"] else None,
                float(row["adr_booked"]) if row["adr_booked"] else None,
                row["customer_type"].strip() if row["customer_type"] else None
            ])
    print("RESERVATION loaded")


# Load RATE_PLAN

def load_rate_plan(cursor, filename):
    with open(filename, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute("""
                INSERT INTO RATE_PLAN (
                    rate_plan_id, room_type_id, rate_plan_name,
                    meal_plan, deposit_type, refundable_flag, is_active
                ) VALUES (
                    :1, :2, :3, :4, :5, :6, :7
                )
            """, [
                int(row["rate_plan_id"]),
                int(row["room_type_id"]),
                row["rate_plan_name"],
                row["meal_plan"].strip() if row["meal_plan"] else None,
                row["deposit_type"].strip() if row["deposit_type"] else None,
                row["refundable_flag"],
                row["is_active"]
            ])
    print("RATE_PLAN loaded")



# Load RESERVATION_ROOM

def load_reservation_room(cursor, filename):
    with open(filename, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute("""
                INSERT INTO RESERVATION_ROOM (
                    reservation_id, room_type_id, qty_rooms, adults_count,
                    babies_count, booked_unit_rate, special_requests_count
                ) VALUES (
                    :1, :2, :3, :4, :5, :6, :7
                )
            """, [
                int(row["reservation_id"]),
                int(row["room_type_id"]),
                int(row["qty_rooms"]),
                int(row["adults_count"]),
                int(row["babies_count"]) if row["babies_count"] else 0,
                float(row["booked_unit_rate"]) if row["booked_unit_rate"] else 0,
                int(row["special_requests_count"]) if row["special_requests_count"] else 0
            ])
    print("RESERVATION_ROOM loaded")



# Load RESERVATION_CANCELLATION

def load_reservation_cancellation(cursor, filename):
    with open(filename, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute("""
                INSERT INTO RESERVATION_CANCELLATION (
                    reservation_id, cancellation_reason_id, canceled_at,
                    canceled_by_user_group, cancellation_note
                ) VALUES (
                    :1, :2, :3, :4, :5
                )
            """, [
                int(row["reservation_id"]),
                int(row["cancellation_reason_id"]),
                parse_timestamp(row["canceled_at"]),
                row["canceled_by_user_group"].strip() if row["canceled_by_user_group"] else None,
                row["cancellation_note"].strip() if row["cancellation_note"] else None
            ])
    print("RESERVATION_CANCELLATION loaded")



# Load RATE_CALENDAR

def load_rate_calendar(cursor, filename):
    with open(filename, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute("""
                INSERT INTO RATE_CALENDAR (
                    rate_plan_id, rate_date, nightly_rate, min_stay,
                    max_sell_rooms, closed_to_arrival
                ) VALUES (
                    :1, :2, :3, :4, :5, :6
                )
            """, [
                int(row["rate_plan_id"]),
                parse_date(row["rate_date"]),
                float(row["nightly_rate"]),
                int(row["min_stay"]) if row["min_stay"] else 1,
                int(row["max_sell_rooms"]) if row["max_sell_rooms"] else None,
                row["closed_to_arrival"]
            ])
    print("RATE_CALENDAR loaded")



# Load PAYMENT_TRANSACTION

def load_payment_transaction(cursor, filename):
    with open(filename, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute("""
                INSERT INTO PAYMENT_TRANSACTION (
                    payment_id, reservation_id, payment_datetime, amount,
                    payment_type, payment_status, reference_no
                ) VALUES (
                    :1, :2, :3, :4, :5, :6, :7
                )
            """, [
                int(row["payment_id"]),
                int(row["reservation_id"]),
                parse_timestamp(row["payment_datetime"]),
                float(row["amount"]),
                row["payment_type"],
                row["payment_status"],
                row["reference_no"].strip() if row["reference_no"] else None
            ])
    print("PAYMENT_TRANSACTION loaded")



# Main load sequence


try:
    with connection.cursor() as cursor:
        # load_hotel(cursor, DATA_DIR / "hotel.csv")
        # load_guest(cursor, DATA_DIR / "guest.csv")
        # load_room_type(cursor, DATA_DIR / "room_type.csv")
        # load_cancellation_reason(cursor, DATA_DIR / "cancellation_reason.csv")
        # load_reservation(cursor, DATA_DIR / "reservation.csv")
        # load_rate_plan(cursor, DATA_DIR / "rate_plan.csv")
        # load_reservation_room(cursor, DATA_DIR / "reservation_room.csv")
        # load_reservation_cancellation(cursor, DATA_DIR / "reservation_cancellation.csv")
        # load_rate_calendar(cursor, DATA_DIR / "rate_calendar.csv")
         load_payment_transaction(cursor, DATA_DIR / "payment_transaction.csv")

    connection.commit()
    print("All data loaded successfully.")

except Exception as e:
    connection.rollback()
    print("Error while loading data:")
    print(e)

finally:
    connection.close()
    print("Connection closed.")

