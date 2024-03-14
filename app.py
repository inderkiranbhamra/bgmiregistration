from flask import Flask, request, jsonify
from flask_cors import CORS
import yagmail
import mysql.connector
import secrets
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

# cursor.execute("CREATE TABLE IF NOT EXISTS UniqueIGN (ign VARCHAR(255) UNIQUE)")
# conn.commit()
# cursor.execute("DROP TABLE IF EXISTS UniqueIGN")
# conn.commit()

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


def check_duplicate_email(data):
    email_set = set()
    emails = [data['leader_email'], data['p2_email'], data['p3_email'], data['p4_email']]
    for email in emails:
        if email in email_set:
            print("Duplicate email detected:", email)
            return True
        else:
            email_set.add(email)

    for email in emails:
        cursor.execute("SELECT * FROM UniqueEmails2 WHERE email = %s", (email,))
        result = cursor.fetchone()
        if result:
            print("Duplicate email detected:", email)
            return True

    return False


def check_duplicate_ign(data):
    ign_set = set()
    igns = [data['leader_ign'], data['p2_ign'], data['p3_ign'], data['p4_ign']]
    for ign in igns:
        if ign in ign_set:
            print("Duplicate IGN detected:", ign)
            return True
        else:
            ign_set.add(ign)

    for ign in igns:
        cursor.execute("SELECT * FROM UniqueIGN WHERE ign = %s", (ign,))
        result = cursor.fetchone()
        if result:
            print("Duplicate ign detected:", ign)
            return True

    return False

@app.route('/')
def index():
    return 'API is working'


@app.route('/submit', methods=['POST'])
def send_email():
    data = request.get_json()
    token = generate_token()

    uniqueemails = [data['leader_email'], data['p2_email'], data['p3_email'], data['p4_email']]
    uniqueigns = [data['leader_ign'], data['p2_ign'], data['p3_ign'], data['p4_ign']]

    if check_duplicate_email(data):
        return jsonify({'message': 'Duplicate email detected.'}), 400

    if check_duplicate_ign(data):
        return jsonify({'message': 'Duplicate IGN detected.'}), 400


    email = data['leader_email']
    email_tokens[email] = token

    auth_link = generate_auth_link(token, data)
    subject = 'Authentication Email for BGMI Registration'
    body = f'''
            <html>
            <head>
                <title>{subject}</title>
            </head>
            <body>
                <h2>Click on the link below to complete your registration:</h2>
                <h2><a href="{auth_link}" >Click Here</a><h2>
            </body>
            </html>
            '''

    yag = yagmail.SMTP(sender_email, app_password)
    yag.send(to=email, subject=subject, contents=body)

    return jsonify({'message': 'Email sent successfully.'})


@app.route('/verify/<token>', methods=['GET'])
def verify(token):
    if token in email_tokens.values():
        emails = [key for key, value in email_tokens.items() if value == token][0]
        data = request.args.to_dict()
        uniqueemails = [data['leader_email'], data['p2_email'], data['p3_email'], data['p4_email']]
        uniqueigns = [data['leader_ign'], data['p2_ign'], data['p3_ign'], data['p4_ign']]

        try:
            for y in uniqueigns:
                cursor.execute("INSERT INTO UniqueIGN (ign) VALUES (%s)", (y,))
            conn.commit()

            for x in uniqueemails:
                cursor.execute("INSERT INTO UniqueEmails2 (email) VALUES (%s)", (x,))
            conn.commit()

            cursor.execute("INSERT INTO BGMIregistrations (team_name, college_name, leader_name, leader_ign, leader_discord_tag, leader_rank, leader_contact, leader_email, p2_name, p2_ign, p2_discord_tag, p2_rank, p2_contact, p2_email, p3_name, p3_ign, p3_discord_tag, p3_rank, p3_contact, p3_email, p4_name, p4_ign, p4_discord_tag, p4_rank, p4_contact, p4_email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                           (data['team_name'], data['college_name'], data['leader_name'], data['leader_ign'], data['leader_discord_tag'], data['leader_rank'], data['leader_contact'], data['leader_email'], data['p2_name'], data['p2_ign'], data['p2_discord_tag'], data['p2_rank'], data['p2_contact'], data['p2_email'], data['p3_name'], data['p3_ign'], data['p3_discord_tag'], data['p3_rank'], data['p3_contact'], data['p3_email'], data['p4_name'], data['p4_ign'], data['p4_discord_tag'], data['p4_rank'], data['p4_contact'], data['p4_email']))
            conn.commit()

            del email_tokens[emails]
            return 'Authentication successful. You are now registered for BGMI in gameathon.'
        except mysql.connector.Error as err:
            print("Error inserting data:", err)
            conn.rollback()
            return jsonify({'message': 'Error inserting data into database.'}), 500
    else:
        return jsonify({'message': 'Invalid or expired verification link.'}), 400
