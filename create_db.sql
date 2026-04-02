
CREATE TABLE HOTEL (
    hotel_id        NUMBER PRIMARY KEY,
    hotel_name      VARCHAR2(100) NOT NULL,
    hotel_type      VARCHAR2(50)  NOT NULL,
    city            VARCHAR2(80)  NOT NULL,
    is_active       CHAR(1)       DEFAULT 'Y' NOT NULL,
    CONSTRAINT chk_hotel_active
        CHECK (is_active IN ('Y', 'N'))
);


CREATE TABLE GUEST (
    guest_id        NUMBER PRIMARY KEY,
    first_name      VARCHAR2(50)  NOT NULL,
    last_name       VARCHAR2(50)  NOT NULL,
    email           VARCHAR2(100) NOT NULL,
    phone           VARCHAR2(25),
    country_code    VARCHAR2(10),
    created_at      TIMESTAMP     DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT uq_guest_email UNIQUE (email)
);


CREATE TABLE ROOM_TYPE (
    room_type_id        NUMBER PRIMARY KEY,
    hotel_id            NUMBER        NOT NULL,
    room_type_code      VARCHAR2(20)  NOT NULL,
    room_type_name      VARCHAR2(60)  NOT NULL,
    max_occupancy       NUMBER        NOT NULL,
    total_inventory     NUMBER        NOT NULL,
    is_active           CHAR(1)       DEFAULT 'Y' NOT NULL,

    CONSTRAINT fk_room_type_hotel
        FOREIGN KEY (hotel_id)
        REFERENCES HOTEL (hotel_id),

    CONSTRAINT uq_room_type_code_per_hotel
        UNIQUE (hotel_id, room_type_code),

    CONSTRAINT chk_room_type_active
        CHECK (is_active IN ('Y', 'N')),

    CONSTRAINT chk_room_type_max_occ
        CHECK (max_occupancy > 0),

    CONSTRAINT chk_room_type_inventory
        CHECK (total_inventory >= 0)
);


CREATE TABLE RESERVATION (
    reservation_id          NUMBER PRIMARY KEY,
    guest_id                NUMBER         NOT NULL,
    hotel_id                NUMBER         NOT NULL,
    booking_date            DATE           NOT NULL,
    check_in_date           DATE           NOT NULL,
    check_out_date          DATE           NOT NULL,
    reservation_status      VARCHAR2(30)   NOT NULL,
    lead_time_days          NUMBER,
    market_segment          VARCHAR2(40),
    distribution_channel    VARCHAR2(40),
    adr_booked              NUMBER(10,2),
    customer_type           VARCHAR2(40),

    CONSTRAINT fk_reservation_guest
        FOREIGN KEY (guest_id)
        REFERENCES GUEST (guest_id),

    CONSTRAINT fk_reservation_hotel
        FOREIGN KEY (hotel_id)
        REFERENCES HOTEL (hotel_id),

    CONSTRAINT chk_reservation_dates
        CHECK (check_out_date > check_in_date),

    CONSTRAINT chk_reservation_lead_time
        CHECK (lead_time_days >= 0),

    CONSTRAINT chk_reservation_adr
        CHECK (adr_booked >= 0)
);


CREATE TABLE RESERVATION_ROOM (
    reservation_id              NUMBER       NOT NULL,
    room_type_id                NUMBER       NOT NULL,
    qty_rooms                   NUMBER       NOT NULL,
    adults_count                NUMBER       NOT NULL,
    babies_count                NUMBER       DEFAULT 0 NOT NULL,
    booked_unit_rate            NUMBER(10,2) NOT NULL,
    special_requests_count      NUMBER       DEFAULT 0 NOT NULL,

    CONSTRAINT pk_reservation_room
        PRIMARY KEY (reservation_id, room_type_id),

    CONSTRAINT fk_res_room_reservation
        FOREIGN KEY (reservation_id)
        REFERENCES RESERVATION (reservation_id),

    CONSTRAINT fk_res_room_room_type
        FOREIGN KEY (room_type_id)
        REFERENCES ROOM_TYPE (room_type_id),

    CONSTRAINT chk_res_room_qty
        CHECK (qty_rooms > 0),

    CONSTRAINT chk_res_room_adults
        CHECK (adults_count >= 0),

    CONSTRAINT chk_res_room_babies
        CHECK (babies_count >= 0),

    CONSTRAINT chk_res_room_rate
        CHECK (booked_unit_rate >= 0),

    CONSTRAINT chk_res_room_requests
        CHECK (special_requests_count >= 0)
);


