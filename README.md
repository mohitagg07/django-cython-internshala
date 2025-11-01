# Django E-commerce & Cython AI Recommender

**Submitted by: Mohit Aggarwal**
**Assignment for: Kumar**

This project is a complete Django e-commerce application that fulfills all assignment requirements, including a Cython-optimized "AI" recommendation engine.

---

## ✅ Features Implemented

* **Task 1 (Django):** Full product display, user cart, and checkout flow.
* **Task 2 (AI Model):** A hybrid recommendation system based on:
    1.  **Content:** Product tags (for initial similarity).
    2.  **User Behavior:** "Like/Dislike" feedback to boost or hide items.
* **Task 3 (Cython):** The entire recommendation algorithm is written in Cython (`recommender_cy.pyx`) and compiled to a `.pyd` module for high performance.
* **Task 4 (User Interaction):** Users can view recommendations, add items to their cart, and provide "Like/Dislike" feedback, which immediately updates future recommendations.

---

## 🚀 How to Run This Project

**CRITICAL: This project requires a C++ compiler to build the Cython module.**

### 1. Prerequisite: Install C++ Compiler
- Download and install **"Build Tools for Visual Studio"**.
- When installing, select the **"Desktop development with C++"** workload.

### 2. Set up the Build Environment
- Open the **Developer Command Prompt for VS** (or run `vcvarsall.bat` as shown in our chat).
- Navigate to the project folder.

### 3. Create Virtual Environment
- `py -m venv venv`
- `.\venv\Scripts\activate`

### 4. Install Dependencies
- `pip install -r requirements.txt`

### 5. Compile the Cython Module
- **This is a mandatory step.**
- `py setup.py build_ext --inplace`
- (This will create the `recommender_cy.cp313-win_amd64.pyd` file in the `shop` folder).

### 6. Set up the Database
- `py manage.py makemigrations`
- `py manage.py migrate`
- `py manage.py createsuperuser` (Create your admin login)

### 7. Run the Server
- `py manage.py runserver`

### 8. How to Test
1.  Go to `http://127.0.0.1:8000/admin/` and log in.
2.  Add 5-10 products with descriptive **tags** (e.g., `laptop, gaming`, `laptop, business`).
3.  Go to `http://127.0.0.1:8000/` to see the site.
4.  Click a product to see the recommendations.
5.  Test the "Like" 👍 and "Dislike" 👎 buttons and watch the recommendations change.
6.  Test the "Add to Cart" and "Checkout" process.
