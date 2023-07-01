from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:63342"}})
import psycopg2


# Configure database connection
connection = psycopg2.connect(
    host="localhost",
    port="5432",
    database="job_database",
    user="postgres",
    password="admin"
)


@app.route('/search', methods=['GET'])
@cross_origin()
def search():
    # Retrieve the query parameters from the request
    employer = request.args.get('employer').lower()
    year = request.args.get('year')
    job_title = request.args.get('jobTitle').lower()
    state = request.args.get('state').lower()
    # city = request.args.get('city').lower()

    # Perform database query and retrieve results
    cursor = connection.cursor()
    cursor.execute(f""" select 
employer_name,
job_title,
pw_wage_level as level,
wage_rate_of_pay_from as salary,
pw_unit_of_pay as unit,
lower(worksite_city) as City,
worksite_state as State

from lca where
 lower(job_title) like '%{job_title}%'  
 and lower(employer_name) like '%{employer}%'  
 --and lower(worksite_state) like '%{state}%'
 order by wage_rate_of_pay_from desc """)
    connection.commit()
    filtered_jobs = cursor.fetchall()
    return jsonify(filtered_jobs)

@app.route('/analytics', methods=['GET'])
@cross_origin()
def analytics():
    # Retrieve the query parameters from the request
    employer = request.args.get('employer').lower()
    year = request.args.get('year')
    job_title = request.args.get('jobTitle').lower()
    state = request.args.get('state').lower()
    # city = request.args.get('city').lower()

    # Perform database query and retrieve results
    cursor = connection.cursor()
    cursor.execute(f""" select 
cast(replace(substring(wage_rate_of_pay_from,2,12),',','' ) as decimal) as salary
from lca where
 lower(job_title) like '%{job_title}%'  
 and lower(employer_name) like '%{employer}%'  
 --and lower(worksite_state) like '%{state}%'
 order by wage_rate_of_pay_from desc """)
    connection.commit()
    salary = cursor.fetchall()
    salary = [float(item[0]) for item in salary]

    return jsonify(salary)


if __name__ == '__main__':
    app.run()
