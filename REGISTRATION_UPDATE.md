# Registration Update - First Name & Last Name

## Changes Made

### 1. Database Schema Updated ✅

Added two new columns to the `users` table:
- `first_name` TEXT
- `last_name` TEXT

**Migration:**
```bash
python migrate_add_names.py
```

### 2. API Updated ✅

**RegisterRequest Model:**
```python
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
```

**Database Insert:**
```python
await db.conn.execute(
    "INSERT INTO users (id, email, hashed_password, first_name, last_name) VALUES (?, ?, ?, ?, ?)",
    (user_id, req.email, hashed_pw, req.first_name, req.last_name)
)
```

### 3. Frontend Updated ✅

**New Registration Form Fields:**
- First Name (required)
- Last Name (required)
- Email (required)
- Password (required)
- Confirm Password (required)

**Layout:**
- First Name and Last Name are side-by-side in a grid
- Clean, modern design
- Proper validation

### 4. URLs Fixed ✅

Changed all authentication URLs from port 8000 to 8080:
- Login: `http://localhost:8080/auth/login`
- Register: `http://localhost:8080/auth/register`

## How to Use

### Register a New User

1. Go to: http://localhost:8080/login
2. Click "Register" tab
3. Fill in the form:
   - **First Name**: John
   - **Last Name**: Doe
   - **Email**: john@example.com
   - **Password**: ••••••••
   - **Confirm Password**: ••••••••
4. Click "Register"
5. You'll be automatically logged in and redirected to the dashboard

### Database Storage

User data is stored in SQLite:

```sql
SELECT id, email, first_name, last_name, created_at 
FROM users;
```

Example output:
```
id                                   | email              | first_name | last_name | created_at
-------------------------------------|--------------------|-----------|-----------|-----------
abc-123-def-456                      | john@example.com   | John      | Doe       | 2025-12-09
```

## Testing

### Test Registration

```bash
curl -X POST http://localhost:8080/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "first_name": "Test",
    "last_name": "User"
  }'
```

Expected response:
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

### Verify in Database

```bash
sqlite3 data/astraflow.db "SELECT email, first_name, last_name FROM users;"
```

## Migration for Existing Databases

If you have an existing database, run the migration:

```bash
python migrate_add_names.py
```

This will:
- Check if columns already exist
- Add `first_name` column if missing
- Add `last_name` column if missing
- Preserve all existing data

## Validation

### Frontend Validation

- ✅ All fields required
- ✅ Email format validation
- ✅ Password minimum 6 characters
- ✅ Password confirmation match
- ✅ Clear error messages

### Backend Validation

- ✅ Email uniqueness check
- ✅ Email format validation (EmailStr)
- ✅ Password hashing with bcrypt
- ✅ Proper error responses

## Display User Name

You can now display the user's full name in the UI:

```javascript
// Get user info from token or API
const userName = `${user.first_name} ${user.last_name}`;
document.getElementById('userName').textContent = userName;
```

## API Response

After successful registration, you get:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

The JWT token contains the user_id, which can be used to fetch user details including first_name and last_name.

## Future Enhancements

### Add User Profile Endpoint

```python
@app.get("/api/user/profile")
async def get_profile(user_id: str = Depends(get_current_user)):
    cursor = await db.conn.execute(
        "SELECT id, email, first_name, last_name, created_at FROM users WHERE id = ?",
        (user_id,)
    )
    row = await cursor.fetchone()
    return {
        "id": row[0],
        "email": row[1],
        "first_name": row[2],
        "last_name": row[3],
        "created_at": row[4]
    }
```

### Display in Chat

Update chat.html to show user's name:
```javascript
async function loadUserProfile() {
    const token = localStorage.getItem('token');
    const response = await fetch('http://localhost:8080/api/user/profile', {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    const user = await response.json();
    document.getElementById('userName').textContent = `${user.first_name} ${user.last_name}`;
}
```

## Files Modified

1. ✅ `services/api_gateway/database.py` - Schema update
2. ✅ `services/api_gateway/main.py` - API update
3. ✅ `templates/login.html` - Form update
4. ✅ `migrate_add_names.py` - Migration script (new)

## Rollback

If you need to rollback:

```sql
-- Remove columns (SQLite doesn't support DROP COLUMN easily)
-- Better to restore from backup or recreate table

-- Backup data
CREATE TABLE users_backup AS SELECT id, email, hashed_password, created_at FROM users;

-- Drop and recreate
DROP TABLE users;
CREATE TABLE users (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Restore data
INSERT INTO users SELECT * FROM users_backup;
DROP TABLE users_backup;
```

## Summary

✅ **Database**: Added first_name and last_name columns
✅ **API**: Updated to accept and store names
✅ **Frontend**: Added input fields for names
✅ **Migration**: Script to update existing databases
✅ **Validation**: All fields required and validated
✅ **Testing**: Verified with curl and browser

**Try it now:**
1. Go to http://localhost:8080/login
2. Click "Register"
3. Fill in your name, email, and password
4. Start chatting!

Your user information is now stored with first and last names in the SQLite database! 🎉
