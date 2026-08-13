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
<img width="1920" height="911" alt="image" src="https://github.com/user-attachments/assets/7f159530-0683-4c8c-a067-d84c542ea2f0" />
<img width="1920" height="913" alt="image" src="https://github.com/user-attachments/assets/a8f63e8b-484f-4521-8f09-2351263627a2" />
<img width="1920" height="906" alt="image" src="https://github.com/user-attachments/assets/6c35c682-5742-4062-9dd3-95f792205dee" />
<img width="1920" height="907" alt="image" src="https://github.com/user-attachments/assets/6f2d40a2-b953-47f6-8d40-97d4e769413d" />
<img width="1920" height="907" alt="image" src="https://github.com/user-attachments/assets/994df615-7212-45ad-9da5-a85acb85171f" />
<img width="1920" height="906" alt="image" src="https://github.com/user-attachments/assets/82feaf50-8453-423c-bd9e-4a8c441af50d" />
<img width="1920" height="911" alt="image" src="https://github.com/user-attachments/assets/34291a49-e86d-4c6d-a565-607c201bf814" />

**Screening & Seat Selection**
<img width="1920" height="904" alt="image" src="https://github.com/user-attachments/assets/67cbdef3-832c-459f-88a6-3edb11a53a94" />
<img width="1920" height="899" alt="image" src="https://github.com/user-attachments/assets/cbaf88df-9db2-4258-abd8-14cb20c289b8" />
<img width="1920" height="899" alt="image" src="https://github.com/user-attachments/assets/43e89ef9-cc05-457a-b75f-08a69a983027" />
<img width="1920" height="906" alt="image" src="https://github.com/user-attachments/assets/91b939e5-dde9-4c25-824a-6ad8c5efaedf" />


**Checkout, Payment Timer & Wallet**
<img width="1899" height="909" alt="image" src="https://github.com/user-attachments/assets/5ec888c3-5c8e-41b7-a740-399a91548cc5" />
<img width="1920" height="897" alt="image" src="https://github.com/user-attachments/assets/7133ee5a-4da3-4a09-8250-b965da24dd96" />
<img width="1920" height="897" alt="image" src="https://github.com/user-attachments/assets/75184c50-6ac9-4646-b9db-4d4a1e04fbe5" />


**Admin Panel (Adding Cinemas & Editing Movies)**
<img width="1920" height="904" alt="image" src="https://github.com/user-attachments/assets/ec910176-22e9-4f3e-a4ef-8612a5573c5f" />
<img width="1920" height="897" alt="image" src="https://github.com/user-attachments/assets/18db8889-ba2c-499d-82b3-7264f1eb5d37" />
<img width="1920" height="900" alt="image" src="https://github.com/user-attachments/assets/ed81bcc6-0254-4529-9f37-353fe4f5a4f5" />
<img width="1920" height="904" alt="image" src="https://github.com/user-attachments/assets/c4ba47c8-fb6b-460c-bb56-c19d70f769cf" />
<img width="1920" height="901" alt="image" src="https://github.com/user-attachments/assets/cc82ecda-6634-4dcb-8920-a98a0de2a7b2" />
<img width="1920" height="891" alt="image" src="https://github.com/user-attachments/assets/20eeca85-1c56-4ae8-9ce8-d2aac893a8fe" />


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
