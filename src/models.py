'''
Database models for the QuickDB application
'''

import bcrypt
import sqlite3
import os
from flask import current_app, g
from flask_login import UserMixin
from datetime import datetime

class Database:
    def __init__(self):
        self.app = None
    
    def init_app(self, app):
        self.app = app
        self.app.teardown_appcontext(self.close_db)
    
    def get_db(self):
        if 'db' not in g:
            db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'quickdb.db')
            g.db = sqlite3.connect(db_path)
            g.db.row_factory = sqlite3.Row
            g.cursor = g.db.cursor()
        return g.db, g.cursor
    
    def close_db(self, e=None):
        db = g.pop('db', None)
        cursor = g.pop('cursor', None)
        
        if cursor:
            cursor.close()
        
        if db is not None:
            db.close()

db = Database()

class User(UserMixin):
    def __init__(self, username=None, password_hash=None, role='Staff', is_active=True, created_at=None, updated_at=None, user_id=None):
        self.id = user_id
        self.username = username
        self.password_hash = password_hash
        self.role = role
        self.is_active = bool(is_active)
        self.created_at = created_at
        self.updated_at = updated_at
    
    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def save(self):
        conn, cursor = db.get_db()
        
        if self.id:
            # Update existing user
            query = """
            UPDATE users 
            SET username = ?, password_hash = ?, role = ?, is_active = ? 
            WHERE user_id = ?
            """
            cursor.execute(query, (self.username, self.password_hash, self.role, self.is_active, self.id))
        else:
            # Insert new user
            query = """
            INSERT INTO users (username, password_hash, role, is_active) 
            VALUES (?, ?, ?, ?)
            """
            cursor.execute(query, (self.username, self.password_hash, self.role, self.is_active))
            self.id = cursor.lastrowid
        
        conn.commit()
        return self
    
    @staticmethod
    def get_by_id(user_id):
        _, cursor = db.get_db()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user_data = cursor.fetchone()
        
        if not user_data:
            return None
        
        return User(
            user_id=user_data['user_id'],
            username=user_data['username'],
            password_hash=user_data['password_hash'],
            role=user_data['role'],
            is_active=user_data['is_active'],
            created_at=user_data['created_at'],
            updated_at=user_data['updated_at']
        )
    
    @staticmethod
    def get_by_username(username):
        _, cursor = db.get_db()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user_data = cursor.fetchone()
        
        if not user_data:
            return None
        
        return User(
            user_id=user_data['user_id'],
            username=user_data['username'],
            password_hash=user_data['password_hash'],
            role=user_data['role'],
            is_active=user_data['is_active'],
            created_at=user_data['created_at'],
            updated_at=user_data['updated_at']
        )
    
    @staticmethod
    def get_all():
        _, cursor = db.get_db()
        cursor.execute("SELECT * FROM users ORDER BY username")
        users_data = cursor.fetchall()
        
        return [User(
            user_id=user_data['user_id'],
            username=user_data['username'],
            password_hash=user_data['password_hash'],
            role=user_data['role'],
            is_active=user_data['is_active'],
            created_at=user_data['created_at'],
            updated_at=user_data['updated_at']
        ) for user_data in users_data]

