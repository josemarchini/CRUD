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
app.config['MYSQL_DB'] = 'progetto_happiness'
mysql = MySQL(app)


@app.route('/api/customers/<int:id>', methods=['GET'])
@cross_origin()
def getCustomerById(id):
    cur=mysql.connection.cursor()
    sql="SELECT * FROM countries_parameters WHERE id = " + str(id) + ""
    cur.execute(sql)
    data=cur.fetchall()
    customer={}
    for customer in data:
        customer = {
            'Id': customer[0],
            'Country': customer[1],
            'Rank': customer[2],
            'Happiness_score': customer[3],
            'Year_score': customer[4],
            'GDP_per_capita': customer[5],
            'Social_support': customer[6],
            'Life_expectancy': customer[7],
            'Freedom': customer[8],
            'Generosity': customer[9],
            'Perceptions_of_corruption': customer[10],
            'Dystopia': customer[11]
        }
    return jsonify(customer)


@app.route('/api/customers', methods=['GET'])
@cross_origin()
def getAllCustomers():
    cur=mysql.connection.cursor()
    sql="SELECT * FROM countries_parameters" #ORDER BY Happiness_score DESC
    cur.execute(sql)
    data=cur.fetchall()
    result = []
    for customer in data:
        customer = {
            'Id': customer[0],
            'Country': customer[1],
            'Rank': customer[2],
            'Happiness_score': customer[3],
            'Year_score': customer[4],
            'GDP_per_capita': customer[5],
            'Social_support': customer[6],
            'Life_expectancy': customer[7],
            'Freedom': customer[8],
            'Generosity': customer[9],
            'Perceptions_of_corruption': customer[10],
            'Dystopia': customer[11]
        }
        result.append(customer)
    return jsonify(result)



@app.route('/api/customers/<int:id>', methods=['DELETE'])
@cross_origin()
def removeCustomer(id):
    #delete customer 2
    cur=mysql.connection.cursor()
    sql="DELETE FROM countries_parameters WHERE id = " + str(id) + ""
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
    sql="INSERT INTO countries_parameters (Country, Rank, Happiness_score, Year_score, GDP_per_capita, Social_support, Life_expectancy, Freedom, Generosity, Perceptions_of_corruption, Dystopia) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    dati=(request.json['Country'], request.json['Rank'], request.json['Happiness_score'], request.json['Year_score'], request.json['GDP_per_capita'], request.json['Social_support'], request.json['Life_expectancy'], request.json['Freedom'], request.json['Generosity'], request.json['Perceptions_of_corruption'], request.json['Dystopia'])
    cur.execute(sql, dati)
    mysql.connection.commit()

    return 'Save Customer'


@app.route('/api/customers', methods=['PUT'])
@cross_origin()
def updateCustomer():
    cur=mysql.connection.cursor()
    #update customer
    sql="UPDATE countries_parameters SET Country = %s, Rank = %s, Happiness_score = %s, Year_score = %s, GDP_per_capita = %s, Social_support = %s, Life_expectancy = %s, Freedom = %s, Generosity = %s, Perceptions_of_corruption = %s, Dystopia = %s WHERE id = " + str(request.json['id']) + ""
    dati=(request.json['Country'], request.json['Rank'], request.json['Happiness_score'], request.json['Year_score'], request.json['GDP_per_capita'], request.json['Social_support'], request.json['Life_expectancy'], request.json['Freedom'], request.json['Generosity'], request.json['Perceptions_of_corruption'], request.json['Dystopia'])
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