# coding=utf-8

from flask import Blueprint, render_template, flash, redirect, session, url_for, request, g, Markup
from flask_login import login_required, login_user, logout_user, current_user

from clovr_launcher.user.models import User
from clovr_launcher.user.forms import RegisterForm
from clovr_launcher.extensions import login_manager

from .forms import LoginForm

blueprint = Blueprint('public', __name__, static_folder='../static')


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route('/', methods=['GET', 'POST'])
@blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    """Handles logging into our app. The launcher app is slightly unique in 
    that the notion of a user is actually an AWS credential with a 'nickname'
    attached to it. 
    
    The user never actually enters a password instead the password is a 
    combination of the AWS access key and the AWS secret key and is handled
    without the user knowing this."""
    if current_user.is_authenticated:
        return redirect(url_for('vm.start_vm'))

    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user)
            flash('Login successful', 'success')
            return redirect(url_for('vm.start_vm'))
        else:
            flash('Invalid Credentials', 'danger')

    return render_template('public/login.html', form=form)


@blueprint.route('/logout/')
@login_required
def logout():
    """Logout a user from the VM launcher application."""
    logout_user()
    session.pop('_flashes', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('public.login'))


@blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    """Register a new user for the launcher app."""
    if current_user.is_authenticated:
        return redirect(url_for('vm.start_vm'))
    
    form = RegisterForm(request.form, csrf_enabled=False)

    if request.method == "POST":
        if form.validate_on_submit():
                user = User.create(username=form.username.data, 
                                   password=form.password.data,
                                   aws_access_key=form.access_key.data,
                                   aws_secret_key=form.secret_key.data)
                flash('User created successfully!', 'success')
                return redirect(url_for('public.login'))

    return render_template('public/register.html', form=form)
