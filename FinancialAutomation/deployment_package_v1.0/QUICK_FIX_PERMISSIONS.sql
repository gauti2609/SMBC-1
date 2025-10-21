-- ============================================================================
-- QUICK FIX: Make fin_app_user a SUPERUSER
-- ============================================================================
-- This is the EASIEST fix for the permission denied error
-- Run this in pgAdmin Query Tool (connected to ANY database as postgres user)
-- ============================================================================

-- Option A: Make existing user a superuser (RECOMMENDED)
ALTER USER fin_app_user WITH SUPERUSER;

-- Verify (should show "Superuser" in attributes)
\du fin_app_user

-- ============================================================================
-- Option B: If Option A fails, recreate user as superuser
-- ============================================================================
-- WARNING: This will disconnect any active sessions!
-- Only use if Option A gives an error

-- Disconnect all sessions
-- SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE usename = 'fin_app_user';

-- Drop and recreate
-- DROP USER IF EXISTS fin_app_user;
-- CREATE USER fin_app_user WITH SUPERUSER PASSWORD 'your_password_from_env_file';

-- Grant ownership
-- ALTER DATABASE financial_automation OWNER TO fin_app_user;

-- ============================================================================
-- DONE! Now test with:
-- python demo_db_setup_simple.py
-- ============================================================================
