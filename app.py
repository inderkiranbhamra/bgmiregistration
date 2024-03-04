from flask import Flask, request, jsonify, redirect, url_for, send_file
from flask_cors import CORS  # Import CORS
import yagmail
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import secrets
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for your Flask app


# Set the secret key for the session
app.secret_key = 'inderkiran@24'

# Email configuration
sender_email = 'hackoverflow@cumail.in'  # replace with your email
app_password = 'lgde lflp hmgu krrd'  # replace with your generated app password

# Google Sheets configuration
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('bgmi-registration-e1d0ccd3b338.json', scope)
gc = gspread.authorize(credentials)
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1Y02mNph9lvPE-LmoJ2Ks6BZ4T84_HPF-O1toDIqYe3w/edit#gid=0'
sh = gc.open_by_url(spreadsheet_url)
worksheet = sh.get_worksheet(2)  # Assuming you are working with the first sheet

# Dictionary to store email verification tokens
email_tokens = {}


# Function to generate a random token
def generate_token():
    return secrets.token_hex(16)


# Function to generate an authentication link with token
def generate_auth_link(token, team_name, college_name, leader_name, leader_ign, leader_discord_tag, leader_rank,
                       leader_contact, leader_email, p2_name, p2_ign, p2_discord_tag, p2_rank, p2_contact, p2_email,
                       p3_name, p3_ign, p3_discord_tag, p3_rank, p3_contact, p3_email, p4_name, p4_ign, p4_discord_tag,
                       p4_rank, p4_contact, p4_email, p5_name, p5_ign, p5_discord_tag, p5_rank, p5_contact, p5_email):
    # Replace spaces with underscores in each parameter
    team_name = team_name.replace(' ', '_')
    college_name = college_name.replace(' ', '_')
    leader_name = leader_name.replace(' ', '_')
    leader_ign = leader_ign.replace(' ', '_')
    leader_discord_tag = leader_discord_tag.replace(' ', '_')
    leader_rank = leader_rank.replace(' ', '_')
    leader_contact = leader_contact.replace(' ', '_')  # Added space
    leader_email = leader_email.replace(' ', '_')  # Added space
    p2_name = p2_name.replace(' ', '_')
    p2_ign = p2_ign.replace(' ', '_')
    p2_discord_tag = p2_discord_tag.replace(' ', '_')
    p2_rank = p2_rank.replace(' ', '_')  # Added space
    p2_contact = p2_contact.replace(' ', '_')  # Added space
    p2_email = p2_email.replace(' ', '_')  # Added space
    p3_name = p3_name.replace(' ', '_')
    p3_ign = p3_ign.replace(' ', '_')
    p3_discord_tag = p3_discord_tag.replace(' ', '_')
    p3_rank = p3_rank.replace(' ', '_')  # Added space
    p3_contact = p3_contact.replace(' ', '_')  # Added space
    p3_email = p3_email.replace(' ', '_')  # Added space
    p4_name = p4_name.replace(' ', '_')
    p4_ign = p4_ign.replace(' ', '_')
    p4_discord_tag = p4_discord_tag.replace(' ', '_')
    p4_rank = p4_rank.replace(' ', '_')  # Added space
    p4_contact = p4_contact.replace(' ', '_')  # Added space
    p4_email = p4_email.replace(' ', '_')  # Added space
    p5_name = p5_name.replace(' ', '_')
    p5_ign = p5_ign.replace(' ', '_')
    p5_discord_tag = p5_discord_tag.replace(' ', '_')
    p5_rank = p5_rank.replace(' ', '_')  # Added space
    p5_contact = p5_contact.replace(' ', '_')  # Added space
    p5_email = p5_email.replace(' ', '_')  # Added space

    # Construct the authentication link with modified parameters
    auth_link = f'https://bgmiregistration.vercel.app/verify/{token}?team_name={team_name}&college_name={college_name}&leader_name={leader_name}&leader_ign={leader_ign}&leader_discord_tag={leader_discord_tag}&leader_rank={leader_rank}&leader_contact={leader_contact}&leader_email={leader_email}&p2_name={p2_name}&p2_ign={p2_ign}&p2_discord_tag={p2_discord_tag}&p2_rank={p2_rank}&p2_contact={p2_contact}&p2_email={p2_email}&p3_name={p3_name}&p3_ign={p3_ign}&p3_discord_tag={p3_discord_tag}&p3_rank={p3_rank}&p3_contact={p3_contact}&p3_email={p3_email}&p4_name={p4_name}&p4_ign={p4_ign}&p4_discord_tag={p4_discord_tag}&p4_rank={p4_rank}&p4_contact={p4_contact}&p4_email={p4_email}&p5_name={p5_name}&p5_ign={p5_ign}&p5_discord_tag={p5_discord_tag}&p5_rank={p5_rank}&p5_contact={p5_contact}&p5_email={p5_email}'
    return auth_link

