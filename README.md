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

Here is a visual overview of the different pages and features in the Cinema Sharif Reservation System:

**Phone Number Entry Page**
<img width="1920" height="911" alt="image" src="https://github.com/user-attachments/assets/b20ca712-6ad6-48ab-a574-c2b773d1072b" />

**Login Page**
<img width="1920" height="913" alt="image" src="https://github.com/user-attachments/assets/80714223-c830-4d88-9d18-5d4d4e184bee" />

**Registration Page**
<img width="1920" height="906" alt="image" src="https://github.com/user-attachments/assets/32f8e6a2-a117-485c-8b4e-7b434ba92aee" />

**Movies List Page**
<img width="1920" height="907" alt="image" src="https://github.com/user-attachments/assets/02a1325f-24e6-4d72-9457-f5c30578949e" />

**My Tickets (Reservations) Page**
<img width="1920" height="907" alt="image" src="https://github.com/user-attachments/assets/4cccbdcc-d642-489a-9471-677c7f6de880" />

**Cinemas Page**
<img width="1920" height="906" alt="image" src="https://github.com/user-attachments/assets/9e469494-d073-4e7e-b8f9-2dcf96be2b30" />

**Movies in a Specific Cinema Page**
<img width="1920" height="911" alt="image" src="https://github.com/user-attachments/assets/6f84c782-d3bb-4431-9af7-750ac72d03ee" />

**Movie Details & Screening Selection Page**
<img width="1920" height="904" alt="image" src="https://github.com/user-attachments/assets/3a56b9b3-fee1-4609-9733-dfbdfc38be79" />
<img width="1920" height="899" alt="image" src="https://github.com/user-attachments/assets/9b3d3df9-af5b-45a0-a76c-51906ee27685" />

**Cinemas & Screenings for a Specific Movie**
<img width="1920" height="899" alt="image" src="https://github.com/user-attachments/assets/2c9eac50-88d3-4765-b366-6ffcf79c00dc" />

**Seat Selection Page**
<img width="1920" height="906" alt="image" src="https://github.com/user-attachments/assets/50ce59aa-bfee-45c1-9a3b-191181d5b15e" />

**Reservation Confirmation & Payment Page**
<img width="1899" height="909" alt="image" src="https://github.com/user-attachments/assets/90dc688f-3354-468e-995e-6ddedb9a76f5" />
<img width="1920" height="897" alt="image" src="https://github.com/user-attachments/assets/886b2f95-d511-4f9a-8901-bb67136bdbe4" />

**Reservation Cancellation Page**
<img width="1920" height="897" alt="image" src="https://github.com/user-attachments/assets/e79d5b2c-8e1d-4f7b-8f88-038ddcff903a" />

**Admin Pages**
<img width="1920" height="904" alt="image" src="https://github.com/user-attachments/assets/28038646-8351-4c4f-a805-4b42bb9b8816" />
<img width="1920" height="897" alt="image" src="https://github.com/user-attachments/assets/0d229e2a-8e8b-4ba1-9756-b33062ef366d" />
<img width="1920" height="900" alt="image" src="https://github.com/user-attachments/assets/df585259-c44b-4165-b678-220febd10932" />
<img width="1920" height="904" alt="image" src="https://github.com/user-attachments/assets/fbdea473-43b7-4792-9dca-720f06e2117b" />
<img width="1920" height="901" alt="image" src="https://github.com/user-attachments/assets/b93a4bec-ed39-4068-98c4-a89c2d1323a8" />
<img width="1920" height="891" alt="image" src="https://github.com/user-attachments/assets/2106dd71-e753-44ee-8678-a19843874c7e" />

## 🚀 Installation & Setup

To run this project locally, follow these steps:

**1. Clone the repository:**
```bash
git clone https://github.com/alif2884/-Cinema-Sharif-Reservation-System.git
cd cinema-sharif
```

**2. Create and activate a virtual environment:**
```bash
python -m venv venv\

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Database Configuration:**
Create a PostgreSQL database and update your .env file or settings.py with your database credentials (NAME, USER, PASSWORD).

**5. Apply migrations:**
```bash
python manage.py makemigrations
python manage.py migrate
```

**6. Run the development server:**
```bash
python manage.py runserver
```
