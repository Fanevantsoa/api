from flask import Flask, jsonify, request
import mysql.connector, json
import pymysql

from pymysql.constants import CLIENT

app = Flask(__name__)

# Fonction pour établir une connexion à la base de données
def connect_to_database():
    return mysql.connector.connect(
        host="sql11.freesqldatabase.com",
        user="sql11698063",
        passwd="k7uB246Nhw",
        database="sql11698063"
    )

def get_data_db(sql_query, value=""):
    try:
        conn = connect_to_database()        #Connection to the mysql database
        curseur = conn.cursor()             # Création du curseur
        
        if value == "":
            curseur.execute(sql_query)
        else:
            curseur.execute(sql_query, value)

        colonnes = [description[0] for description in curseur.description]  # Récupération des noms des colonnes

        resultats = curseur.fetchall()  # Récupération des résultats

        # Convertir les résultats en une liste de dictionnaires
        etudiants = []
        for resultat in resultats:
            etudiant = dict(zip(colonnes, resultat))
            etudiants.append(etudiant)

        # Fermeture du curseur et de la connexion à la base de données
        curseur.close()
        conn.close()

        return jsonify(etudiants)
    except Exception as e:
        return jsonify(f"{e}")


@app.route('/student', methods=['GET', 'POST'])
def all_students():
    if request.method == 'GET':
        try:
            requete = "SELECT * FROM students"  # Exécution d'une requête SELECT pour récupérer les données des étudiants
            return get_data_db(requete)
        except Exception as e:
            return jsonify(), 500

    elif request.method == 'POST':
        try:
            # Récupérer le contenu JSON de la requête
            user_data = request.json

            #Connection to the mysql database
            conn = connect_to_database()

            # Assuming `conn` is your database connection object
            curseur = conn.cursor()

            query1 = "INSERT INTO students (id, lastname, firstname, classe) VALUES (%s, %s, %s, %s)"
            values1 = (user_data["id"],  user_data["lastname"], user_data["firstname"], user_data["classe"])
            curseur.execute(query1, values1)
            conn.commit()

            # Fermeture du curseur et de la connexion à la base de données
            curseur.close()
            conn.close()

            return get_data_db("SELECT * FROM students WHERE id=%s", (user_data["id"],))

        except Exception as e:
            return jsonify(), 500

    else:
        'Nothing Found', 404

@app.route('/student/<student_id>', methods=['GET', 'PUT', 'DELETE'])
def one_student(student_id):
    if request.method == 'GET':
        try:
            requete = "SELECT * FROM students WHERE id=%s"
            return get_data_db(requete, (student_id,))
        except Exception as e:
            return jsonify(), 500
        
    elif request.method == 'PUT':
        try:
            # Récupérer le contenu JSON de la requête
            user_data = request.json

            #Connection to the mysql database
            conn = connect_to_database()

            # Assuming `conn` is your database connection object
            curseur = conn.cursor()

            query1 = '''UPDATE students SET firstname=%s, lastname=%s, classe=%s WHERE id=%s'''
            values1 = (user_data["firstname"], user_data["lastname"], user_data["classe"], user_data["id"])
            curseur.execute(query1, values1)
            conn.commit()

            # Fermeture du curseur et de la connexion à la base de données
            curseur.close()
            conn.close()

            return get_data_db("SELECT * FROM students WHERE id=%s", (user_data["id"],))

        except Exception as e:
            return jsonify(), 500

    elif request.method == 'DELETE':
        try:
            # Connection to the mysql database
            conn = connect_to_database()

            # Création du curseur
            curseur = conn.cursor()

            requete = "DELETE FROM students WHERE id=%s"
            curseur.execute(requete, (student_id,))

            # Commit the transaction
            conn.commit()

            # Fermeture du curseur et de la connexion à la base de données
            curseur.close()
            conn.close()

            return get_data_db("SELECT * FROM students WHERE id=%s", (student_id,))

        except Exception as e:
            # Rollback in case there is any error
            conn.rollback()
            return jsonify(), 500

    else:
        'Nothing Found', 404

@app.route('/event', methods=['GET', 'POST'])
def all_event():
    if request.method == 'GET':
        try:
            requete = "SELECT * FROM event_presence"  # Exécution d'une requête SELECT pour récupérer les données des étudiants
            return get_data_db(requete)
        except Exception as e:
            return jsonify(), 500

    elif request.method == 'POST':
        try:
            # Récupérer le contenu JSON de la requête
            user_data = request.json

            #Connection to the mysql database
            conn = connect_to_database()

            # Assuming `conn` is your database connection object
            curseur = conn.cursor()

            query2 = "INSERT INTO event_presence (id, payment, presence) VALUES (%s, %s, %s)"
            values2 = (user_data["id"],  user_data["payment"], user_data["presence"])
            curseur.execute(query2, values2)
            conn.commit()

            # Fermeture du curseur et de la connexion à la base de données
            curseur.close()
            conn.close()

            return get_data_db("SELECT * FROM event_presence WHERE id=%s", (user_data["id"],))

        except Exception as e:
            return jsonify(), 500
    else:
        'Nothing Found', 404

@app.route('/event/<student_id>', methods=['GET', 'PUT', 'DELETE'])
def one_event(student_id):
    if request.method == 'GET':
        try:
            requete = "SELECT * FROM event_presence WHERE id=%s"
            return get_data_db(requete, (student_id,))
        except Exception as e:
            return jsonify(), 500

    elif request.method == 'PUT':
        try:
            # Récupérer le contenu JSON de la requête
            user_data = request.json

            #Connection to the mysql database
            conn = connect_to_database()

            # Assuming `conn` is your database connection object
            curseur = conn.cursor()

            query2 = '''UPDATE event_presence SET presence=%s, payment=%s WHERE id=%s'''
            values2 = (user_data["presence"], user_data["payment"], user_data["id"])
            curseur.execute(query2, values2)
            conn.commit()

            # Fermeture du curseur et de la connexion à la base de données
            curseur.close()
            conn.close()

            return get_data_db("SELECT * FROM event_presence WHERE id=%s", (user_data["id"],))

        except Exception as e:
            return jsonify(), 500

    elif request.method == 'DELETE':
        try:
            # Connection to the mysql database
            conn = connect_to_database()

            # Création du curseur
            curseur = conn.cursor()

            requete = "DELETE FROM event_presence WHERE id=%s"
            curseur.execute(requete, (student_id,))

            # Commit the transaction
            conn.commit()

            # Fermeture du curseur et de la connexion à la base de données
            curseur.close()
            conn.close()

            return get_data_db("SELECT * FROM event_presence WHERE id=%s", (student_id,))

        except Exception as e:
            # Rollback in case there is any error
            conn.rollback()
            return jsonify(), 500

    else:
        'Nothing Found', 404

if __name__ == '__main__':
    app.run(debug=True)
