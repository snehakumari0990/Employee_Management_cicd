from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Employee

main = Blueprint('main', __name__)

@main.route('/')
def index():
    employees = Employee.query.order_by(Employee.name).all()
    return render_template('index.html', employees=employees)

@main.route('/search')
def search():
    query = request.args.get('query', '')
    if query:
        employees = Employee.query.filter(
            Employee.name.ilike(f'%{query}%') |
            Employee.department.ilike(f'%{query}%')
        ).all()
    else:
        employees = Employee.query.all()
    return render_template('index.html', employees=employees, search_query=query)

@main.route('/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        department = request.form['department']
        position = request.form['position']
        salary = request.form['salary']

        existing = Employee.query.filter_by(email=email).first()
        if existing:
            flash('An employee with this email already exists.', 'danger')
            return render_template('add_employee.html')

        new_employee = Employee(
            name=name,
            email=email,
            department=department,
            position=position,
            salary=float(salary)
        )
        db.session.add(new_employee)
        db.session.commit()
        flash(f'✅ Employee {name} added successfully!', 'success')
        return redirect(url_for('main.index'))

    return render_template('add_employee.html')

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    employee = Employee.query.get_or_404(id)

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        
        existing = Employee.query.filter(
            Employee.email == email,
            Employee.id != id
        ).first()
        
        if existing:
            flash('An employee with this email already exists.', 'danger')
            return render_template('edit_employee.html', employee=employee)

        employee.name = name
        employee.email = email
        employee.department = request.form['department']
        employee.position = request.form['position']
        employee.salary = float(request.form['salary'])
        db.session.commit()
        flash(f'✅ Employee {employee.name} updated successfully!', 'success')
        return redirect(url_for('main.index'))

    return render_template('edit_employee.html', employee=employee)

@main.route('/delete/<int:id>', methods=['POST'])
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    name = employee.name
    db.session.delete(employee)
    db.session.commit()
    flash(f'ℹ️ Employee {name} has been deleted.', 'info')
    return redirect(url_for('main.index'))