#!/usr/bin/env python3

'''
Database initialization script

This script creates the database schema and initializes an admin user.
'''

import os
import sys
import argparse
import getpass
import bcrypt
import sqlite3
import pathlib
from dotenv import load_dotenv

def parse_args():
    parser = argparse.ArgumentParser(description="Initialize the QuickDB database")
    parser.add_argument('--reset', action='store_true', help='Drop existing tables before creating new ones')
    parser.add_argument('--username', help='Admin username (default: admin)')
    parser.add_argument('--password', help='Admin password (default: admin)')
    parser.add_argument('--non-interactive', action='store_true', help='Run without prompting for input')
    return parser.parse_args()

def connect_to_db():
    # Get the path to the SQLite database file
    base_dir = pathlib.Path(__file__).parent.parent
    db_path = os.path.join(base_dir, 'quickdb.db')
    
    # Create a connection to the SQLite database
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    
    print(f"Connected to database: {db_path}")
    return conn

def create_tables(conn, reset=False):
    cursor = conn.cursor()
    
    if reset:
        # Drop tables if they exist
        cursor.execute("DROP TABLE IF EXISTS notes")
        cursor.execute("DROP TABLE IF EXISTS services")
        cursor.execute("DROP TABLE IF EXISTS clients")
        cursor.execute("DROP TABLE IF EXISTS users")
    
    # Enable foreign key constraints
    cursor.execute("PRAGMA foreign_keys = ON")
    
    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('Admin', 'Staff')) DEFAULT 'Staff',
        is_active INTEGER NOT NULL DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Create clients table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        client_id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_name TEXT NOT NULL,
        primary_contact_name TEXT,
        primary_contact_email TEXT,
        primary_contact_phone TEXT,
        company_address TEXT,
        client_status TEXT NOT NULL CHECK(client_status IN ('Active', 'Inactive', 'Prospect')) DEFAULT 'Prospect',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Create indexes for clients table
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_client_name ON clients (client_name)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_client_status ON clients (client_status)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_contact_email ON clients (primary_contact_email)")
    
    # Create services table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS services (
        service_id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER NOT NULL,
        service_name TEXT NOT NULL,
        engagement_date DATE,
        service_status TEXT NOT NULL CHECK(service_status IN ('Planned', 'In Progress', 'Completed', 'Cancelled')) DEFAULT 'Planned',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (client_id) REFERENCES clients(client_id)
    )
    """)
    
    # Create index for services table
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_service_client_id ON services (client_id)")
    
    # Create notes table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        note_id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        note_text TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (client_id) REFERENCES clients(client_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    """)
    
    # Create indexes for notes table
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_note_client_id ON notes (client_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_note_user_id ON notes (user_id)")
    
    conn.commit()
    print("Database tables created successfully")

def create_admin_user(conn, args):
    cursor = conn.cursor()
    
    # Check if admin user already exists
    cursor.execute("SELECT COUNT(*) as count FROM users WHERE role='Admin'")
    admin_count = cursor.fetchone()['count']
    
    if admin_count > 0 and not args.reset:
        if args.non_interactive:
            print("Admin user already exists. Skipping.")
            return
        else:
            create_new = input("Admin user already exists. Create another? (y/n): ").lower() == 'y'
            if not create_new:
                cursor.close()
                return
    
    # Get admin username and password
    if args.non_interactive or args.username and args.password:
        username = args.username or 'admin'
        password = args.password or 'admin'
        confirm_password = password
        print(f"Creating admin user '{username}' with supplied or default password")
    else:
        try:
            username = input("Enter admin username: ")
            password = getpass.getpass("Enter admin password: ")
            confirm_password = getpass.getpass("Confirm admin password: ")
        except (EOFError, KeyboardInterrupt):
            print("\nUsing default admin credentials (admin/admin)")
            username = 'admin'
            password = 'admin'
            confirm_password = password
    
    if password != confirm_password:
        print("Passwords do not match")
        return
    
    # Hash the password
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Insert admin user
    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, 'Admin')",
            (username, password_hash)
        )
        conn.commit()
        print(f"Admin user '{username}' created successfully")
    except sqlite3.Error as err:
        print(f"Error creating admin user: {err}")
        conn.rollback()

def main():
    args = parse_args()
    conn = connect_to_db()
    create_tables(conn, reset=args.reset)
    create_admin_user(conn, args)
    conn.close()
    print("Database initialization complete")

if __name__ == '__main__':
    main()