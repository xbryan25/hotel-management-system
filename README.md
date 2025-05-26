# ![Hotel Icon](resources/icons/hms_db_icon.ico) HotelEase

A Hotel Management System that streamlines the booking and administration process for both customers and hotel staff. This application allows customers to search for available rooms, make reservations, and manage their bookings, while providing hotel administrators with tools to track occupancy, handle cancellations, and modify reservations efficiently.

## Features

### 🧭 Dashboard  
An overview panel that displays real-time hotel data including rooms, reservations, and guest activities.

- View today’s check-ins and check-outs
- Monitor available, reserved, and booked rooms
- Track room statuses: **Available**, **Reserved**, **Occupied**, **Under Maintenance**, or **Not Available**
- View ongoing reservations at a glance

---

### 🛏️ Rooms  
Displays all rooms in the hotel, with the option to add and manage individual room details.

- Create and register new rooms
- Each room entry includes:
  - Room Picture
  - Room Number
  - Capacity
  - Daily Rate
  - Status
- Toggle between **grid view** and **list view** for room browsing

---

### 📅 Reservations  
Manage all room reservations, including upcoming and active bookings.

- Create new reservations
- Each reservation includes:
  - Unique Reservation ID
  - Guest Information
  - Billing Details
  - Room Details

---

### 🧳 Bookings  
Handles guest check-ins and check-outs. Once a guest checks in, their reservation becomes a booking.

- Booking includes full guest details, billing summary, and stay information

---

### 👤 Guests  
Manage guest records.

- Store complete guest information
- Edit guest profiles as needed

---

### 💳 Billings  
Oversee all payment transactions for the guests.

- Handle guest payments
- Track outstanding balances and payment history

---

### 🛎️ Services  
Offer additional paid services for guests during their stay.

- Add customizable hotel services (e.g., extra pillows, room cleaning)
- Set and manage service rates


## To run the project on a local machine

Clone the project
```bash
  git clone https://github.com/xbryan25/hotel-management-system.git
```

Go to project directory
```bash
  hotel-management-system
```

Create and activate the virtual environment
```bash
  python -m venv hotel-management-system-venv
  venv\Scripts\activate
```

Once in the virtual environment, install dependencies
```bash
  pip install -r requirements.txt
```

Once the dependencies are installed, create an .env file for your database credentials

- Powershell
```bash
ni .env
```

- cmd
```bash
type nul > .env
```

In the .env file, input your database credentials and preferred default user mode. For example:

- Open .env file using powershell or cmd
```bash
notepad .env
```

- Add and save contents
```bash
DB_HOST=localhost
DB_USER=your_username
DB_PASSWORD=your_password
```

- Switch to the working directory
```bash
cd src
```

- Run driver.py
```bash
py driver.py
```

- After running the application, deactivate the virtual environment:
```bash
deactivate
```