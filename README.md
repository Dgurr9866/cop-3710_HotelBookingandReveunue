# cop-3710_HotelBookingandReveunue

## Hotel Booking and Revenue Management Database

## Project Description
This project implements a relational database for a hotel booking system. The database supports both operational reservation and revenue-focused analytics.

## Project Scope

The system is designed to support:
- Guest and reservation management(create, modify, cancel reservations)
- Room type and inventory tracking
- Pricing and date-based rate management
- Payment transaction tracking
- Cancellation logging and cancellation trend analysis
- Occupancy and revenue reporting

### Key Features

#### Reservation Management:

*    **Guest and Reservation Tracking:** Management of guest information, reservation details, and status tracking (Confirmed, Canceled, Checked-in, etc.). 
    
*    **Room and Inventory Control:** Defining room types and inventory management to track capacity.

*   **Transaction-Safe Booking:** Implementation of booking logic designed to prevent overbooking and ensure data integrity.

#### Pricing:

*    **Dynamic Pricing:** Support for various rates and date-based pricing.

*    **Revenue Metrics:** Calculation and tracking of important performance metrics.

*    **Occupancy Forecasting:** Views and queries to project future occupancy based on current bookings and historical trends. 

#### Cancellations Analysis:
*   **Cancellation Tracking:** Logging of cancellation times and reason for cancellation.

*   **Risk Analysis:** Analysis of cancellation trends to identify patterns.

#### End Users

**Front Desk / Reservation Agent** - Ability to create/modify cancel reservations.

**Revenue Manager** - Ability to monitor occupancy and analyze cancellations

**Hotel Manager / Operations Manager** - Ability to track performance summaries and operations.

#### Data Sources

I will use the Hotel Booking demand Page given by the instructor using this url:

https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand

## Note
To satisfy the project complexity requirement, the data may extend beyond the Kaggle resource. Therefore, some values may be fabricated where real data is not available.