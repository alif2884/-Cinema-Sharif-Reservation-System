# 🎬 Cinema Sharif Reservation System

A comprehensive, modular platform for managing and booking movie tickets online, developed using **Django** and **PostgreSQL**. This system is built with a strong emphasis on software engineering principles, design patterns, and concurrency management to ensure a secure and stable experience for both users and administrators.

## 🌟 Key Features

### 👤 User Panel (Customers)
* **Advanced Search & Filtering:** Filter movies by genre, release year, and title.
* **Movie Details & Screenings:** View complete movie information, posters, synopses, and available screening times.
* **Interactive Seat Selection:** A visual UI to check seat statuses (available, reserved, selected).
* **Digital Wallet System:** Users can charge their accounts and pay for tickets seamlessly using their wallet balance.
* **Time-limited Cart:** Allocates a specific timeframe (e.g., 15 minutes) to complete the payment process, preventing seat blocking.
* **Reservation Management:** Ability to cancel reservations and get a refund to the wallet using a tracking code.

### 🛡️ Admin Panel
* **Two-Factor/Custom Authentication:** Secure and dedicated access system for administrators.
* **Cinema Management:** Add, edit, delete, and view the list of cinemas along with their capacities.
* **Movie & Screening Management:** Define new movies, upload posters, set durations, and schedule screenings.

## ⚙️ Technical Highlights & Solved Challenges
* **Concurrency Control:** Utilized database-level locks (`select_for_update`) to prevent double-booking anomalies when multiple users attempt to reserve the same seat simultaneously.
* **Modular Architecture:** Separated the project logic into independent Django apps (`accounts`, `movies`, `reservation`, `screenings`) for better maintainability and scalability.
* **Design Patterns:**
  * **Factory Pattern:** Used for the unified creation of entities (e.g., invoices).
  * **Singleton Pattern:** Implemented for managing global system settings.

## 🛠️ Tech Stack
* **Backend:** Python, Django (MTV Architecture)
* **Database:** PostgreSQL
* **Frontend:** HTML5, CSS3, Vanilla JavaScript (with custom interactive UIs)
* **Security:** CSRF Protection, Session Management, Role-Based Access Control

## 📸 Screenshots

*Note: The following images demonstrate the user and admin workflows.*

**Home Page & Movie Filtering**
![Home Page](image_86e26b.png)

**Screening & Seat Selection**
![Seat Selection](image_86e245.png)

**Checkout, Payment Timer & Wallet**
![Checkout](image_86e22b.png)

**Admin Panel (Adding Cinemas & Editing Movies)**
![Admin Panel 1](image_86e20f.png)
![Admin Panel 2](image_86e20a.png)

## 🚀 Installation & Setup

To run this project locally, follow these steps:

**1. Clone the repository:**
```bash
git clone [https://github.com/YourUsername/cinema-sharif.git](https://github.com/YourUsername/cinema-sharif.git)
cd cinema-sharif
```

2. Create and activate a virtual environment:

Bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
3. Install dependencies:

Bash
pip install -r requirements.txt
4. Database Configuration:
Create a PostgreSQL database and update your .env file or settings.py with your database credentials (NAME, USER, PASSWORD).

5. Apply migrations:

Bash
python manage.py makemigrations
python manage.py migrate
6. Run the development server:

Bash
python manage.py runserver
