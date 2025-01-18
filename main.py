from flask import Flask, request, jsonify, render_template_string
import sqlite3
import datetime

app = Flask(__name__)

# define html template
html = """
<!DOCTYPE html>
<html>
<head>
    <title>Work Orders</title>
</head>
<body>
    <h1>Work Orders</h1>
    <a href="/create">Create Work Order</a>
    <table border="1">
        <tr>
            <th>Work Order ID</th>
            <th>Customer</th>
            <th>Description</th>
            <th>Status</th>
            <th>Tech</th>
            <th>Delete</th>
        </tr>
        {% for workorder in workorders %}
        <tr>
            <td><a href="/edit/{{ workorder[0] }}">{{workorder[0]}}</a></td>
            <td>{{ workorder[10] }}</td>
            <td>{{ workorder[1] }}</td>
            <td>{{ workorder[2] }}</td>
            <td>{{ workorder[5] }}</td>
            <td>
                <form method="post" action="/delete/{{ workorder[0] }}">
                    <input type="submit" value="Delete">
                </form>
            </td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""


@app.route('/')
def home():
    data = get_workorders()
    return render_template_string(html, workorders=data)


def get_workorders():
    """Get all work orders"""
    conn = sqlite3.connect('okwo.db')
    cursor = conn.cursor()
    cursor.execute("SELECT w.*, c.customer_name FROM workorders w left join customers c on w.customer_code = c.customer_code")
    workorders = cursor.fetchall()
    conn.close()
    return workorders

@app.route('/create', methods=['GET', 'POST'])
def create_workorder():
    """Create a new work order"""
    if request.method == 'POST':
        workorder_description = request.form['workorder_description']
        workorder_status = request.form['workorder_status']
        workorder_priority = request.form['workorder_priority']
        workorder_due_date = (datetime.datetime.now() + datetime.timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
        workorder_assigned_to = request.form['workorder_assigned_to']
        workorder_created_by = "TIMO"
        workorder_created_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        customer_code = request.form['customer_code']
        conn = sqlite3.connect('okwo.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO workorders (workorder_description, workorder_status, workorder_priority, workorder_due_date, workorder_assigned_to, workorder_created_by, workorder_created_date, customer_code) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (workorder_description, workorder_status, workorder_priority, workorder_due_date, workorder_assigned_to, workorder_created_by, workorder_created_date, customer_code))
        conn.commit()
        conn.close()
        # return jsonify({"message": "Work order created successfully!"})
        request.form = request.form.copy()
        request.form.clear()
        # redirect to home page
        return home()
    return '''
        <form method="post">
            Work Order Description: <input type="text" name="workorder_description"><br>
            Work Order Status:
            <select name="workorder_status">
                <option value="Open" default>Open</option>
                <option value="Hold">On Hold</option>
                <option value="In Progress">In Progress</option>
                <option value="Closed">Closed</option>
            </select><br>
            Work Order Priority:
            <select name="workorder_priority">
                <option value="Low">Low</option>
                <option value="Medium" default>Medium</option>
                <option value="High">High</option>
            </select><br>
            Work Order Assigned To: 
            <select name="workorder_assigned_to">
                <option value="">Select</option>
                <option value="Steve Lukather">Steve Lukather</option>
                <option value="David Paich">David Paich</option>
                <option value="Joseph Williams">Joseph Williams</option>
                <option value="Steve Porcaro">Steve Porcaro</option>
                <option value="Bobby Kimball">Bobby Kimball</option>
            </select><br>
            Customer Code: <input type="text" name="customer_code"><br>
            <input type="submit" value="Create Work Order">
        </form>
        <a href="/">Back to Work Orders</a>
    '''

@app.route('/edit/<int:workorder_id>', methods=['GET', 'POST'])
def edit_workorder(workorder_id):
    """Edits a work order"""
    if request.method == 'POST':
        workorder_description = request.form['workorder_description']
        workorder_status = request.form['workorder_status']
        workorder_priority = request.form['workorder_priority']
        workorder_due_date = request.form['workorder_due_date']
        workorder_assigned_to = request.form['workorder_assigned_to']
        workorder_updated_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        customer_code = request.form['customer_code']
        conn = sqlite3.connect('okwo.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE workorders SET workorder_description=?, workorder_status=?, workorder_priority=?, workorder_due_date=?, workorder_assigned_to=?, workorder_updated_date=?, customer_code=? WHERE workorder_id=?', (workorder_description, workorder_status, workorder_priority, workorder_due_date, workorder_assigned_to, workorder_updated_date, customer_code, workorder_id))
        conn.commit()
        conn.close()
        return jsonify({"message": "Work order updated successfully!"})
    conn = sqlite3.connect('okwo.db')
    cursor = conn.cursor()
    cursor.execute("SELECT w.*, c.customer_code FROM workorders w left join customers c on w.customer_code = c.customer_code WHERE workorder_id=?", (workorder_id,))
    workorder = cursor.fetchone()
    conn.close()
    request.form = request.form.copy()
    request.form.clear()
    return '''
        <h1>Edit Work Order</h1>
        <form method="post">
            Work Order Description: <input type="text" name="workorder_description" value="{}"><br>
            Work Order Status:
            <select name="workorder_status">
                <option value="Open" {}>Open</option>
                <option value="Hold" {}>On Hold</option>
                <option value="In Progress" {}>In Progress</option>
                <option value="Closed" {}>Closed</option>
            </select><br>
            Work Order Priority:
            <select name="workorder_priority">
                <option value="Low" {}>Low</option>
                <option value="Medium" {}>Medium</option>
                <option value="High" {}>High</option>
            </select><br>
            Work Order Due Date: <input type="text" name="workorder_due_date" value="{}"><br>
            Work Order Assigned To: 
            <select name="workorder_assigned_to">
                <option value="">Select</option>
                <option value="Steve Lukather" {}>Steve Lukather</option>
                <option value="David Paich" {}>David Paich</option>
                <option value="Joseph Williams" {}>Joseph Williams</option>
                <option value="Steve Porcaro" {}>Steve Porcaro</option>
                <option value="Bobby Kimball" {}>Bobby Kimball</option>
            </select><br>
            Customer Code: <input type="text" name="customer_code" value="{}"><br>
            <input type="submit" value="Update Work Order">
        </form>

        <a href="/">Back to Work Orders</a>
    '''.format(
        workorder[1], 
        'selected' if workorder[2] == 'Open' else '', 
        'selected' if workorder[2] == 'Hold' else '', 
        'selected' if workorder[2] == 'In Progress' else '', 
        'selected' if workorder[2] == 'Closed' else '', 
        'selected' if workorder[3] == 'Low' else '', 
        'selected' if workorder[3] == 'Medium' else '', 
        'selected' if workorder[3] == 'High' else '', 
        workorder[4], 
        'selected' if workorder[5] == 'Steve Lukather' else '', 
        'selected' if workorder[5] == 'David Paich' else '', 
        'selected' if workorder[5] == 'Joseph Williams' else '', 
        'selected' if workorder[5] == 'Steve Porcaro' else '', 
        'selected' if workorder[5] == 'Bobby Kimball' else '', 
        workorder[10]
    )
    


@app.route('/delete/<int:workorder_id>', methods=['POST'])
def delete_workorder(workorder_id):
    """Deletes a work order"""
    conn = sqlite3.connect('okwo.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM workorders WHERE workorder_id=?', (workorder_id,))
    conn.commit()
    conn.close()
    
    # redirect to home page
    return home()

if __name__ == '__main__':
    app.run(debug=True)