# Django CRUD Application with Data Visualization

A full-featured Django REST API application with CRUD operations, data visualization dashboard, and third-party API integration.

## Features

- **RESTful API** - Complete CRUD operations for item management
- **Data Visualization** - Interactive charts and statistics dashboard
- **Third-party API Integration** - Weather data integration using OpenWeather API
- **PostgreSQL Database** - Production-ready database configuration
- **Admin Interface** - Django admin panel for data management
- **Bootstrap UI** - Responsive web interface
- **CORS Support** - Cross-Origin Resource Sharing enabled
- **Environment Variables** - Secure configuration management

## Tech Stack

- Django 4.2.7
- Django REST Framework 3.14.0
- PostgreSQL
- Bootstrap 5.1.3
- Chart.js
- OpenWeather API

## Project Structure

```
crud_project/
├── crud_project/          # Project configuration
│   ├── settings.py        # Django settings
│   ├── urls.py            # Root URL configuration
│   ├── wsgi.py            # WSGI application
│   └── asgi.py            # ASGI application
├── items/                 # Main application
│   ├── models.py          # Item model
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # API views and logic
│   ├── urls.py            # App URL patterns
│   ├── admin.py           # Admin configuration
│   └── templates/         # HTML templates
│       └── items/
│           ├── base.html
│           ├── dashboard.html
│           └── items_list.html
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
└── .env                   # Environment variables
```

## Installation

### Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd crud_project
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create PostgreSQL database**
   ```bash
   psql -U postgres
   CREATE DATABASE crud_db;
   \q
   ```

5. **Configure environment variables**
   
   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/crud_db
   OPENWEATHER_API_KEY=your-openweather-api-key
   SUPABASE_URL=https://your-project.supabase.co
   ```

   Get your OpenWeather API key from: https://openweathermap.org/api

6. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

9. **Run development server**
   ```bash
   python manage.py runserver
   ```

10. **Access the application**
    - Dashboard: http://localhost:8000/
    - API Browser: http://localhost:8000/api/items/
    - Browse Items: http://localhost:8000/api/browse/
    - Admin Panel: http://localhost:8000/admin/

## API Endpoints

### Items

- `GET /api/items/` - List all items (paginated)
- `POST /api/items/` - Create new item
- `GET /api/items/{id}/` - Retrieve specific item
- `PUT /api/items/{id}/` - Update item
- `PATCH /api/items/{id}/` - Partial update
- `DELETE /api/items/{id}/` - Delete item

### Custom Endpoints

- `GET /api/items/categories/` - Get category statistics
- `GET /api/items/recent_items/` - Get items from last 7 days
- `GET /api/weather/?city=<city_name>` - Get weather data for a city

## Data Model

### Item Model

```python
{
    "id": integer,
    "name": string (max 200 chars),
    "description": text (optional),
    "category": choice (ELECTRONICS, CLOTHING, BOOKS, HOME, SPORTS, OTHER),
    "price": decimal (max 10 digits, 2 decimal places),
    "quantity": integer (default: 1),
    "created_at": datetime (auto),
    "updated_at": datetime (auto)
}
```

## Usage Examples

### Creating an Item (cURL)

```bash
curl -X POST http://localhost:8000/api/items/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop",
    "description": "High-performance laptop",
    "category": "ELECTRONICS",
    "price": "999.99",
    "quantity": 5
  }'
```

### Getting Weather Data

```bash
curl http://localhost:8000/api/weather/?city=London
```

### Category Statistics

```bash
curl http://localhost:8000/api/items/categories/
```

## Dashboard Features

The dashboard (`/api/dashboard/`) provides:

- **Statistics Cards**: Total items, total value, average price
- **Category Chart**: Bar chart showing items by category
- **Daily Trend**: Line chart showing items added in last 7 days
- **Weather Integration**: Real-time weather data for any city
- **API Testing Links**: Quick access to test API endpoints

## Configuration

### Database

The application uses PostgreSQL with connection pooling. Configure via `DATABASE_URL` environment variable or modify `settings.py` for direct configuration.

### CORS

CORS is enabled for all origins in development. For production, update `CORS_ALLOW_ALL_ORIGINS` in `settings.py`:

```python
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
]
```

### Pagination

Default pagination is set to 10 items per page. Modify in `settings.py`:

```python
REST_FRAMEWORK = {
    'PAGE_SIZE': 10
}
```

## Deployment

### Environment Variables for Production

```env
SECRET_KEY=<generate-secure-key>
DEBUG=False
DATABASE_URL=postgresql://user:password@host:port/database
ALLOWED_HOSTS=yourdomain.com,.onrender.com
OPENWEATHER_API_KEY=your-api-key
```

### Deployment Checklist

- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use secure `SECRET_KEY`
- [ ] Set up production database
- [ ] Configure static files serving
- [ ] Enable HTTPS
- [ ] Set up proper CORS origins
- [ ] Configure database connection pooling

## Testing

Run tests with:

```bash
python manage.py test
```

## Admin Panel

Access the Django admin at `/admin/` to:

- Add, edit, delete items
- View item statistics
- Filter by category and date
- Search items by name or description

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Troubleshooting

### Database Connection Error

```bash
# Check PostgreSQL is running
sudo service postgresql status

# Verify database exists
psql -U postgres -l
```

### Missing Dependencies

```bash
pip install -r requirements.txt --upgrade
```

### Migration Issues

```bash
python manage.py makemigrations
python manage.py migrate --run-syncdb
```

## License

This project is open source and available under the MIT License.

## Support

For issues and questions, please open an issue in the repository.

## Acknowledgments

- Django Documentation
- Django REST Framework
- OpenWeather API
- Chart.js
- Bootstrap
