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


@app.route('/risultato', methods=['GET'])
def elenco():
    cur=mysql.connection.cursor()
    #se apro la pagina elenco, apro il DB
    perfile= 'C://Users/alonso/Documents/CursoGeneration/ProggettoFinale/CRUD/templates/prova.html'
    file=open(perfile, 'w')
    intestazione = '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n<title>HAPPINESS SCORE</title>\n</head>\n' \
                   '<style> h1 {text-align: center;} </style> <body ali bgcolor="#F3F768"> <h1>ELENCO PAESI, GDP PER CAPITA E ANNO: </h1> <ol>'
    finale = '</ol></body></html>'
    file.write(intestazione)
    cur.execute("SELECT Country,Value_parameters,Year_score FROM parameters INNER JOIN links ON "
                     "parameters.id_parameters=links.id_parameters INNER JOIN countries ON "
                     "links.id_country=countries.id_country WHERE parameters.Parameters='GDP_per_capita';")
    myresult = cur.fetchall()
    for i in myresult:
        file.write('<h4> <li>'+str(i[0])+'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'+str(i[1])+'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'+str(i[2])+'</li> </h4>')
    file.write(finale)
    file.close()
    return render_template('prova.html')


@app.route('/risultato1', methods=['GET'])
def elencoHP():
    cur=mysql.connection.cursor()
    #se apro la pagina elenco, apro il DB
    perfile= 'C://Users/alonso/Documents/CursoGeneration/ProggettoFinale/CRUD/templates/prova1.html'
    file=open(perfile, 'w')
    intestazione = '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n<title>HAPPINESS SCORE</title>\n</head>\n' \
                   '<style> h1 {text-align: center;} </style> <body bgcolor="#F3F768"> <h1> MEDIA DEL HAPPINESS_SCORE RAGGRUPPATO PER PAESE: </h1><ol>'
    finale = '</ol></body></html>'
    file.write(intestazione)
    cur.execute("select Country, avg(countries.Happiness_score) as Media_Happiness_score from happiness.countries group by Country;")
    myresult = cur.fetchall()
    for i in myresult:
        file.write('<h4> <li>'+str(i[0])+'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'+str(i[1])+'</li> </h4>')
    file.write(finale)
    file.close()
    return render_template('prova1.html')

@app.route('/risultato2', methods=['GET'])
def elencoHPpaesi():
    cur=mysql.connection.cursor()
    #se apro la pagina elenco, apro il DB
    perfile= 'C://Users/alonso/Documents/CursoGeneration/ProggettoFinale/CRUD/templates/prova2.html'
    file=open(perfile, 'w')
    intestazione = '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n<title>HAPPINESS SCORE</title>\n</head>\n' \
                   '<style> h1 {text-align: center;} </style> <body bgcolor="#F3F768"> <h1> MEDIA DEL HAPPINESS_SCORE RAGGRUPPATO PER ITALIA, FILIPPINE, PERU, ALBANIA, UCRAINA </h1>'
    finale = '</body></html>'
    file.write(intestazione)
    cur.execute("select Country, avg(countries.Happiness_score) as Media_Happiness_score from happiness.countries where Country like 'Italy' or Country like 'Peru' or Country like 'Albania' or Country like 'Philippines' or Country like 'Ukraine' group by Country order by Media_Happiness_score desc;")
    myresult = cur.fetchall()
    for i in myresult:
        file.write('<br><br><br><center><h4><li>'+str(i[0])+'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'+str(i[1])+'</li> </h4></center>')
    file.write(finale)
    file.close()
    return render_template('prova2.html')



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
    app.run(None, 5000, True)