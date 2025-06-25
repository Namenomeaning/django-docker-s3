# Django E-commerce Application

A Django-based e-commerce application with PostgreSQL database and AWS S3 integration for static/media files.

## Features

- Product catalog with categories
- Shopping cart functionality
- Order management
- AWS S3 integration for static and media files
- PostgreSQL database
- Docker containerization
- Nginx reverse proxy

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd django-ecommerce
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   ```
   
3. **Update the `.env` file with your configuration**
   - Set your SECRET_KEY
   - Configure AWS credentials if using S3
   - Modify database settings if needed
   - Set superuser credentials

4. **Start the application**
   ```bash
   docker-compose up --build
   ```

5. **Access the application**
   - Website: http://localhost:1337
   - Admin panel: http://localhost:1337/admin/
   - Default superuser: username `test`, password `test` (or as configured in .env)

## Configuration

The application uses environment variables for configuration. Key settings include:

- `SECRET_KEY`: Django secret key
- `DEBUG`: Enable/disable debug mode
- `USE_S3`: Enable AWS S3 for static/media files (TRUE/FALSE)
- `AWS_*`: AWS credentials and bucket configuration
- `DJANGO_SUPERUSER_*`: Superuser account details

## Development

The application automatically:
- Runs database migrations
- Creates a superuser account
- Loads sample data (categories and products)

## Want to learn how to build this?

Check out the [post](https://testdriven.io/blog/storing-django-static-and-media-files-on-amazon-s3/).
