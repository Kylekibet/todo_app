from flask import Blueprint, render_template, redirect, url_for, flash, abort
from forms import AddTask, AddCategory
from flask_login import login_required, current_user
from models import Task, Category, db
from sqlalchemy import func, and_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload



pages_bp = Blueprint('pages', __name__)


@pages_bp.route('/')
def home():
    return render_template('index.html')

@pages_bp.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task():
    form = AddTask()
    if form.validate_on_submit():
        task = Task(
            title=form.task.data,
            category_id=form.category_id.data or None,
            date_due=form.date_due.data,
            user_id=current_user.id,
        )
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('pages.add_task'))
    return render_template(
        'add_task.html',
        form=form,
        form_action=url_for('pages.add_task'),)
    
@pages_bp.route('/task/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def task_edit(task_id):
    task = db.session.scalar(select(Task).where(task_id == Task.id, Task.user_id == current_user.id))
    
    if task is None:
        abort(404)
    
    form = AddTask(data={
        'task': task.title,
        'category_id': task.category_id or 0,
        'date_due': task.date_due
    })
    if form.validate_on_submit():
        task.title = form.task.data
        task.category_id = form.category_id.data or None
        task.date_due = form.date_due.data
        db.session.commit()
        return redirect(url_for('pages.view_tasks', category_id=task.category_id or 0))
    return render_template('add_task.html', form=form, page_title='Edit task', button_text='Edit task', form_action=url_for('pages.task_edit', task_id=task.id))


@pages_bp.route('/add_category', methods=['GET', 'POST'])
@login_required
def add_category():
    form = AddCategory()
    if form.validate_on_submit():
        category = Category(name=form.category.data.strip(), user_id=current_user.id)
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash('You already have a category with that name.')
        else:
            return redirect(url_for('pages.add_category'))
    return render_template('add_category.html', form=form, form_action=url_for('pages.add_category'))

@pages_bp.route('/category/edit/<int:category_id>', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    category = db.session.scalar(select(Category).where(category_id == Category.id, Category.user_id == current_user.id))
    
    if category is None:
        abort(404)
        
    form = AddCategory(data={
        'category': category.name
    })
    
    if form.validate_on_submit():
        category.name = form.category.data
        db.session.commit()
        return redirect(url_for('pages.view_categories'))
    return render_template('add_category.html', form=form, page_title='Edit category', button_text='Edit Category', form_action=url_for('pages.edit_category', category_id=category.id))

@pages_bp.route('/tasks/<int:category_id>')
@login_required
def view_tasks(category_id):
    query = db.select(Task).where(Task.user_id == current_user.id)

    if category_id == 0:
        category_name = 'Uncategorized'
        query = query.where(Task.category_id.is_(None))
    else:
        category = db.session.scalar(
            db.select(Category).where(
                Category.id == category_id,
                Category.user_id == current_user.id,
            )
        )
        if category is None:
            abort(404)
        category_name = category.name
        query = query.where(Task.category_id == category.id)

    tasks = db.session.scalars(
        query.order_by(Task.done, Task.date_due.is_(None), Task.date_due, Task.date_created.desc())
    ).all()
    return render_template('view_tasks.html', tasks=tasks, category_name=category_name)


@pages_bp.route('/categories')
@login_required
def view_categories():
    rows = db.session.execute(
        db.select(Category, func.count(Task.id))
        .outerjoin(Task, and_(Task.category_id == Category.id, Task.done.is_(False)))
        .where(Category.user_id == current_user.id)
        .group_by(Category.id)
        .order_by(Category.name)
    ).all()

    uncategorized_due = db.session.scalar(
        db.select(func.count(Task.id)).where(
            Task.user_id == current_user.id,
            Task.category_id.is_(None),
            Task.done.is_(False),
        )
    )

    return render_template('view_categories.html', rows=rows, uncategorized_due=uncategorized_due)

@pages_bp.route('/delete/category/<int:category_id>')
@login_required
def delete_category(category_id):
    category = db.session.scalar(
        select(Category).where(
            Category.id == category_id, 
            Category.user_id == current_user.id
        )
    )

    if category is None:
        abort(404)

    # Option 1: Reassign all tasks in this category to "Uncategorized" (None)
    db.session.execute(
        db.update(Task)
        .where(Task.category_id == category.id)
        .values(category_id=None)
    )

    # Now safely delete the category
    db.session.delete(category)
    db.session.commit()
    
    flash('Category deleted. Any remaining tasks were moved to Uncategorized.', 'success')
    return redirect(url_for('pages.view_categories'))

@pages_bp.route('/delete/task/<int:task_id>')
@login_required
def delete_task(task_id):
    task = db.session.scalar(select(Task).where(Task.id == task_id, Task.user_id == current_user.id))

    if task is None:
        abort(404)
    category_id = task.category_id if task.category_id is not None else 0
    
    print(f"deleteing {task} task")
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('pages.view_tasks', category_id=category_id))


        
    

