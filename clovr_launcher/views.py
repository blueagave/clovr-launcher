# coding=utf-8

from flask import render_template, flash, redirect, session, url_for, request, g, Markup
from clovr_launcher import app

@app.route('/')
@app.route('/index')
def index():
    return render_template('start_vm.html')

@app.route('/start_vm')
def start_vm():
    return render_template('start_vm.html')

@app.route('/manage_vms')
def manage_vms():
    return render_template('manage_vms.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    return render_template('login.html')




