from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import yagmail
import mysql.connector
import secrets
import os
from urllib.parse import urlencode

app = Flask(__name__)
CORS(app)

app.secret_key = 'inderkiran@24'

# MySQL database configuration
DB_HOST = 'sql6.freesqldatabase.com'
DB_NAME = 'sql6690830'
DB_USER = 'sql6690830'
DB_PASSWORD = 'elmCpSuTy2'

# Connect to the MySQL database
conn = mysql.connector.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
cursor = conn.cursor()

# Create the registrations table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS BGMIregistrations (
        id INT AUTO_INCREMENT PRIMARY KEY,
        team_name VARCHAR(255),
        college_name VARCHAR(255),
        leader_name VARCHAR(255),
        leader_ign VARCHAR(255),
        leader_discord_tag VARCHAR(255),
        leader_rank VARCHAR(255),
        leader_contact VARCHAR(255),
        leader_email VARCHAR(255),
        p2_name VARCHAR(255),
        p2_ign VARCHAR(255),
        p2_discord_tag VARCHAR(255),
        p2_rank VARCHAR(255),
        p2_contact VARCHAR(255),
        p2_email VARCHAR(255),
        p3_name VARCHAR(255),
        p3_ign VARCHAR(255),
        p3_discord_tag VARCHAR(255),
        p3_rank VARCHAR(255),
        p3_contact VARCHAR(255),
        p3_email VARCHAR(255),
        p4_name VARCHAR(255),
        p4_ign VARCHAR(255),
        p4_discord_tag VARCHAR(255),
        p4_rank VARCHAR(255),
        p4_contact VARCHAR(255),
        p4_email VARCHAR(255)
    )
''')
conn.commit()

# Email configuration
sender_email = 'hackoverflow@cumail.in'
app_password = 'lgde lflp hmgu krrd'

email_tokens = {}


def generate_token():
    return secrets.token_hex(16)


def generate_auth_link(token, data):
    auth_link = f'https://bgmiregistration.vercel.app/verify/{token}?'
    auth_link += urlencode(data)
    return auth_link


def check_duplicate(data):
    # Check for duplicates in the MySQL database across all fields
    cursor.execute("SELECT * FROM BGMIregistrations WHERE leader_ign = %s OR leader_discord_tag = %s OR leader_email = %s OR leader_contact = %s OR team_name = %s OR p2_ign = %s OR p2_discord_tag = %s OR p2_email = %s OR p2_contact = %s OR p2_name = %s OR p3_ign = %s OR p3_discord_tag = %s OR p3_email = %s OR p3_contact = %s OR p3_name = %s OR p4_ign = %s OR p4_discord_tag = %s OR p4_email = %s OR p4_contact = %s OR p4_name = %s",
                   (data['leader_ign'], data['leader_discord_tag'], data['leader_email'], data['leader_contact'], data['team_name'], data['p2_ign'], data['p2_discord_tag'], data['p2_email'], data['p2_contact'], data['p2_name'], data['p3_ign'], data['p3_discord_tag'], data['p3_email'], data['p3_contact'], data['p3_name'], data['p4_ign'], data['p4_discord_tag'], data['p4_email'], data['p4_contact'], data['p4_name']))
    result = cursor.fetchone()
    if result:
        return True
    else:
        # Check for repeated values within the received data
        all_values = [data['leader_email'], data['team_name'], data['leader_contact'], data['leader_ign'], data['leader_discord_tag'],
                      data['p2_email'], data['p2_ign'], data['p2_contact'], data['p2_discord_tag'], data['p2_name'],
                      data['p3_email'], data['p3_ign'], data['p3_contact'], data['p3_discord_tag'], data['p3_name'],
                      data['p4_email'], data['p4_ign'], data['p4_contact'], data['p4_discord_tag'], data['p4_name']]
        unique_values = set(all_values)
        if len(unique_values) != len(all_values):
            return True  # If there are repeated values within the received data, return True indicating duplicates

        # Check for uniqueness of email, IGN, team name, contact, and Discord tag across the entire database
        cursor.execute("SELECT * FROM BGMIregistrations WHERE leader_email = %s OR team_name = %s OR leader_contact = %s OR leader_ign = %s OR leader_discord_tag = %s OR p2_email = %s OR p2_ign = %s OR p2_contact = %s OR p2_discord_tag = %s OR p2_name = %s OR p3_email = %s OR p3_ign = %s OR p3_contact = %s OR p3_discord_tag = %s OR p3_name = %s OR p4_email = %s OR p4_ign = %s OR p4_contact = %s OR p4_discord_tag = %s OR p4_name = %s",
                       (data['leader_email'], data['team_name'], data['leader_contact'], data['leader_ign'], data['leader_discord_tag'], data['p2_email'], data['p2_ign'], data['p2_contact'], data['p2_discord_tag'], data['p2_name'], data['p3_email'], data['p3_ign'], data['p3_contact'], data['p3_discord_tag'], data['p3_name'], data['p4_email'], data['p4_ign'], data['p4_contact'], data['p4_discord_tag'], data['p4_name']))
        result = cursor.fetchone()
        if result:
            return True
    return False



@app.route('/')
def index():
    return 'API is working'


@app.route('/submit', methods=['POST'])
def send_email():
    data = request.get_json()
    token = generate_token()

    if check_duplicate(data):
        return jsonify({'message': 'Duplicate entry detected. IGN, Discord tag, email, or phone number is already registered.'}), 400

    email = data['leader_email']
    email_tokens[email] = token

    auth_link = generate_auth_link(token, data)
    subject = 'Authentication Link'
    body = f'''
            <html>
            <head>
                <title>{subject}</title>
            </head>
            <body>
                <h2>{subject}</h2>
                <p>Click the button below to authenticate:</p>
                <a href="{auth_link}" >Authenticate</a>
            </body>
            </html>
            '''

    yag = yagmail.SMTP(sender_email, app_password)
    yag.send(to=email, subject=subject, contents=body)

    return jsonify({'message': 'Email sent successfully.'})


@app.route('/verify/<token>', methods=['GET'])
def verify(token):
    if token in email_tokens.values():
        email = [key for key, value in email_tokens.items() if value == token][0]
        data = request.args.to_dict()

        # Insert data into the MySQL database
        cursor.execute("INSERT INTO BGMIregistrations (team_name, college_name, leader_name, leader_ign, leader_discord_tag, leader_rank, leader_contact, leader_email, p2_name, p2_ign, p2_discord_tag, p2_rank, p2_contact, p2_email, p3_name, p3_ign, p3_discord_tag, p3_rank, p3_contact, p3_email, p4_name, p4_ign, p4_discord_tag, p4_rank, p4_contact, p4_email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       (data['team_name'], data['college_name'], data['leader_name'], data['leader_ign'], data['leader_discord_tag'], data['leader_rank'], data['leader_contact'], data['leader_email'], data['p2_name'], data['p2_ign'], data['p2_discord_tag'], data['p2_rank'], data['p2_contact'], data['p2_email'], data['p3_name'], data['p3_ign'], data['p3_discord_tag'], data['p3_rank'], data['p3_contact'], data['p3_email'], data['p4_name'], data['p4_ign'], data['p4_discord_tag'], data['p4_rank'], data['p4_contact'], data['p4_email']))
        conn.commit()

        del email_tokens[email]
        return 'Authentication successful. You are now registered for Valorant in gameathon.'
    else:
        return jsonify({'message': 'Invalid or expired verification link.'}), 400


