from flask import Flask, render_template, request, redirect, url_for, session, flash , jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin


#app = Flask(__name__)
app = Flask(__name__, static_folder='templates')

cors=CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Exitosox100pre'
app.config['MYSQL_DB'] = 'pagepersonal'
mysql = MySQL(app)


@app.route('/api/customers/<int:id>', methods=['GET'])
@cross_origin()
def getCustomerById(id):
    cur=mysql.connection.cursor()
    sql="SELECT id, name, lastname, email, phone, address FROM customers WHERE id = " + str(id) + ""
    cur.execute(sql)
    data=cur.fetchall()
    customer={}
    for customer in data:
        customer = {
            'id': customer[0],
            'name': customer[1],
            'lastname': customer[2],
            'email': customer[3],
            'phone': customer[4],
            'address': customer[5]
        }
    return jsonify(customer)


@app.route('/api/customers', methods=['GET'])
@cross_origin()
def getAllCustomers():
    cur=mysql.connection.cursor()
    sql="SELECT id, name, lastname, email, phone, address FROM customers"
    cur.execute(sql)
    data=cur.fetchall()
    result = []
    for customer in data:
        customer = {
            'id': customer[0],
            'name': customer[1],
            'lastname': customer[2],
            'email': customer[3],
            'phone': customer[4],
            'address': customer[5]
        }
        result.append(customer)
    return jsonify(result)



@app.route('/api/customers/<int:id>', methods=['DELETE'])
@cross_origin()
def removeCustomer(id):
    #delete customer 2
    cur=mysql.connection.cursor()
    sql="DELETE FROM customers WHERE id = " + str(id) + ""
    cur.execute(sql)
    mysql.connection.commit()

    return 'Remove Customer'


@app.route('/api/customers', methods=['POST'])
@cross_origin()
def createCustomer():
    if 'id' in request.json:
        updateCustomer()
    else:
        saveCustomer()
    
    return 'ok'


def saveCustomer():
    cur=mysql.connection.cursor()
    sql="INSERT INTO customers (name, lastname, email, phone, address) VALUES (%s, %s, %s, %s, %s)"
    dati=(request.json['name'], request.json['lastname'], request.json['email'], request.json['phone'], request.json['address'])
    cur.execute(sql, dati)
    mysql.connection.commit()

    return 'Save Customer'


@app.route('/api/customers', methods=['PUT'])
@cross_origin()
def updateCustomer():
    cur=mysql.connection.cursor()
    #update customer
    sql="UPDATE customers SET name = %s, lastname = %s, email = %s, phone = %s, address = %s WHERE id = %s"
    dati=(request.json['name'], request.json['lastname'], request.json['email'], request.json['phone'], request.json['address'], request.json['id'])
    cur.execute(sql, dati)
    mysql.connection.commit()

    return 'Save Customer'




@app.route('/')
@cross_origin()
def index():
    return render_template('index.html')


#voglio mostrare tutti i file che sono nella cartella templates 
@app.route('/<path:path>')
@cross_origin()
def publicFiles(path):
    return app.send_static_file(path)





#name == main
if __name__ == '__main__':
    app.run(None, 3000, True)