# Sundari Silk Palace — Backend API

This is the Django backend API for Sundari Silk Palace. It provides the database and API endpoints for managing products, categories, testimonials, and customer inquiries.

## Tech Stack
- **Framework**: Django & Django REST Framework (DRF)
- **Database**: PostgreSQL (hosted on Neon)
- **Image Storage**: Cloudinary
- **Hosting**: Render (Web Service)
- **Static Files**: WhiteNoise

## Live Architecture
The backend is fully deployed and accessible via Render.
- **Admin Panel**: `/admin/` (Manage products and view inquiries)
- **API Endpoints**: 
  - `GET /api/health/`
  - `GET /api/categories/`
  - `GET /api/products/`
  - `GET /api/testimonials/`
  - `POST /api/inquiries/`

*Note: The frontend application securely consumes these endpoints.*

## Local Development Setup

1. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Environment Variables:**
   Create a `.env` file based on `.env.example`. You will need your Cloudinary credentials and a local or remote PostgreSQL connection string.

4. **Run migrations and seed data:**
   ```bash
   python manage.py migrate
   python manage.py seed_data
   ```

5. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

## Deployment Notes
- **Render Setup**: Deploys automatically on push to the `main` branch via the `build.sh` script.
- **Sleep Prevention**: The Render free tier spins down after 15 minutes of inactivity. To prevent this, an external monitor (like UptimeRobot) is configured to ping `/api/health/` every 5 minutes.
