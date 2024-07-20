
# Zajil API Documentation 🌟

## Introduction 🎉
Welcome to the Zajil API documentation! This project, built with Flask, enables voice and text order management, chat history retrieval, and invoice generation. Below are the available API endpoints:

**Base URL:** 
```
https://api.call-gpt.tech
```

## Endpoints 📝

### 1. Convert Text to Voice 📋
To convert text to voice, send a POST request to `/api/v1/order/voice/<chat_id>` with a JSON payload containing the `text`. AI will generate a response and produce a corresponding audio file.

- **Request Format:**
  ```json
  {
    "text": "Your text here"
  }
  ```

- **Response:**
  ```json
  {
    "voiceLink": "https://api.call-gpt.tech/api/v1/voice/<voice_id>"
  }
  ```

### 2. Chat 🔐
To start a chat session, send a POST request to `/api/v1/order/chat/<chat_id>` with a JSON payload containing the `text`. The AI will respond, and the chat history will be recorded in the database.

- **Request Format:**
  ```json
  {
    "text": "Your text here"
  }
  ```

- **Response:**
  ```json
  {
    "response": "AI's response here"
  }
  ```

### 3. View Chat History ♻️
To retrieve the chat history for a given `chat_id`, send a GET request to `/api/v1/order/history/<chat_id>`. It returns all recorded messages in the chat.

- **Response:**
  ```json
  {
    "chat_history": [
      {
        "role": "user",
        "content": "Message content here"
      },
      {
        "role": "system",
        "content": "AI response here"
      }
    ]
  }
  ```

### 4. Close Order and Generate Invoice ✅
To close an order and generate an invoice, send a GET request to `/api/v1/order/close/<chat_id>`. AI will summarize the order details, and an invoice will be created.

- **Response:**
  ```json
  {
    "response": "Order closed successfully"
  }
  ```

### 5. Get All Orders 📑
To retrieve all orders for a specific user, send a GET request to `/api/v1/get_all_orders`. Include the user's phone number in the request headers.

- **Request Header:**
  ```
  phone: User's phone number
  ```

- **Response:**
  ```json
  {
    "orders": [
      {
        "order": "Order details here",
        "status": "Order status",
        "price": "Order price",
        "location": "Order location"
      }
    ]
  }
  ```

### 6. Get All Products 🛒
To retrieve all products available, send a GET request to `/api/v1/get_all_products`.

- **Response:**
  ```json
  {
    "products": [
      {
        "name": "Product name",
        "price": "Product price",
        "ingredients": "Product ingredients",
        "category": "Product category",
        "stock": "Product stock"
      }
    ]
  }
  ```