class Client:
    def __init__(self, client_name=None, primary_contact_name=None, primary_contact_email=None, 
                 primary_contact_phone=None, company_address=None, client_status='Prospect', 
                 created_at=None, updated_at=None, client_id=None):
        self.id = client_id
        self.client_name = client_name
        self.primary_contact_name = primary_contact_name
        self.primary_contact_email = primary_contact_email
        self.primary_contact_phone = primary_contact_phone
        self.company_address = company_address
        self.client_status = client_status
        self.created_at = created_at
        self.updated_at = updated_at
    
    def save(self):
        conn, cursor = db.get_db()
        
        if self.id:
            # Update existing client
            query = """
            UPDATE clients 
            SET client_name = ?, primary_contact_name = ?, primary_contact_email = ?, 
                primary_contact_phone = ?, company_address = ?, client_status = ? 
            WHERE client_id = ?
            """
            cursor.execute(query, (
                self.client_name, self.primary_contact_name, self.primary_contact_email,
                self.primary_contact_phone, self.company_address, self.client_status, self.id
            ))
        else:
            # Insert new client
            query = """
            INSERT INTO clients 
            (client_name, primary_contact_name, primary_contact_email, primary_contact_phone, 
             company_address, client_status, created_at, updated_at) 
            VALUES (?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))
            """
            cursor.execute(query, (
                self.client_name, self.primary_contact_name, self.primary_contact_email,
                self.primary_contact_phone, self.company_address, self.client_status
            ))
            self.id = cursor.lastrowid
        
        conn.commit()
        return self
    
    @staticmethod
    def get_by_id(client_id):
        _, cursor = db.get_db()
        cursor.execute("SELECT * FROM clients WHERE client_id = ?", (client_id,))
        client_data = cursor.fetchone()
        
        if not client_data:
            return None
        
        return Client(
            client_id=client_data['client_id'],
            client_name=client_data['client_name'],
            primary_contact_name=client_data['primary_contact_name'],
            primary_contact_email=client_data['primary_contact_email'],
            primary_contact_phone=client_data['primary_contact_phone'],
            company_address=client_data['company_address'],
            client_status=client_data['client_status'],
            created_at=client_data['created_at'],
            updated_at=client_data['updated_at']
        )
    
    @staticmethod
    def get_all(search='', status=''):
        conn, cursor = db.get_db()
        
        query = "SELECT * FROM clients"
        params = []
        
        where_conditions = []
        if search:
            where_conditions.append("(client_name LIKE ? OR primary_contact_name LIKE ? OR primary_contact_email LIKE ?)")
            search_param = f'%{search}%'
            params.extend([search_param, search_param, search_param])
        
        if status:
            where_conditions.append("client_status = ?")
            params.append(status)
        
        if where_conditions:
            query += " WHERE " + " AND ".join(where_conditions)
        
        query += " ORDER BY client_name"
        
        cursor.execute(query, params)
        clients_data = cursor.fetchall()
        
        return [Client(
            client_id=client_data['client_id'],
            client_name=client_data['client_name'],
            primary_contact_name=client_data['primary_contact_name'],
            primary_contact_email=client_data['primary_contact_email'],
            primary_contact_phone=client_data['primary_contact_phone'],
            company_address=client_data['company_address'],
            client_status=client_data['client_status'],
            created_at=client_data['created_at'],
            updated_at=client_data['updated_at']
        ) for client_data in clients_data]
    
    @staticmethod
    def get_count(status=None):
        conn, cursor = db.get_db()
        
        query = "SELECT COUNT(*) as count FROM clients"
        params = []
        
        if status:
            query += " WHERE client_status = ?"
            params.append(status)
        
        cursor.execute(query, params)
        result = cursor.fetchone()
        return result['count']

