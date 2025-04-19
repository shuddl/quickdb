#!/usr/bin/env python3

'''
QuickDB - Client Information Management System
Main application entry point
'''

import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

from models import db, User, Client, Service, Note
from forms import LoginForm, ClientForm, ServiceForm, NoteForm, UserForm
from utils.auth import is_admin

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('APP_SECRET_KEY', 'dev_key')

# Initialize database
db.init_app(app)

# Initialize Login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = User.get_by_username(username)
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        
        flash('Invalid username or password', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Get counts for dashboard stats
    client_count = Client.get_count()
    active_client_count = Client.get_count(status='Active')
    prospects_count = Client.get_count(status='Prospect')
    
    return render_template(
        'dashboard.html',
        client_count=client_count,
        active_client_count=active_client_count,
        prospects_count=prospects_count
    )

# Client routes
@app.route('/clients')
@login_required
def clients():
    search = request.args.get('search', '')
    status = request.args.get('status', '')
    clients_list = Client.get_all(search=search, status=status)
    return render_template('clients/index.html', clients=clients_list, search=search, status=status)

@app.route('/clients/new', methods=['GET', 'POST'])
@login_required
def new_client():
    form = ClientForm()
    if form.validate_on_submit():
        client = Client(
            client_name=form.client_name.data,
            primary_contact_name=form.primary_contact_name.data,
            primary_contact_email=form.primary_contact_email.data,
            primary_contact_phone=form.primary_contact_phone.data,
            company_address=form.company_address.data,
            client_status=form.client_status.data
        )
        client.save()
        flash('Client added successfully', 'success')
        return redirect(url_for('clients'))
    
    return render_template('clients/form.html', form=form, title='New Client')

@app.route('/clients/<int:client_id>')
@login_required
def view_client(client_id):
    client = Client.get_by_id(client_id)
    if not client:
        flash('Client not found', 'danger')
        return redirect(url_for('clients'))
    
    services = Service.get_by_client(client_id)
    notes = Note.get_by_client(client_id)
    
    return render_template(
        'clients/view.html',
        client=client,
        services=services,
        notes=notes
    )

@app.route('/clients/<int:client_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_client(client_id):
    client = Client.get_by_id(client_id)
    if not client:
        flash('Client not found', 'danger')
        return redirect(url_for('clients'))
    
    form = ClientForm(obj=client)
    if form.validate_on_submit():
        client.client_name = form.client_name.data
        client.primary_contact_name = form.primary_contact_name.data
        client.primary_contact_email = form.primary_contact_email.data
        client.primary_contact_phone = form.primary_contact_phone.data
        client.company_address = form.company_address.data
        client.client_status = form.client_status.data
        client.save()
        
        flash('Client updated successfully', 'success')
        return redirect(url_for('view_client', client_id=client_id))
    
    return render_template('clients/form.html', form=form, title='Edit Client')

# Service routes
@app.route('/clients/<int:client_id>/services/new', methods=['GET', 'POST'])
@login_required
def new_service(client_id):
    client = Client.get_by_id(client_id)
    if not client:
        flash('Client not found', 'danger')
        return redirect(url_for('clients'))
    
    form = ServiceForm()
    if form.validate_on_submit():
        service = Service(
            client_id=client_id,
            service_name=form.service_name.data,
            engagement_date=form.engagement_date.data,
            service_status=form.service_status.data
        )
        service.save()
        
        flash('Service added successfully', 'success')
        return redirect(url_for('view_client', client_id=client_id))
    
    return render_template(
        'services/form.html',
        form=form,
        client=client,
        title='New Service'
    )

# Note routes
@app.route('/clients/<int:client_id>/notes/new', methods=['GET', 'POST'])
@login_required
def new_note(client_id):
    client = Client.get_by_id(client_id)
    if not client:
        flash('Client not found', 'danger')
        return redirect(url_for('clients'))
    
    form = NoteForm()
    if form.validate_on_submit():
        note = Note(
            client_id=client_id,
            user_id=current_user.id,
            note_text=form.note_text.data
        )
        note.save()
        
        flash('Note added successfully', 'success')
        return redirect(url_for('view_client', client_id=client_id))
    
    return render_template(
        'notes/form.html',
        form=form,
        client=client,
        title='New Note'
    )

# Admin routes
@app.route('/users')
@login_required
def users():
    if not is_admin(current_user):
        flash('Access denied', 'danger')
        return redirect(url_for('dashboard'))
    
    users_list = User.get_all()
    return render_template('users/index.html', users=users_list)

@app.route('/users/new', methods=['GET', 'POST'])
@login_required
def new_user():
    if not is_admin(current_user):
        flash('Access denied', 'danger')
        return redirect(url_for('dashboard'))
    
    form = UserForm()
    if form.validate_on_submit():
        # Check if username already exists
        if User.get_by_username(form.username.data):
            flash('Username already exists', 'danger')
            return render_template('users/form.html', form=form, title='New User')
        
        user = User(
            username=form.username.data,
            role=form.role.data,
            is_active=form.is_active.data
        )
        user.set_password(form.password.data)
        user.save()
        
        flash('User added successfully', 'success')
        return redirect(url_for('users'))
    
    return render_template('users/form.html', form=form, title='New User')

@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if not is_admin(current_user):
        flash('Access denied', 'danger')
        return redirect(url_for('dashboard'))
    
    user = User.get_by_id(user_id)
    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('users'))
    
    # Prevent editing yourself
    if user.id == current_user.id:
        flash('Cannot edit your own account', 'danger')
        return redirect(url_for('users'))
    
    form = UserForm(obj=user)
    if form.validate_on_submit():
        # Check if username already exists and is not the current user
        existing_user = User.get_by_username(form.username.data)
        if existing_user and existing_user.id != user_id:
            flash('Username already exists', 'danger')
            return render_template('users/form.html', form=form, title='Edit User')
        
        user.username = form.username.data
        user.role = form.role.data
        user.is_active = form.is_active.data
        
        # Update password if provided
        if form.password.data:
            user.set_password(form.password.data)
        
        user.save()
        flash('User updated successfully', 'success')
        return redirect(url_for('users'))
    
    # Don't send password to form
    form.password.data = ''
    
    return render_template('users/form.html', form=form, title='Edit User')

if __name__ == '__main__':
    host = os.getenv('HOST', '0.0.0.0')  # Changed to 0.0.0.0 to allow external connections
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'True').lower() == 'true'  # Changed default to True
    
    print(f"Starting server on {host}:{port}")
    print(f"Access the application in your browser at: http://localhost:{port}")
    print(f"Press CTRL+C to stop the server")
    
    app.run(host=host, port=port, debug=debug)
