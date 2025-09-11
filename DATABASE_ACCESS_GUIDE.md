# מדריך גישה למסד הנתונים דרך Docker

## 🐘 גישה למסד הנתונים PostgreSQL

### 1. דרך פקודות Docker (הדרך הפשותה):

```bash
# כניסה לקונטיינר עם PostgreSQL CLI
cd /mnt/d/המסמכים/Documents/practec-project/AI-Driven-Learning-Platform/backend
docker exec -it ai_learning_db_container psql -U postgres -d ai_learning_platform

# או עם פקודה אחת מכל מקום:
docker exec -it ai_learning_db_container psql -U postgres -d ai_learning_platform
```

### 2. פקודות SQL שימושיות במסד:

```sql
-- הצגת כל הטבלאות
\dt

-- הצגת כל המשתמשים
SELECT id, name, email, role, is_active, created_at FROM users;

-- הצגת משתמש admin
SELECT * FROM users WHERE role = 'admin';

-- הצגת כל ההיסטוריה
SELECT p.id, p.prompt, u.name as user_name, u.email, 
       c.name as category, sc.name as subcategory, 
       p.created_at
FROM prompts p
LEFT JOIN users u ON p.user_id = u.id
LEFT JOIN categories c ON p.category_id = c.id
LEFT JOIN sub_categories sc ON p.sub_category_id = sc.id
ORDER BY p.created_at DESC;

-- יצירת משתמש admin חדש (אם צריך)
INSERT INTO users (name, email, password_hash, role, is_active) 
VALUES ('New Admin', 'newadmin@example.com', '$2b$12$hashedpassword', 'admin', true);

-- עדכון משתמש קיים להיות admin
UPDATE users SET role = 'admin' WHERE email = 'user@example.com';

-- מחיקת משתמש
DELETE FROM users WHERE id = 5;
```

### 3. יציאה מ-psql:
```sql
\q
```

### 4. גישה עם כלים חיצוניים:

**פרטי החיבור:**
- Host: localhost
- Port: 5433
- Database: ai_learning_platform
- Username: postgres  
- Password: postgres123

**כלים מומלצים:**
- pgAdmin 4
- DBeaver
- DataGrip
- VS Code עם PostgreSQL extension

### 5. פקודות Docker נוספות:

```bash
# עצירה והפעלה של הקונטיינר
docker stop ai_learning_db_container
docker start ai_learning_db_container

# צפייה בלוגים
docker logs ai_learning_db_container

# עדכון compose (אם שינית משהו)
docker-compose down
docker-compose up -d
```

### 6. גיבוי ושחזור:

```bash
# גיבוי מסד הנתונים
docker exec ai_learning_db_container pg_dump -U postgres ai_learning_platform > backup.sql

# שחזור מגיבוי
docker exec -i ai_learning_db_container psql -U postgres ai_learning_platform < backup.sql
```

## 🛡️ פרטי משתמש Admin שנוצר:

- **Email:** admin@learningplatform.com
- **Password:** admin123
- **Role:** admin

## ⚠️ הערות חשובות:

1. **אבטחה:** סיסמת ה-admin זמנית - שנה אותה מיד!
2. **גיבויים:** עשה גיבויים קבועים למסד הנתונים
3. **הרשאות:** כל פעולות ה-admin מתועדות בלוגים
4. **פורט:** המסד פועל על פורט 5433 (לא 5432 הסטנדרטי)
