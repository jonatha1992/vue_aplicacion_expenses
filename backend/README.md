# FastAPI Expenses Tracker

This project is a FastAPI application for managing expenses. It provides a simple API to register, retrieve, update, and delete expense entries.

## Project Structure

```
fastapi-expenses
├── app
│   ├── main.py          # Entry point of the FastAPI application
│   ├── models.py        # Data models for the application
│   ├── crud.py          # CRUD operations for expenses
│   └── routes
│       └── expenses.py  # Routes for managing expenses
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd fastapi-expenses
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```
   uvicorn app.main:app --reload
   ```

## Usage

### Endpoints

- **Create an Expense**
  - `POST /expenses/`
  - Body: `{ "name": "Expense Name", "amount": 100.0, "date": "2023-01-01" }`

- **Retrieve All Expenses**
  - `GET /expenses/`

- **Update an Expense**
  - `PUT /expenses/{id}/`
  - Body: `{ "name": "Updated Name", "amount": 150.0, "date": "2023-01-02" }`

- **Delete an Expense**
  - `DELETE /expenses/{id}/`

## License

This project is licensed under the MIT License.