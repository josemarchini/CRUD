from flask import Flask, render_template, request, redirect, url_for, session, flash , jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin


#app = Flask(__name__)
app = Flask(__name__, static_folder='templates')

#voglio permettere a CORS tutti le richieste get, delete, put, post
cors=CORS(app) #resources={r"/api/*": {"origins": "http://localhost:5000"}}
app.config['CORS_HEADERS'] = 'Content-Type'
#app.config['CORS_HEADERS'] = 'Access-Control-Allow-Origin'
#app.config['CORS_METHODS'] = 'GET, POST, PUT, DELETE, OPTIONS'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Exitosox100pre'
app.config['MYSQL_DB'] = 'happiness'
mysql = MySQL(app)


@app.route('/api/customers/<int:id>', methods=['GET'])
@cross_origin()
def getCustomerById(id):
    cur=mysql.connection.cursor()
    sql="SELECT c.Country, c.Rank, c.Happiness_score, c.Year_score, p.Parameters, l.Value_parameters FROM countries c JOIN links l ON c.id_country = l.id_country JOIN parameters p ON l.id_parameters = p.id_parameters WHERE id = " + str(id) + ""
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
            'Parameters': customer[5],
            'Value_parameters': customer[6],
            
        }
    return jsonify(customer)


@app.route('/api/customers', methods=['GET'])
@cross_origin()
def getAllCustomers():
    cur=mysql.connection.cursor()
    sql="select Country, countries.Rank, Happiness_score, Year_score, Parameters, Value_parameters from happiness.countries left join happiness.links on countries.id_country=links.id_country left join happiness.parameters on links.id_parameters=parameters.id_parameters" #ORDER BY Happiness_score DESC
    cur.execute(sql)
    data=cur.fetchall()
    result = []
    for customer in data:
        customer = {
            #'Id': customer[0],
            'Country': customer[0],
            'Rank': customer[1],
            'Happiness_score': customer[2],
            'Year_score': customer[3],
            'Parameters': customer[4],
            'Value_parameters': customer[5],
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
    #sql="INSERT INTO countries_parameters (Country, Rank, Happiness_score, Year_score, GDP_per_capita, Social_support, Life_expectancy, Freedom, Generosity, Perceptions_of_corruption, Dystopia) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    #dati=(request.json['Country'], request.json['Rank'], request.json['Happiness_score'], request.json['Year_score'], request.json['GDP_per_capita'], request.json['Social_support'], request.json['Life_expectancy'], request.json['Freedom'], request.json['Generosity'], request.json['Perceptions_of_corruption'], request.json['Dystopia'])
    sql="INSERT INTO customers (Country) VALUES ('%s')"
    dati=(request.json['Country'])
    cur.execute(sql, dati)
    mysql.connection.commit()

    return 'Save Customer'


@app.route('/api/customers', methods=['GET'])
@cross_origin()
def updateCustomer():
    cur=mysql.connection.cursor()
    #update customer
    sql="UPDATE customers SET Country = %s, Rank = %s, Happiness_score = %s, Year_score = %s, GDP_per_capita = %s, Social_support = %s, Life_expectancy = %s, Freedom = %s, Generosity = %s, Perceptions_of_corruption = %s, Dystopia = %s WHERE id = " + str(request.json['id']) + ""
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




'''@app.route('/', methods=['GET'])
def home():
    titolo = '<h2>PROGETTO HAPPINESS</h2>'
    richiesta1 = '<form action="/database" method="GET">' \
                 '<a href="/database"><h3>Visualizza tutto il database</h3></a></form>'
    richiesta2 ='<form action = "/anno" method= "POST">Seleziona l\'anno che ti interessa tra' \
                ' 2017,2018,2019,2020,2021,2022: <input name="texta"> <input type="submit" value="Invio"></form>'
    return titolo + '<br>'+'<br>' + richiesta1 + '<br>' + richiesta2'''

@app.route('/risultato', methods=['GET'])
def elenco():
    cur=mysql.connection.cursor()
    #se apro la pagina elenco, apro il DB
    perfile= 'C://Users/alonso/Documents/CursoGeneration/ProggettoFinale/CRUD/templates/prova.html'
    file=open(perfile, 'w')
    intestazione = '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n<title>HAPPINESS SCORE</title>\n</head>\n' \
                   '<body bgcolor="#2b6e8d">ELENCO PAESI, GDP PER CAPITA E ANNO:<ol>'
    finale = '</ol></body></html>'
    file.write(intestazione)
    cur.execute("SELECT Country,Value_parameters,Year_score FROM parameters INNER JOIN links ON "
                     "parameters.id_parameters=links.id_parameters INNER JOIN countries ON "
                     "links.id_country=countries.id_country WHERE parameters.Parameters='GDP_per_capita';")
    myresult = cur.fetchall()
    for i in myresult:
        file.write('<li>'+str(i[0])+'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'+str(i[1])+'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'+str(i[2])+'</li>')
    file.write(finale)
    file.close()
    return render_template('prova.html')









#name == main
if __name__ == '__main__':
    app.run(None, 5000, True)