# Church Management System API

REST API for managing church members, visitors, Sunday school records, tithes, accounts, and bulk SMS.

## Features

- Member and membership management
- Sunday school records and birthday lookups
- Visitor management
- Tithe records and analytics
- JWT authentication with refresh token rotation and logout
- Bulk SMS sending via CSV or templates
- OpenAPI schema and Swagger documentation
- Cloudinary media storage

## Tech Stack

- Python 3
- Django 5
- Django REST Framework
- Simple JWT
- MySQL
- drf-spectacular
- Cloudinary
- Gunicorn and Uvicorn
- Render

## Local Setup

### Prerequisites

- Python 3.10 or later
- MySQL
- A virtual environment tool such as `venv`

### Installation

```bash
git clone https://github.com/archimedesAJ/cms-api.git
cd cms-api

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and set `DATABASE_URL` to your local MySQL connection string. Create the `cms_db` database in MySQL, then create and migrate the Django tables:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.

## Environment Variables

Create a `.env` file in the project root from `.env.example`. Set the database URL and provide credentials for any integrations you use:

```dotenv
DATABASE_URL=mysql://root:your-password@localhost:3306/cms_db
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
ARK_API_KEY=your-sms-api-key
ARK_SENDER_ID=LF Intl Min
```

Cloudinary credentials are used for media storage. The Arkesel credentials are required for SMS sending.

## API Endpoints

`{id}` in the tables below is the object primary key.

### Authentication and Profile

| Method | Endpoint   | Authentication | Description                                                                        |
| ------ | ---------- | -------------- | ---------------------------------------------------------------------------------- |
| `POST` | `/login`   | No             | Authenticate with `username` and `password`; returns JWT access and refresh tokens |
| `POST` | `/logout`  | Required       | Blacklist the refresh token supplied in the JSON body                              |
| `GET`  | `/profile` | Required       | Get the authenticated user's profile                                               |

### Members

| Method         | Endpoint                    | Authentication | Description                          |
| -------------- | --------------------------- | -------------- | ------------------------------------ |
| `GET`          | `/members/`                 | Required       | List members                         |
| `POST`         | `/members/`                 | Required       | Create a member                      |
| `GET`          | `/members/{id}/`            | Required       | Retrieve a member                    |
| `PUT`, `PATCH` | `/members/{id}/`            | Required       | Update a member                      |
| `DELETE`       | `/members/{id}/`            | Required       | Delete a member                      |
| `GET`          | `/members/males/`           | Required       | List male members                    |
| `GET`          | `/members/females/`         | Required       | List female members                  |
| `GET`          | `/members/birthdays_today/` | Required       | List members whose birthday is today |

The members list accepts the `gender` query parameter. Filtered request: `/members/?gender=male`.

### Sunday School

| Method         | Endpoint                         | Authentication | Description                                                   |
| -------------- | -------------------------------- | -------------- | ------------------------------------------------------------- |
| `GET`          | `/sundayschool/`                 | No             | List Sunday school students                                   |
| `POST`         | `/sundayschool/`                 | No             | Create a Sunday school student                                |
| `GET`          | `/sundayschool/{id}/`            | No             | Retrieve a Sunday school student                              |
| `PUT`, `PATCH` | `/sundayschool/{id}/`            | No             | Update a Sunday school student                                |
| `DELETE`       | `/sundayschool/{id}/`            | No             | Delete a Sunday school student                                |
| `GET`          | `/sundayschool/males/`           | No             | The registered gender action currently returns female records |
| `GET`          | `/sundayschool/birthdays_today/` | No             | List students whose birthday is today                         |

The Sunday School list accepts the `gender` query parameter.

### Visitors

| Method         | Endpoint           | Authentication | Description                                                   |
| -------------- | ------------------ | -------------- | ------------------------------------------------------------- |
| `GET`          | `/visitors/`       | No             | List visitors                                                 |
| `POST`         | `/visitors/`       | No             | Create a visitor                                              |
| `GET`          | `/visitors/{id}/`  | No             | Retrieve a visitor                                            |
| `PUT`, `PATCH` | `/visitors/{id}/`  | No             | Update a visitor                                              |
| `DELETE`       | `/visitors/{id}/`  | No             | Delete a visitor                                              |
| `GET`          | `/visitors/males/` | No             | The registered gender action currently returns female records |

The visitors list accepts the `gender` query parameter.

### Tithes

| Method         | Endpoint                          | Authentication | Description                                            |
| -------------- | --------------------------------- | -------------- | ------------------------------------------------------ |
| `GET`          | `/tithes/`                        | Required       | List active tithes                                     |
| `POST`         | `/tithes/`                        | Required       | Record a tithe                                         |
| `GET`          | `/tithes/{id}/`                   | Required       | Retrieve a tithe                                       |
| `PUT`, `PATCH` | `/tithes/{id}/`                   | Required       | Update a tithe                                         |
| `DELETE`       | `/tithes/{id}/`                   | Required       | Soft-delete a tithe                                    |
| `POST`         | `/tithes/{id}/restore/`           | Required       | Restore a soft-deleted tithe                           |
| `GET`          | `/tithes/deleted/`                | Required       | List soft-deleted tithes                               |
| `GET`          | `/tithes/by-member/{member_id}/`  | Required       | List active tithes for a member                        |
| `GET`          | `/tithes/export-pdf/{member_id}/` | Required       | Download a member tithe report as PDF                  |
| `GET`          | `/tithes/analytics/`              | Required       | Get tithe totals, member summaries, and monthly trends |

Tithe list and PDF export requests support `date_given__gte`, `date_given__lte`, and `member` filters. Analytics supports `year` and `month` query parameters.

### Bulk SMS

| Method | Endpoint                          | Authentication | Description                                                  |
| ------ | --------------------------------- | -------------- | ------------------------------------------------------------ |
| `POST` | `/bulksms/send/`                  | No             | Send a message to a JSON list of recipients                  |
| `POST` | `/bulksms/send/csv/`              | No             | Send a message to phone numbers from a CSV upload            |
| `POST` | `/bulksms/send/template-sms/csv/` | No             | Send template parameters and phone numbers from a CSV upload |

CSV uploads expect `Phone Number` and `Full Name` columns. The template form uses all columns except `Phone Number` as template parameters.

### Django and API Documentation

| Method | Endpoint   | Authentication     | Description           |
| ------ | ---------- | ------------------ | --------------------- |
| `GET`  | `/admin/`  | Django admin login | Django administration |
| `GET`  | `/schema/` | No                 | OpenAPI schema        |
| `GET`  | `/docs/`   | No                 | Swagger UI            |

## Authentication

The API uses JWT bearer authentication:

```http
Authorization: Bearer <access-token>
```

Obtain tokens through the login endpoint, then send the access token with protected requests. Refresh tokens are rotated, and the prior refresh token is blacklisted when configured in `SIMPLE_JWT`.

## Tests

```bash
python manage.py test
```

## Deployment

The repository includes `render.yaml` and `build.sh` for deployment on Render. The Render service uses Gunicorn with Uvicorn workers and applies migrations during the build:

```bash
./build.sh
python3 -m gunicorn cmsapi.asgi:application -k uvicorn.workers.UvicornWorker
```

For production, replace the development SECRET_KEY and database configuration with environment-based settings, and restrict `ALLOWED_HOSTS` and CORS origins.
