# README: Environment Configuration

## How to set up your `.env` file

Before running the backend, you **must create a `.env` file** in the `backend` directory.  
This file is required for database connection, API settings, and OpenAI integration.

### Example `.env` file

Create a file named `.env` in `backend/` and add the following content:

```ini
DATABASE_URL=mysql+pymysql://<username>:<password>@localhost:3306/<database_name>
API_PREFIX=/api
DEBUG=True

ALLOWED_ORIGINS=https://localhost:3000,https://localhost:5173
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Field descriptions

- **DATABASE_URL**  
  Your MySQL connection string. Replace `<username>`, `<password>`, and `<database_name>` with your own settings.

- **API_PREFIX**  
  The prefix for your API endpoints (default: `/api`).

- **DEBUG**  
  Set to `True` for development mode, `False` for production.

- **ALLOWED_ORIGINS**  
  Comma-separated list of allowed frontend origins (for CORS).

- **OPENAI_API_KEY**  
  Your OpenAI API key.  
  You must obtain this from [OpenAI Platform](https://platform.openai.com/api-keys).

---

**Note:**  
Do **not** commit your `.env` file to version control.  
Keep your API keys and sensitive information secure.