# MediTrack

## 📌 About
A full-stack project using **React, Python (FastAPI/Flask), MongoDB Atlas, and Streamlit**.  
It manages medicines with role-based access, tracks stock/orders, raises alerts for shortages & expiries, and applies a simple ML model for demand prediction.  

---

## 🚀 Features
- Role-based login (Admin, Supplier, Pharmacist)  
- Inventory management (add, update, delete, track medicines)  
- Order placement & tracking  
- Alerts for low stock and expiring medicines  
- Streamlit dashboards with analytics & ML predictions  
- Cloud database with MongoDB Atlas  

---

## 🏗️ Tech Stack
- **Frontend**: React  
- **Backend**: Python (FastAPI/Flask)  
- **Database**: MongoDB Atlas  
- **Analytics**: Streamlit  
- **Machine Learning**: scikit-learn, pandas, numpy  

---

## 🗺️ Project Roadmap
This project is broken down into four manageable phases, guiding development from the ground up.

### Phase 1: Foundation & Backend Core
This phase focuses on setting up the project environment and building the backend API and database.
-   [x] **Project Setup**: Initialize Git, create project structure (`backend`, `frontend`, `analytics`).
-   [x] **Database Setup**: Set up a MongoDB Atlas cluster and get the connection string.
-   [x] **Backend API**: Initialize a FastAPI project.
-   [x] **Database Schema**: Define models for `users`, `medicines`, and `orders`.
-   [ ] **User Authentication**: Implement user registration, login (with JWT), and role-based access control.

### Phase 2: Core Business Logic
Build the main features of the application on the backend.
-   [ ] **Inventory Management**: Create CRUD endpoints for `Admin` to manage medicines.
-   [ ] **Order Management**: Create endpoints for `Pharmacists` to place orders and for `Suppliers` to update order status.

### Phase 3: Frontend Development with React
Build the user interface to interact with the backend.
-   [ ] **React Setup**: Initialize a React app (e.g., with Vite) and set up `react-router-dom`.
-   [ ] **UI Components**:
    -   [ ] Build `Login` and `Register` pages.
    -   [ ] Design a main `Dashboard` layout with role-based navigation.
    -   [ ] Create pages for `Inventory` and `Orders`.
-   [ ] **API Integration**: Connect React components to the backend API using a library like `axios` and manage application state.

### Phase 4: Advanced Features & Analytics
Add the "smart" features to the application.
-   [ ] **Alerting System**:
    -   [ ] Create a background task in FastAPI to check for low stock and near-expiry medicines.
    -   [ ] Display alerts in the frontend UI.
-   [ ] **Analytics Dashboard**:
    -   [ ] Create a Streamlit application.
    -   [ ] Connect Streamlit to MongoDB to visualize inventory levels and order trends.
-   [ ] **Machine Learning Model**:
    -   [ ] Train a forecasting model (`scikit-learn`) on historical order data.
    -   [ ] Integrate the model into the Streamlit dashboard to predict medicine demand.
