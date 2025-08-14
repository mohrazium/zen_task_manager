-- init-db/init.sql
CREATE DATABASE zen_task_manager_db;
CREATE USER zen_task_manager_user WITH PASSWORD 'Z3n#T45k#M4n4g3r#P455w0rd';
GRANT ALL PRIVILEGES ON DATABASE zen_task_manager_db TO zen_task_manager_user;