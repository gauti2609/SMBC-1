-- ============================================================================
-- PostgreSQL Permission Setup for Financial Automation
-- ============================================================================
-- IMPORTANT: Run this as the 'postgres' superuser!
-- In pgAdmin: Right-click "financial_automation" database → Query Tool
-- In psql: Connect as postgres user first
-- ============================================================================

-- Step 1: Connect to the database (psql only, skip in pgAdmin)
-- \c financial_automation

-- Step 2: Grant database-level privileges
GRANT ALL PRIVILEGES ON DATABASE financial_automation TO fin_app_user;

-- Step 3: Grant schema-level privileges
GRANT ALL ON SCHEMA public TO fin_app_user;
GRANT CREATE ON SCHEMA public TO fin_app_user;
GRANT USAGE ON SCHEMA public TO fin_app_user;

-- Step 4: Grant privileges on existing tables
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO fin_app_user;

-- Step 5: Grant privileges on existing sequences (for SERIAL columns)
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO fin_app_user;

-- Step 6: Grant privileges on existing functions
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO fin_app_user;

-- Step 7: Set default privileges for future objects
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO fin_app_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO fin_app_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON FUNCTIONS TO fin_app_user;

-- Step 8: CRITICAL - Make fin_app_user the owner of the schema
ALTER SCHEMA public OWNER TO fin_app_user;

-- ============================================================================
-- ALTERNATIVE: If above doesn't work, make fin_app_user a SUPERUSER
-- ============================================================================
-- Uncomment the line below if you still get permission errors:
-- ALTER USER fin_app_user WITH SUPERUSER;

-- Step 9: Verify permissions
SELECT 
    grantee, 
    privilege_type 
FROM 
    information_schema.role_table_grants 
WHERE 
    grantee = 'fin_app_user';

-- Step 10: Display user roles
\du fin_app_user

-- ============================================================================
-- Expected Output:
-- ============================================================================
-- GRANT (multiple times)
-- ALTER SCHEMA
-- (Table showing SELECT, INSERT, UPDATE, DELETE, etc.)
-- Role name: fin_app_user | Attributes: []
-- ============================================================================

-- Done! Now try running: python demo_db_setup_simple.py