# Route to handle form submission and send authentication email
@app.route('/submit', methods=['POST'])
def send_email():
    if request.method == 'POST':
        team_name = request.form.get('team_name')
        college_name = request.form.get('college_name')
        leader_name = request.form.get('leader_name')
        leader_ign = request.form.get('leader_ign')
        leader_discord_tag = request.form.get('leader_discord_tag')
        leader_rank = request.form.get('leader_rank')
        leader_contact = request.form.get('leader_contact')
        leader_email = request.form.get('leader_email')
        p2_name = request.form.get('p2_name')
        p2_ign = request.form.get('p2_ign')
        p2_discord_tag = request.form.get('p2_discord_tag')
        p2_rank = request.form.get('p2_rank')
        p2_contact = request.form.get('p2_contact')
        p2_email = request.form.get('p2_email')
        p3_name = request.form.get('p3_name')
        p3_ign = request.form.get('p3_ign')
        p3_discord_tag = request.form.get('p3_discord_tag')
        p3_rank = request.form.get('p3_rank')
        p3_contact = request.form.get('p3_contact')
        p3_email = request.form.get('p3_email')
        p4_name = request.form.get('p4_name')
        p4_ign = request.form.get('p4_ign')
        p4_discord_tag = request.form.get('p4_discord_tag')
        p4_rank = request.form.get('p4_rank')
        p4_contact = request.form.get('p4_contact')
        p4_email = request.form.get('p4_email')
        p5_name = request.form.get('p5_name')
        p5_ign = request.form.get('p5_ign')
        p5_discord_tag = request.form.get('p5_discord_tag')
        p5_rank = request.form.get('p5_rank')
        p5_contact = request.form.get('p5_contact')
        p5_email = request.form.get('p5_email')

        token = generate_token()
        email = leader_email  # Assuming leader's email is used for verification
        email_tokens[email] = token

        # Construct authentication link with all required parameters
        auth_link = generate_auth_link(token, team_name, college_name, leader_name, leader_ign, leader_discord_tag,
                                       leader_rank, leader_contact, leader_email, p2_name, p2_ign, p2_discord_tag,
                                       p2_rank, p2_contact, p2_email, p3_name, p3_ign, p3_discord_tag, p3_rank,
                                       p3_contact, p3_email, p4_name, p4_ign, p4_discord_tag, p4_rank, p4_contact,
                                       p4_email, p5_name, p5_ign, p5_discord_tag, p5_rank, p5_contact, p5_email)
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

        # Create yagmail SMTP client
        yag = yagmail.SMTP(sender_email, app_password)

        # Send the email
        yag.send(to=email, subject=subject, contents=body)

        return redirect(url_for('email_sent'))


# Route to inform user that email has been sent
@app.route('/email_sent')
def email_sent():
    return send_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'email_sent.html'))


# Route to handle verification
@app.route('/verify/<token>', methods=['GET'])
def verify(token):
    if token:
        # Check if the token exists in email_tokens
        if token in email_tokens.values():
            # Get the email associated with the token
            email = [key for key, value in email_tokens.items() if value == token][0]

            # Retrieve data from the query parameters
            team_name = request.args.get('team_name')
            college_name = request.args.get('college_name')
            leader_name = request.args.get('leader_name')
            leader_ign = request.args.get('leader_ign')
            leader_discord_tag = request.args.get('leader_discord_tag')
            leader_rank = request.args.get('leader_rank')
            leader_contact = request.args.get('leader_contact')
            leader_email = request.args.get('leader_email')
            p2_name = request.args.get('p2_name')
            p2_ign = request.args.get('p2_ign')
            p2_discord_tag = request.args.get('p2_discord_tag')
            p2_rank = request.args.get('p2_rank')
            p2_contact = request.args.get('p2_contact')
            p2_email = request.args.get('p2_email')
            p3_name = request.args.get('p3_name')
            p3_ign = request.args.get('p3_ign')
            p3_discord_tag = request.args.get('p3_discord_tag')
            p3_rank = request.args.get('p3_rank')
            p3_contact = request.args.get('p3_contact')
            p3_email = request.args.get('p3_email')
            p4_name = request.args.get('p4_name')
            p4_ign = request.args.get('p4_ign')
            p4_discord_tag = request.args.get('p4_discord_tag')
            p4_rank = request.args.get('p4_rank')
            p4_contact = request.args.get('p4_contact')
            p4_email = request.args.get('p4_email')
            p5_name = request.args.get('p5_name')
            p5_ign = request.args.get('p5_ign')
            p5_discord_tag = request.args.get('p5_discord_tag')
            p5_rank = request.args.get('p5_rank')
            p5_contact = request.args.get('p5_contact')
            p5_email = request.args.get('p5_email')

            # Check if all required parameters are present
            if team_name and college_name and leader_name and leader_ign and leader_discord_tag and leader_rank \
                    and leader_contact and leader_email and p2_name and p2_ign and p2_discord_tag and p2_rank \
                    and p2_contact and p2_email and p3_name and p3_ign and p3_discord_tag and p3_rank and p3_contact \
                    and p3_email and p4_name and p4_ign and p4_discord_tag and p4_rank and p4_contact and p4_email \
                    and p5_name and p5_ign and p5_discord_tag and p5_rank and p5_contact and p5_email:
                # Append new data to Google Sheets
                new_row = [team_name, college_name, leader_name, leader_ign, leader_discord_tag, leader_rank,
                           leader_contact, leader_email, p2_name, p2_ign, p2_discord_tag, p2_rank, p2_contact,
                           p2_email, p3_name, p3_ign, p3_discord_tag, p3_rank, p3_contact, p3_email, p4_name,
                           p4_ign, p4_discord_tag, p4_rank, p4_contact, p4_email, p5_name, p5_ign, p5_discord_tag,
                           p5_rank, p5_contact, p5_email]
                worksheet.append_row(new_row)
                # Remove token from dictionary after verification
                del email_tokens[email]
                return jsonify({'message': 'Authentication successful. Data stored into Google Sheets.'})
            else:
                return jsonify({'message': 'Missing parameters in the verification link.'}), 400
        else:
            return jsonify({'message': 'Invalid or expired verification link.'}), 400
    else:
        return jsonify({'message': 'No token provided.'}), 400

