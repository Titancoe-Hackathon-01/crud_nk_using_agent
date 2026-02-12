# Employee Management System

A RESTful API-based employee management system with CRUD operations, search, and filtering capabilities.

## Features

- **CRUD Operations**: Create, Read, Update, and Delete employee records
- **Employee Fields**: ID, Name, Email, Department, Role, Hire Date
- **Search & Filter**: Filter employees by department
- **RESTful API Design**: Clean, intuitive API endpoints
- **Data Validation**: Comprehensive input validation with error handling
- **Thread-Safe**: Safe for concurrent operations
- **Clean Code**: Well-structured, maintainable codebase

## Requirements

- Python 3.7+
- Flask 3.0.0
- Flask-CORS 4.0.0
- python-dateutil 2.8.2

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd crud_nk_using_agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Health Check
```
GET /api/health
```
Check if the service is running.

**Response:**
```json
{
  "success": true,
  "data": {
    "status": "healthy"
  }
}
```

### Create Employee
```
POST /api/employees
```

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "department": "Engineering",
  "role": "Software Engineer",
  "hire_date": "2024-01-15"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com",
    "department": "Engineering",
    "role": "Software Engineer",
    "hire_date": "2024-01-15"
  }
}
```

### Get All Employees
```
GET /api/employees
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john.doe@example.com",
      "department": "Engineering",
      "role": "Software Engineer",
      "hire_date": "2024-01-15"
    }
  ]
}
```

### Get Employee by ID
```
GET /api/employees/{id}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com",
    "department": "Engineering",
    "role": "Software Engineer",
    "hire_date": "2024-01-15"
  }
}
```

### Update Employee
```
PUT /api/employees/{id}
```

**Request Body (all fields optional):**
```json
{
  "name": "John Smith",
  "email": "john.smith@example.com",
  "department": "Engineering",
  "role": "Senior Software Engineer",
  "hire_date": "2024-01-15"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "John Smith",
    "email": "john.smith@example.com",
    "department": "Engineering",
    "role": "Senior Software Engineer",
    "hire_date": "2024-01-15"
  }
}
```

### Delete Employee
```
DELETE /api/employees/{id}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "message": "Employee 1 deleted successfully"
  }
}
```

### Search Employees by Department
```
GET /api/employees/search?department=Engineering
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john.doe@example.com",
      "department": "Engineering",
      "role": "Software Engineer",
      "hire_date": "2024-01-15"
    }
  ]
}
```

## Data Validation

The system includes comprehensive validation for all employee fields:

- **Name**: Required, 2-100 characters
- **Email**: Required, valid email format, must be unique
- **Department**: Required, 2-50 characters
- **Role**: Required, 2-50 characters
- **Hire Date**: Required, YYYY-MM-DD format, cannot be in the future, must be after 1900

## Error Handling

All endpoints return consistent error responses:

```json
{
  "success": false,
  "error": "Error message description"
}
```

Common HTTP status codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request (validation error)
- `404` - Not Found
- `405` - Method Not Allowed
- `500` - Internal Server Error

## Usage Examples

### Using cURL

**Create an employee:**
```bash
curl -X POST http://localhost:5000/api/employees \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Smith",
    "email": "jane.smith@example.com",
    "department": "Marketing",
    "role": "Marketing Manager",
    "hire_date": "2024-02-01"
  }'
```

**Get all employees:**
```bash
curl http://localhost:5000/api/employees
```

**Search by department:**
```bash
curl "http://localhost:5000/api/employees/search?department=Marketing"
```

**Update an employee:**
```bash
curl -X PUT http://localhost:5000/api/employees/1 \
  -H "Content-Type: application/json" \
  -d '{
    "role": "Senior Marketing Manager"
  }'
```

**Delete an employee:**
```bash
curl -X DELETE http://localhost:5000/api/employees/1
```

## Project Structure

```
crud_nk_using_agent/
├── app.py              # Flask application and API endpoints
├── employee.py         # Employee model with validation
├── database.py         # In-memory database with thread-safe operations
├── requirements.txt    # Python dependencies
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## Architecture

- **app.py**: Main Flask application containing all RESTful API endpoints
- **employee.py**: Employee model with comprehensive validation logic
- **database.py**: Thread-safe in-memory database for storing employee records
- **Separation of Concerns**: Clear separation between API layer, business logic, and data layer

## Design Decisions

1. **In-Memory Storage**: For simplicity and ease of deployment, uses thread-safe in-memory storage
2. **Flask Framework**: Lightweight and perfect for RESTful APIs
3. **Comprehensive Validation**: All inputs are validated at the model level
4. **Thread Safety**: Uses locks to ensure data consistency in concurrent environments
5. **RESTful Design**: Follows REST principles with proper HTTP methods and status codes
6. **Error Handling**: Consistent error responses across all endpoints
7. **CORS Enabled**: Allows cross-origin requests for frontend integration

## Future Enhancements

- Add persistent database (PostgreSQL, MySQL)
- Implement authentication and authorization
- Add pagination for employee list
- Add more search filters (by name, email, role)
- Add sorting capabilities
- Add unit and integration tests
- Add API documentation with Swagger/OpenAPI
- Add logging and monitoring
