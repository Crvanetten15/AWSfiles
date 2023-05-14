import json
import mysql.connector

mydb = mysql.connector.connect(
    host="seniordesign.c4wzumehck9a.us-east-2.rds.amazonaws.com",
    user="admin",
    password="password",
    database="disease_data"
)

mycursor = mydb.cursor()

# Specific Selection Statements for our SQL Query


def singularSelect(table):
    mycursor.execute(f"SELECT * FROM {table};")


def yearWeek(table, year, week):
    mycursor.execute(
        f"SELECT * FROM {table} WHERE year = {year} and week = {week};")


def yearDisease(table, year, disease):
    mycursor.execute(
        f"SELECT * FROM {table} WHERE year = {year} and disease = '{disease}';")


def diseaseStateYear(table, disease, state, year):
    mycursor.execute(
        f"SELECT * FROM {table} WHERE disease_name = '{disease}' and state = '{state}' and year = {year};")


def diseaseStateWeek(table, disease, year, week):
    mycursor.execute(
        f"SELECT * FROM {table} WHERE disease_name = '{disease}' and year = {year} and week = {week};")


# Lambda function handlers for our API gateway


def lambda_handler(event, context):
    """
    This function creates a new RDS database table and writes records to it
    """
    if event["httpMethod"] == "OPTIONS":
        # CORS preflight request
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "POST"
            },
            "body": ""
        }
    if event["httpMethod"] == "GET":
        # CORS preflight request
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "POST"
            },
            "body": json.dumps({"error": "query_data parameter is missing"})
        }
    if event["httpMethod"] == "POST":
        body = json.loads(event["body"])
        if "query_data" not in body:
            response = {
                "statusCode": 400,
                "headers": {
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"error": "query_data parameter is missing"})
            }
        else:
            table = body["query_data"]["table"]
            disease = body["query_data"]["disease"]
            year = body["query_data"]["year"]
            week = body["query_data"]["week"]
            state = body["query_data"]["state"]
            funct = body["function"]["number"]

            if funct == 1:
                singularSelect(table)
            elif funct == 2:
                yearWeek(table, year, week)
            elif funct == 3:
                yearDisease(table, year, disease)
            elif funct == 4:
                diseaseStateYear(table, disease, state, year)
            elif funct == 5:
                diseaseStateWeek(table, disease, year, week)

            myresult = mycursor.fetchall()
            response = {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps(myresult)
            }
    else:
        response = {
            "statusCode": 405,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Allow": "POST, OPTIONS"
            },
            "body": json.dumps({"error": "Method not allowed"})
        }

    return response
