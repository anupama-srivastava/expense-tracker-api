# Expense Tracker API

A comprehensive RESTful API for personal expense tracking and budget management built with Django REST Framework. This API provides advanced features for managing expenses, budgets, analytics, and notifications with real-time capabilities.

## 🚀 Features

- **User Management**: JWT authentication with user registration and profile management
- **Expense Tracking**: CRUD operations for expenses with categorization and receipt attachments
- **Budget Management**: Set and track budgets with spending limits and alerts
- **Advanced Analytics**: Detailed spending analytics with charts and reports
- **Real-time Notifications**: Email and in-app notifications for budget alerts and reminders
- **Data Visualization**: Generate charts and reports using matplotlib and seaborn
- **File Upload**: Support for receipt images with AWS S3 integration
- **API Documentation**: Auto-generated interactive API documentation with Swagger/OpenAPI
- **Background Tasks**: Asynchronous processing with Celery and Redis
- **Comprehensive Testing**: Unit tests with pytest and factory patterns

## 🛠️ Technology Stack

- **Backend**: Django 4.x, Django REST Framework
- **Database**: PostgreSQL (production), SQLite (development)
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Caching**: Redis
- **Task Queue**: Celery with Redis broker
- **File Storage**: AWS S3 (production), local storage (development)
- **API Documentation**: drf-spectacular (OpenAPI 3)
- **Testing**: pytest, factory-boy
- **Code Quality**: black, flake8, pre-commit hooks

## 📋 Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose (optional)
- AWS Account (for S3 storage in production)

## 🏃‍♂️ Quick Start

### Using Docker Compose (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd expense-tracker-api
```

2. Create environment file:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Start services:
```bash
docker-compose up --build
```

4. Run migrations:
```bash
docker-compose exec web python manage.py migrate
```

5. Create superuser:
```bash
docker-compose exec web python manage.py createsuperuser
```

6. Access the API:
- API Documentation: http://localhost:8000/api/docs/
- Admin Panel: http://localhost:8000/admin/

### Local Development

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your local configuration
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Start development server:
```bash
python manage.py runserver
```

## 📁 Project Structure

```
expense-tracker-api/
├── apps/
│   ├── analytics/          # Analytics and reporting
│   ├── budgets/           # Budget management
│   ├── expenses/          # Expense CRUD operations
│   ├── notifications/     # Notification system
│   └── users/            # User management
├── config/
│   ├── settings.py       # Django settings
│   ├── urls.py          # URL configuration
│   └── wsgi.py          # WSGI configuration
├── logs/                # Application logs
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker services
└── manage.py          # Django management script
```

## 🔗 API Endpoints

### Authentication
- `POST /api/v1/auth/register/` - User registration
- `POST /api/v1/auth/login/` - User login
- `POST /api/v1/auth/logout/` - User logout
- `POST /api/v1/auth/token/refresh/` - Refresh JWT token
- `GET /api/v1/auth/profile/` - Get user profile
- `PUT /api/v1/auth/profile/` - Update user profile

### Expenses
- `GET /api/v1/expenses/` - List all expenses
- `POST /api/v1/expenses/` - Create new expense
- `GET /api/v1/expenses/{id}/` - Get specific expense
- `PUT /api/v1/expenses/{id}/` - Update expense
- `DELETE /api/v1/expenses/{id}/` - Delete expense
- `GET /api/v1/expenses/categories/` - Get expense categories
- `POST /api/v1/expenses/{id}/attach-receipt/` - Attach receipt to expense

### Budgets
- `GET /api/v1/budgets/` - List all budgets
- `POST /api/v1/budgets/` - Create new budget
- `GET /api/v1/budgets/{id}/` - Get specific budget
- `PUT /api/v1/budgets/{id}/` - Update budget
- `DELETE /api/v1/budgets/{id}/` - Delete budget
- `GET /api/v1/budgets/{id}/status/` - Get budget status and alerts

### Analytics
- `GET /api/v1/analytics/summary/` - Get spending summary
- `GET /api/v1/analytics/trends/` - Get spending trends
- `GET /api/v1/analytics/category-breakdown/` - Category-wise breakdown
- `GET /api/v1/analytics/monthly-report/` - Monthly expense report
- `GET /api/v1/analytics/export/` - Export analytics data

### Notifications
- `GET /api/v1/notifications/` - List notifications
- `PUT /api/v1/notifications/{id}/read/` - Mark notification as read
- `POST /api/v1/notifications/settings/` - Update notification preferences

## 🔧 Environment Variables

Create a `.env` file with the following variables:

```bash
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/expense_tracker

# Redis
REDIS_URL=redis://localhost:6379/0

# Email (Optional)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# AWS S3 (Optional - for production)
USE_S3=False
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=us-east-1

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=apps --cov-report=html

# Run specific app tests
pytest apps/expenses/tests/
```

## 🚀 Deployment

### Production Deployment Checklist

1. **Security Settings**:
   - Set `DEBUG=False`
   - Use strong `SECRET_KEY`
   - Configure proper `ALLOWED_HOSTS`
   - Enable HTTPS

2. **Database**:
   - Use PostgreSQL in production
   - Set up regular backups
   - Configure connection pooling

3. **File Storage**:
   - Configure AWS S3 for media files
   - Set up CDN for static files

4. **Background Tasks**:
   - Configure Celery with proper broker
   - Set up monitoring for Celery workers

5. **Monitoring**:
   - Set up error tracking (Sentry)
   - Configure logging
   - Set up health checks

### Using Docker for Production

```bash
# Build and run production containers
docker-compose -f docker-compose.prod.yml up -d

# Run migrations
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

# Collect static files
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
```

## 📊 Database Schema

### Core Models

- **User**: Custom user model with email as username
- **Expense**: Individual expense records with categories, amounts, dates
- **Category**: Expense categories (Food, Transport, Shopping, etc.)
- **Budget**: Monthly/weekly budgets with spending limits
- **Notification**: User notifications and alerts
- **Receipt**: Receipt images attached to expenses

## 🎯 Key Features in Detail

### Expense Management
- Multi-currency support
- Receipt attachment with image upload
- Recurring expense tracking
- Split expense functionality
- Custom categories and tags

### Budget Management
- Monthly/weekly/annual budgets
- Category-specific budgets
- Real-time budget tracking
- Automated alerts when approaching limits
- Budget vs actual spending analysis

### Analytics & Reporting
- Interactive charts and graphs
- Spending trends over time
- Category-wise analysis
- Monthly/yearly reports
- Export to CSV/PDF
- Predictive analytics

### Notifications
- Email notifications for budget alerts
- Push notifications (future enhancement)
- Customizable notification preferences
- Digest emails with spending summaries

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🗺️ Roadmap

- [ ] Mobile app integration
- [ ] Bank account integration
- [ ] AI-powered spending insights
- [ ] Shared budgets for families
- [ ] Receipt OCR for automatic data extraction
- [ ] Voice input for expense entry
- [ ] Advanced forecasting and predictions

---