class Service:
    def __init__(self, client_id=None, service_name=None, engagement_date=None, 
                 service_status='Planned', created_at=None, updated_at=None, service_id=None):
        self.id = service_id
        self.client_id = client_id
        self.service_name = service_name
        self.engagement_date = engagement_date
        self.service_status = service_status
        self.created_at = created_at
        self.updated_at = updated_at
    
    def save(self):
        conn, cursor = db.get_db()
        
        if self.id:
            # Update existing service
            query = """
            UPDATE services 
            SET client_id = ?, service_name = ?, engagement_date = ?, service_status = ? 
            WHERE service_id = ?
            """
            cursor.execute(query, (
                self.client_id, self.service_name, self.engagement_date, 
                self.service_status, self.id
            ))
        else:
            # Insert new service
            query = """
            INSERT INTO services 
            (client_id, service_name, engagement_date, service_status, created_at, updated_at) 
            VALUES (?, ?, ?, ?, datetime('now'), datetime('now'))
            """
            cursor.execute(query, (
                self.client_id, self.service_name, self.engagement_date, self.service_status
            ))
            self.id = cursor.lastrowid
        
        conn.commit()
        return self
    
    @staticmethod
    def get_by_id(service_id):
        _, cursor = db.get_db()
        cursor.execute("SELECT * FROM services WHERE service_id = ?", (service_id,))
        service_data = cursor.fetchone()
        
        if not service_data:
            return None
        
        return Service(
            service_id=service_data['service_id'],
            client_id=service_data['client_id'],
            service_name=service_data['service_name'],
            engagement_date=service_data['engagement_date'],
            service_status=service_data['service_status'],
            created_at=service_data['created_at'],
            updated_at=service_data['updated_at']
        )
    
    @staticmethod
    def get_by_client(client_id):
        _, cursor = db.get_db()
        cursor.execute(
            "SELECT * FROM services WHERE client_id = ? ORDER BY engagement_date DESC", 
            (client_id,)
        )
        services_data = cursor.fetchall()
        
        return [Service(
            service_id=service_data['service_id'],
            client_id=service_data['client_id'],
            service_name=service_data['service_name'],
            engagement_date=service_data['engagement_date'],
            service_status=service_data['service_status'],
            created_at=service_data['created_at'],
            updated_at=service_data['updated_at']
        ) for service_data in services_data]

class Note:
    def __init__(self, client_id=None, user_id=None, note_text=None, 
                 created_at=None, note_id=None):
        self.id = note_id
        self.client_id = client_id
        self.user_id = user_id
        self.note_text = note_text
        self.created_at = created_at
        self.user = None  # To store the user who created the note
    
    def save(self):
        conn, cursor = db.get_db()
        
        if self.id:
            # Update existing note
            query = """
            UPDATE notes 
            SET client_id = ?, user_id = ?, note_text = ? 
            WHERE note_id = ?
            """
            cursor.execute(query, (
                self.client_id, self.user_id, self.note_text, self.id
            ))
        else:
            # Insert new note
            query = """
            INSERT INTO notes 
            (client_id, user_id, note_text, created_at) 
            VALUES (?, ?, ?, datetime('now'))
            """
            cursor.execute(query, (
                self.client_id, self.user_id, self.note_text
            ))
            self.id = cursor.lastrowid
        
        conn.commit()
        return self
    
    @staticmethod
    def get_by_id(note_id):
        _, cursor = db.get_db()
        cursor.execute("""
            SELECT n.*, u.username, u.role 
            FROM notes n 
            JOIN users u ON n.user_id = u.user_id 
            WHERE n.note_id = ?
        """, (note_id,))
        note_data = cursor.fetchone()
        
        if not note_data:
            return None
        
        note = Note(
            note_id=note_data['note_id'],
            client_id=note_data['client_id'],
            user_id=note_data['user_id'],
            note_text=note_data['note_text'],
            created_at=note_data['created_at']
        )
        
        # Create a simple user object without password
        note.user = type('User', (), {
            'username': note_data['username'],
            'role': note_data['role']
        })
        
        return note
    
    @staticmethod
    def get_by_client(client_id):
        _, cursor = db.get_db()
        cursor.execute("""
            SELECT n.*, u.username, u.role 
            FROM notes n 
            JOIN users u ON n.user_id = u.user_id 
            WHERE n.client_id = ? 
            ORDER BY n.created_at DESC
        """, (client_id,))
        notes_data = cursor.fetchall()
        
        result = []
        for note_data in notes_data:
            note = Note(
                note_id=note_data['note_id'],
                client_id=note_data['client_id'],
                user_id=note_data['user_id'],
                note_text=note_data['note_text'],
                created_at=note_data['created_at']
            )
            
            # Create a simple user object without password
            note.user = type('User', (), {
                'username': note_data['username'],
                'role': note_data['role']
            })
            
            result.append(note)
        
        return result
