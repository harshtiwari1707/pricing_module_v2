# Pricing Module V2

Welcome to **Pricing Module V2**!

## Getting Started
1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/pricing_module_v2.git
    cd pricing_module_v2
    ```

2. (Optional but Recommended) Create and activate a virtual environment:

    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install project dependencies:
    ```bash
    pip install -r requirements.txt
    ```


4. Database Setup:
    ```bash
    python manage.py migrate
    ```

5. Create a superuser for admin access:
    ```bash
    python manage.py createsuperuser
    ```

6. Run the server:
    ```bash
    python manage.py runserver
    ```

Access the admin page on: http://127.0.0.1:8000/admin/

Access the pricing calculation API on: http://127.0.0.1:8000/pricing_config/calculate_total_price/?total_distance=10&trip_time=59&waiting_time=10&trip_date=2023-08-03 
