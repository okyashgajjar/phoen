# End-to-End Postman Testing Guide for Phoen CPQ

This guide explains how to perform end-to-end testing of the Phoen CPQ backend API using Postman.

## Prerequisites
1. **Start the Backend Server**:
   Ensure your FastAPI server is running on `http://localhost:8000`.
   ```bash
   cd backend
   python main.py
   ```
2. **Open Postman**: Download and launch the Postman client.

---

## Testing Workflow (Quote-to-Cash)

### Step 1: Login to get the Access Token (Admin)
The system is pre-seeded with a default Admin account when the server starts. You do not need to sign up.

- **Method**: `POST`
- **URL**: `http://localhost:8000/api/v1/auth/login`
- **Body** (Raw JSON):
  ```json
  {
    "email": "admin@phoen.io",
    "password": "password"
  }
  ```
- **Expected Response**: `200 OK` with an `access_token` (e.g., `{"access_token": "admin_1", "token_type": "bearer"}`).
- **Action**: Copy this `access_token`.

### Step 3: Setup Postman Authorization
For all the following requests, you must include the token in the Headers:
1. Go to the **Authorization** tab in Postman.
2. Select **Bearer Token**.
3. Paste the `access_token` from Step 2 into the Token field.

### Step 4: Provision a Sales Representative & Customer
As an admin, you can create other employees and customers using the protected `/users` endpoint.

- **Method**: `POST`
- **URL**: `http://localhost:8000/api/v1/auth/users`
- **Body** (Sales Rep):
  ```json
  {
    "email": "sales@phoen.com",
    "password": "password",
    "name": "Sarah Sales",
    "role": "sales_rep"
  }
  ```
- **Body** (Customer):
  ```json
  {
    "email": "client@acmecorp.com",
    "password": "password",
    "name": "Acme Corp",
    "role": "customer"
  }
  ```

*(To test the rest of the flow from the Sales Rep's perspective, log in with `sales@phoen.com` and use their token).*

### Step 5: Fetch Catalog & Pricing Rules
Before creating a quote, fetch the available products.

- **Method**: `GET`
- **URL**: `http://localhost:8000/api/v1/products/`
- **Expected Response**: A list of catalog items and their pricing tiers.

### Step 6: Create a Quotation (Draft)
Submit a new quote to the system.

- **Method**: `POST`
- **URL**: `http://localhost:8000/api/v1/quotations/`
- **Body** (Raw JSON):
  ```json
  {
    "account": "Acme Corp",
    "title": "Enterprise Cloud Suite",
    "amount": 45000,
    "rep": "Sarah Sales",
    "items": [
      {"sku": "CLOUD-ENT", "qty": 50, "discount_pct": 10}
    ]
  }
  ```

### Step 7: Manager Approval (If Flagged)
If the quote exceeds maximum discount limits, it gets flagged. To approve it, log in as a `manager`, get their token, and hit the approval endpoint.

- **Method**: `POST`
- **URL**: `http://localhost:8000/api/v1/approvals/<QUOTE_ID>/approve`
- **Expected Response**: `200 OK` (Status updates to `APPROVED`).

### Step 8: Customer Negotiation & Acceptance
Simulate the customer accepting the quote in their portal.

- **Method**: `POST`
- **URL**: `http://localhost:8000/api/v1/portal/<QUOTE_ID>/accept`
- **Expected Response**: `200 OK` (Status updates to `WON`).

### Step 9: Fulfillment & Billing
Once the quote is won, push it to fulfillment and generate the invoice.

- **Method**: `POST`
- **URL**: `http://localhost:8000/api/v1/fulfillment/dispatch`
- **Body** (Raw JSON):
  ```json
  { "quote_id": "<QUOTE_ID>" }
  ```

- **Method**: `POST`
- **URL**: `http://localhost:8000/api/v1/billing/invoice`
- **Body** (Raw JSON):
  ```json
  { "quote_id": "<QUOTE_ID>" }
  ```

---

## Health Check
To quickly verify if your API is up and running without authentication:
- **Method**: `GET`
- **URL**: `http://localhost:8000/health`
- **Expected Response**: `{"status": "ok"}`
