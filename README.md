# Pricing Module V2

Welcome to **Pricing Module V2**!

## Getting Started
1. Clone the repository:

    ```bash
    git clone https://github.com/harshtiwari1707/pricing_module_v2.git
    cd pricing_module_v2
    ```

2. (Optional) Create and activate a virtual environment:

    ```bash
    # Windows
    python -m venv pyenv
    pyenv\Scripts\activate

    # macOS/Linux
    python3 -m venv pyenv
    source pyenv/bin/activate
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

Access the admin page at - http://127.0.0.1:8000/admin/

Access the pricing calculation API at - http://127.0.0.1:8000/pricing_config/calculate_total_price/?total_distance=15&trip_time=62&waiting_time=15&trip_date=2023-10-04 
