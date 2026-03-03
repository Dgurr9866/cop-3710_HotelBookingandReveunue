# Hotel Booking and Revenue Management ER Diagram

## User Groups
- Front Desk / Reservation Agent
- Revenue Manager
- Hotel / Operations Manager

## ER Diagram

![Hotel Booking ERD](image/hotel_booking_erd.png)


## Final Normalized Relational Schema

**HOTEL**(hotel_id PK, hotel_name, hotel_type, city, is_active)
**GUEST**(guest_id PK, first_name, last_name, email, phone, country_code, created_at)
**ROOM_TYPE**(room_type_id PK, hotel_id FK, room_type_code, room_type_name, max_occupancy, total_inventory, is_active)
**RESERVATION**(reservation_id PK, guest_id FK, hotel_id FK, booking_date, check_in_date, check_out_date, reservation_status, lead_time_days, market_segment, distribution_channel, adr_booked, customer_type)
**RESERVATION_ROOM**(reservation_id PK,FK, room_type_id PK, FK, qty_rooms, adults_count, babies_count, booked_unit_rate, special_requests_count)
**CANCELLATION_REASON**(cancellation_reason_id PK, reason_code, reason_description, active_flag)
**RESERVATION_CANCELLATION**(reservation_id PK, FK, cancellation_reason_id FK, canceled_at, canceled_by_user_group, cancellation_note)
**RATE_CALENDAR**(rate_plan_id PK, FK, rate_date PK, nightly_rate, min_stay, max_sell_rooms, closed_to_arrival)
**RATE_PLAN**(rate_plan_id PK, room_type_id FK, rate_plan_name, meal_plan, refundable_flag, is_active)
**PAYMENT_TRANSACTION**(payment_id PK, reservation_id FK, payment_datetime, amount, payment_type, payment_status, reference_no)

**All relations are in BCNF**