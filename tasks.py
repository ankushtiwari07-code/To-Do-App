from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import task

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/')
def view_tasks():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    all_tasks = task.query.all()
    return render_template('tasks.html', tasks=all_tasks)


@tasks_bp.route('/add', methods=['POST'])
def add_task():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    title = request.form.get('title', '').strip()

    if title:
        new_task = task(title=title, status='pending')
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully', 'success')

    return redirect(url_for('tasks.view_tasks'))


@tasks_bp.route('/toggle/<int:task_id>', methods=['POST'])
def toggle_status(task_id):
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    current_task = db.session.get(task, task_id)

    if current_task:
        if current_task.status.lower() == 'pending':
            current_task.status = 'working'
        elif current_task.status.lower() == 'working':
            current_task.status = 'done'
        else:
            current_task.status = 'pending'

        db.session.commit()

    return redirect(url_for('tasks.view_tasks'))


@tasks_bp.route('/clear', methods=['POST'])
def clear_tasks():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    task.query.delete()
    db.session.commit()
    flash('All tasks cleared!', 'info')

    return redirect(url_for('tasks.view_tasks'))
