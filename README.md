# 🧳 Yatra Planner

Yatra Planner is a travel planning and aggregation platform built with **FastAPI** that combines multiple travel-related services into a single API. It provides weather forecasts, tourist attractions, currency exchange rates, and real-time updates using **Server-Sent Events (SSE)**.

---

## 🚀 Features

- 🌤️ Weather Forecast Integration
- 📍 Tourist Attractions & Places Recommendations
- 💱 Real-Time Currency Exchange Rates
- 📡 Server-Sent Events (SSE) Streaming
- ⚡ FastAPI-based REST APIs
- 📝 Request Validation using Pydantic
- 🔄 Asynchronous API Calls with HTTPX
- 📖 Interactive Swagger Documentation

---

## 🏗️ Tech Stack

### Backend
- FastAPI
- Python
- Pydantic
- HTTPX
- Uvicorn

### APIs Used
- WeatherAPI
- ExchangeRate API
- Custom Places Service

---

## 📂 Project Structure

```text
Yatra-Planner/
│
├── app/
│   ├── routes/
│   │   ├── planner.py
│   │   └── stream.py
│   │
│   ├── services/
│   │   ├── weather.py
│   │   ├── places.py
│   │   └── currency.py
│   │
│   ├── models.py
│   └── main.py
│
├── .env
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/your-username/yatra-planner.git
cd yatra-planner
```

### Create Virtual Environment

```bash
python -m venv env
```

### Activate Virtual Environment

#### Windows

```bash
env\Scripts\activate
```

#### Linux/Mac

```bash
source env/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the root directory.

```env
WEATHERAPI_API_KEY=your_weatherapi_key
EXCHANGERATE_API_KEY=your_exchange_rate_api_key
```

---

## ▶️ Run the Application

```bash
python -m uvicorn app.main:app --reload
```

Server runs at:

```text
http://127.0.0.1:8000
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 📌 Travel Planner Endpoint

### Create Travel Plan

**POST**

```http
/plan
```

### Request Body

```json
{
  "destination": "Delhi",
  "start_date": "2026-09-23",
  "end_date": "2026-09-24",
  "base_currency": "INR"
}
```

### Sample Response

```json
{
  "message": "Travel plan created successfully",
  "weather_data": [],
  "places_data": [],
  "currency_rates": {}
}
```

---

## 📡 SSE Streaming Endpoint

### Stream Travel Plan Progress

**POST**

```http
/stream
```

### Events

```text
start
weather
weather_complete
places
places_complete
currency
currency_complete
complete
```

### Example SSE Response

```text
event: start
data: {"message":"Starting travel plan aggregation..."}

event: weather
data: {"message":"Fetching weather information..."}

event: weather_complete
data: {...}

event: places_complete
data: {...}

event: currency_complete
data: {...}

event: complete
data: {"message":"Travel plan generated successfully"}
```

---

## 🧪 Testing

Use Swagger UI:

```text
http://127.0.0.1:8000/docs
```

Or test using cURL:

```bash
curl -X POST "http://127.0.0.1:8000/plan" \
-H "Content-Type: application/json" \
-d '{
  "destination":"Delhi",
  "start_date":"2026-09-23",
  "end_date":"2026-09-24",
  "base_currency":"INR"
}'
```

---

## 🎯 Future Enhancements

- Hotel Recommendations
- Flight Search Integration
- AI-Powered Itinerary Generation
- User Authentication
- Travel Budget Estimation
- Database Integration
- Deployment on Render/AWS

---

## 👨‍💻 Author

**Shaik Riyaz**

- Backend Developer
- Python & FastAPI Enthusiast
- Passionate about building scalable APIs

---

