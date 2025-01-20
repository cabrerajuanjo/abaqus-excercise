# Investment Portfolio Management System

<div style="background-color: #F0DD00; color: black; padding: 10px; border-radius: 5px; font-weight: bold;">
⚠️ **Warning:** This project was created as a take-home assignment for a job position and is not intended to be used as a real financial tool.
</div>

This project is a full-stack application for managing investment portfolios. It provides a backend built with Django and Django REST Framework and a frontend developed in React. The application allows users to:

1. **Visualize portfolio data**: Display totals by date and asset weights graphically.
2. **Load and delete data via Excel file**: Upload portfolio data using an Excel file.
3. **Perform transactions**: Buy or sell.

## Features

### Frontend (React)
Three main components
  - **Visualization Module**: Displays graphs for portfolio totals by date and asset weights.
  - **Data Loading Module**: Enables users to upload Excel files containing portfolio data.
  - **Transaction Module**: Allows buying and selling assets directly through the UI.

### Backend (Django + Django REST Framework)
- RESTful API endpoints for managing and visualizing portfolio data.
- Helpers selectors to improve user experience
- Integration tests for the most common flows

## API Endpoints

### 1. Portfolio Weights
- **Endpoint**: `/api/portfolio/weights`
- **Method**: GET
- **Query Parameters**:
  - `date__lt` (optional): Filter weights before a specific date.
  - `date__gt` (optional): Filter weights after a specific date.
- **Response**: 
  ```json
  [
    {
      "date": "2025-01-01",
      "asset": "Asset A",
      "portfolio": "Portfolio X",
      "weight": 0.25
    }
  ]
  ```

### 2. Portfolio Totals
- **Endpoint**: `/api/portfolio/totals`
- **Method**: GET
- **Query Parameters**:
  - `date__lt` (optional): Filter totals before a specific date.
  - `date__gt` (optional): Filter totals after a specific date.
- **Response**:
  ```json
  [
    {
      "date": "2025-01-01",
      "portfolio": "Portfolio X",
      "total_amount": 1000000.0
    }
  ]
  ```

### 3. Load Portfolio Data
- **Endpoint**: `/api/portfolio/load`
- **Method**: POST
- **Body**:
  ```json
  {
    "file": "<Excel File>",
    "initial_total": 1000000.0
  }
  ```
- **Response**: HTTP 200 OK

### 4. Perform Transactions
- **Endpoint**: `/api/portfolio/transact`
- **Method**: POST
- **Body**:
  ```json
  {
    "date": "2025-01-01",
    "portfolio": "Portfolio X",
    "asset": "Asset A",
    "operation": "BUY",
    "amount": 500
  }
  ```
- **Response**:
  ```json
  {
    "success": true
  }
  ```

### 5. Reset Portfolio Data
- **Endpoint**: `/api/portfolio/reset`
- **Method**: POST
- **Response**: HTTP 200 OK

### 6. List Portfolios
- **Endpoint**: `/api/portfolio/portfolios`
- **Method**: GET
- **Response**:
  ```json
  ["Portfolio X", "Portfolio Y"]
  ```

### 7. List Assets
- **Endpoint**: `/api/portfolio/assets`
- **Method**: GET
- **Response**:
  ```json
  ["Asset A", "Asset B"]
  ```

### 8. List Dates
- **Endpoint**: `/api/portfolio/dates`
- **Method**: GET
- **Response**:
  ```json
  ["2025-01-01", "2025-01-02"]
  ```

## Excel File Format

When uploading data via Excel files, ensure the following format is followed for each sheet:

### Sheet: `weights`
This sheet specifies the weights of different assets in various portfolios by date.

#### Columns:
- **Fecha**: Date of the weights (e.g., `2022-02-15`).
- **activos**: Name of the asset (e.g., `EEUU`, `Europa`, `UK`).
- **portafolio 1**: Weight of the asset in Portfolio 1 (e.g., `0.28`, `0.087`).
- **portafolio 2**: Weight of the asset in Portfolio 2 (e.g., `0.28`, `0.067`).

#### Sample Data:
| Fecha       | activos | portafolio 1 | portafolio 2 |
|-------------|---------|--------------|--------------|
| 2022-02-15  | EEUU    | 0.28         | 0.28         |
| 2022-02-15  | Europa  | 0.087        | 0.067        |
| 2022-02-15  | UK      | 0.023        | 0.023        |


### Sheet: `Precios`
This sheet contains daily prices for various assets.

#### Columns:
- **Dates**: Date of the recorded prices (e.g., `2022-02-15`).
- Asset columns: Each column represents an asset with its price on the specified date. Examples:
  - **EEUU**: Price of the US asset (e.g., `9383.57`).
  - **Europa**: Price of the Europe asset (e.g., `66.03`).
  - **Japón**: Price of the Japan asset (e.g., `390.26256`).
  - Additional assets: `EM Asia`, `Latam`, `High Yield`, `IG Corporate`, etc.

#### Sample Data:
| Dates       | EEUU     | Europa  | Japón    | EM Asia | Latam | High Yield | IG Corporate | ...  |
|-------------|----------|---------|----------|---------|-------|------------|--------------|------|
| 2022-02-15  | 9383.57  | 66.03   | 390.26256| 82.35   | 26.84 | 2355.25    | 3314.66      | ...  |
| 2022-02-16  | 9393.09  | 66.25   | 399.66912| 82.76   | 27.16 | 2357.94    | 3314.05      | ...  |
| 2022-02-17  | 9195.35  | 65.09   | 397.73559| 82.01   | 26.44 | 2357.02    | 3317.27      | ...  |


Ensure all column names match exactly, and the data is complete for all required fields.

## Setup Instructions

### Development environment

#### Backend
1. Clone the repository and navigate to the backend directory.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Apply migrations:
   ```bash
   python manage.py migrate
   ```

4. Start the server:
   ```bash
   python manage.py runserver
   ```
- (optional) Run tests:
   ```bash
   python manage.py test
   ```

#### Frontend
1. Navigate to the frontend directory.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