CREATE TABLE CANCELLATION_REASON (
    cancellation_reason_id  NUMBER PRIMARY KEY,
    reason_code             VARCHAR2(20)  NOT NULL,
    reason_description      VARCHAR2(200) NOT NULL,
    active_flag             CHAR(1)       DEFAULT 'Y' NOT NULL,

    CONSTRAINT uq_cancel_reason_code UNIQUE (reason_code),

    CONSTRAINT chk_cancel_reason_active
        CHECK (active_flag IN ('Y', 'N'))
);


CREATE TABLE RESERVATION_CANCELLATION (
    reservation_id              NUMBER PRIMARY KEY,
    cancellation_reason_id      NUMBER         NOT NULL,
    canceled_at                 TIMESTAMP      NOT NULL,
    canceled_by_user_group      VARCHAR2(40),
    cancellation_note           VARCHAR2(300),

    CONSTRAINT fk_res_cancel_reservation
        FOREIGN KEY (reservation_id)
        REFERENCES RESERVATION (reservation_id),

    CONSTRAINT fk_res_cancel_reason
        FOREIGN KEY (cancellation_reason_id)
        REFERENCES CANCELLATION_REASON (cancellation_reason_id)
);


CREATE TABLE RATE_PLAN (
    rate_plan_id         NUMBER PRIMARY KEY,
    room_type_id         NUMBER        NOT NULL,
    rate_plan_name       VARCHAR2(80)  NOT NULL,
    meal_plan            VARCHAR2(40),
    deposit_type         VARCHAR2(40),
    refundable_flag      CHAR(1)       DEFAULT 'Y' NOT NULL,
    is_active            CHAR(1)       DEFAULT 'Y' NOT NULL,

    CONSTRAINT fk_rate_plan_room_type
        FOREIGN KEY (room_type_id)
        REFERENCES ROOM_TYPE (room_type_id),

    CONSTRAINT chk_rate_plan_refundable
        CHECK (refundable_flag IN ('Y', 'N')),

    CONSTRAINT chk_rate_plan_active
        CHECK (is_active IN ('Y', 'N'))
);


CREATE TABLE RATE_CALENDAR (
    rate_plan_id         NUMBER        NOT NULL,
    rate_date            DATE          NOT NULL,
    nightly_rate         NUMBER(10,2)  NOT NULL,
    min_stay             NUMBER        DEFAULT 1 NOT NULL,
    max_sell_rooms       NUMBER,
    closed_to_arrival    CHAR(1)       DEFAULT 'N' NOT NULL,

    CONSTRAINT pk_rate_calendar
        PRIMARY KEY (rate_plan_id, rate_date),

    CONSTRAINT fk_rate_calendar_plan
        FOREIGN KEY (rate_plan_id)
        REFERENCES RATE_PLAN (rate_plan_id),

    CONSTRAINT chk_rate_calendar_rate
        CHECK (nightly_rate >= 0),

    CONSTRAINT chk_rate_calendar_min_stay
        CHECK (min_stay > 0),

    CONSTRAINT chk_rate_calendar_max_sell
        CHECK (max_sell_rooms IS NULL OR max_sell_rooms >= 0),

    CONSTRAINT chk_rate_calendar_cta
        CHECK (closed_to_arrival IN ('Y', 'N'))
);


CREATE TABLE PAYMENT_TRANSACTION (
    payment_id          NUMBER PRIMARY KEY,
    reservation_id      NUMBER         NOT NULL,
    payment_datetime    TIMESTAMP      NOT NULL,
    amount              NUMBER(10,2)   NOT NULL,
    payment_type        VARCHAR2(30)   NOT NULL,
    payment_status      VARCHAR2(30)   NOT NULL,
    reference_no        VARCHAR2(50),

    CONSTRAINT fk_payment_reservation
        FOREIGN KEY (reservation_id)
        REFERENCES RESERVATION (reservation_id),

    CONSTRAINT uq_payment_reference UNIQUE (reference_no),

    CONSTRAINT chk_payment_amount
        CHECK (amount >= 0)
);
