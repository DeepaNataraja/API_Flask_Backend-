from flask import Flask , jsonify , request 
import psycopg2
 
app = Flask(__name__)
   
user = 'postgres'
password = 'postgres'
host = 'localhost'
port = 5432
database = 'HR'   
 
print(host, database, user, password, port)

def get_db_connection() :
    conn = psycopg2.connect(
        database="HR", user='postgres',
        password='postgres', host='localhost', port='5432')
    return conn
 
# end point for GET items 
@app.route("/p.items",methods=['GET'])
def get_items():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        print("api-functioncalled")

        cursor.execute('SELECT d.department_id as d_department_id, d.department_name, d.location_id, e.employee_id, e.first_name, e.last_name, e.email, e.phone_number, e.hire_date, e.job_id, e.salary, e.manager_id, e.department_id FROM employees e INNER JOIN departments d ON e.department_id = d.department_id INNER JOIN locations l ON d.location_id = l.location_id INNER JOIN countries c ON l.country_id = c.country_id INNER JOIN regions r ON c.region_id = r.region_id INNER JOIN jobs j ON e.job_id=j.job_id INNER JOIN dependents de ON e.employee_id=de.employee_id')
        rows = cursor.fetchall()

        result = []
        for row in rows:
            d = {}
            for i, col in enumerate(cursor.description):
                d[col[0]] = row[i]
            result.append(d)
            print(result)
        
        return jsonify(result)
            
    except Exception as e:
        result = jsonify("exception error : {e}")
        print("exception error",e)

    finally:    
        cursor.close()
        conn.close()

# end point for post item  
@app.route("/p.item/<employee_id>",methods=['GET'])
def get_single_item(employee_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT d.department_id AS d_department_id, d.department_name, d.location_id, e.employee_id, e.first_name, e.last_name, e.email, e.phone_number, e.hire_date, e.job_id, e.salary, e.manager_id, e.department_id FROM employees e INNER JOIN departments d ON e.department_id = d.department_id INNER JOIN locations l ON d.location_id = l.location_id INNER JOIN countries c ON l.country_id = c.country_id INNER JOIN regions r ON c.region_id = r.region_id INNER JOIN jobs j ON e.job_id = j.job_id WHERE e.employee_id = %s", (employee_id,))
        row = cursor.fetchone()
        
        if row is None:
            return jsonify({'error': 'Employee not found'})
        
        result = {}
        for i, col in enumerate(cursor.description):
            result[col[0]] = row[i]
        
        return jsonify(result)  
    
    except Exception as e:
        result = {'message': str(e)}
        return jsonify(result)
    
    finally:    
        cursor.close()
        conn.close()
 
# end point for delete item

@app.route('/p.del-item/<d_department_id>/<employee_id>',methods=['DELETE'])

def delete_employee(d_department_id, employee_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        sql1 = "DELETE FROM departments WHERE department_id = %s"
        sql2 = "DELETE FROM employees WHERE employee_id = %s"

        print("before execute")
        cursor.execute(sql1, (d_department_id,) )
        print("before employee execute ")
        cursor.execute(sql2,(employee_id,))

        print("after execution")
        resp = jsonify({"message": "Item deleted successfully"})
        return resp
     
    except Exception as e:
        resp = jsonify("exception error : {e}")
        print("exception error",e)
        return resp 
    finally:
        cursor.close()
        conn.close()

#endpoint for post  

@app.route('/p.post-item', methods=['POST'])
def post_item():
    try:
        new_user = request.get_json()
        print(new_user)
        print("api-functioncalled")

        d_department_id = new_user['d_department_id']
        department_name = new_user['department_name']
        location_id = new_user['location_id']
        employee_id = new_user['employee_id']
        first_name = new_user['first_name']
        last_name = new_user['last_name']
        email = new_user['email']
        phone_number = new_user['phone_number']
        hire_date = new_user['hire_date']
        job_id = new_user['job_id']
        salary = new_user['salary']
        manager_id = new_user['manager_id']
        department_id = new_user['department_id']

        print("before validation")
        
        if employee_exists(employee_id):
            print("employee validation")
            return jsonify({"message": "Employee ID already exists"}), 400
        
        if department_exists(department_id):
            print("department validation")
            return jsonify({"message": "Department ID already exists"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        
        sql1 = "INSERT INTO departments(department_id, department_name, location_id ) VALUES (%s, %s, %s) RETURNING department_id"
        sql2 = "INSERT INTO employees(employee_id, first_name, last_name, email ,phone_number ,hire_date, job_id, salary, manager_id,department_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        
        print("before execute")
        cursor.execute(sql1, (d_department_id, department_name, location_id,))
        dep_id = cursor.fetchone()[0] # retrieve the returned department_id
        print("before employee execute ")
        cursor.execute(sql2,(employee_id, first_name, last_name, email ,phone_number ,hire_date, job_id, salary, manager_id,dep_id,) )
        conn.commit() # commit the transaction
        
        print("after execution")

        resp = jsonify("Item added successfully!")
        return resp
    except Exception as e:
        resp = jsonify("exception error : {e}")
        print("exception error",e)
        return resp
    finally:
        cursor.close()
        conn.close()
 
def employee_exists(employee_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM employees WHERE employee_id = %s", (employee_id,))
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count > 0

def department_exists(department_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM departments WHERE department_id = %s", (department_id,))
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count > 0
 
#end point for update 

@app.route('/p.put-item/<d_department_id>/<employee_id>',methods=['PUT'])
def put_item(d_department_id,employee_id):
    try:
        new_user = request.get_json()
        print(new_user)
        print("api-functioncalled")

        d_department_id = new_user['d_department_id']
        department_name = new_user['department_name']
        location_id = new_user['location_id']
        employee_id = new_user['employee_id']
        first_name = new_user['first_name']
        last_name = new_user['last_name']
        email = new_user['email']
        phone_number = new_user['phone_number']
        hire_date = new_user['hire_date']
        job_id = new_user['job_id']
        salary = new_user['salary']
        manager_id = new_user['manager_id']
        department_id = new_user['department_id']
        print("before validation")

        conn = get_db_connection()
        cursor = conn.cursor()

        sql1 = ("UPDATE departments SET department_id=%s,department_name=%s, location_id=%s WHERE department_id=%s RETURNING department_id ")
        sql2 = ("UPDATE employees SET employee_id=%s,first_name=%s,last_name=%s,email=%s,phone_number = %s,hire_date=%s,job_id=%s,salary=%s,manager_id=%s,department_id=%s WHERE employee_id=%s")

        print("before execute")
        cursor.execute(sql1, (d_department_id,department_name, location_id,d_department_id,))
        dept_id = cursor.fetchone()[0]
        print("before employee execute ")
        cursor.execute(sql2,(employee_id, first_name, last_name, email ,phone_number ,hire_date, job_id, salary, manager_id,dept_id,employee_id)) 
        conn.commit()
        print("after execution")

        resp = jsonify("Item updated successfully!")
        return resp
    except Exception as e:
        resp = jsonify("exception error : {e}")
        print("exception error",e)
        return resp
    finally :
        cursor.close()
        conn.close()


if __name__ == "__main__":
    app.run()


 