import requests
import smtplib
import os
import paramiko
import schedule



EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

def restart_container():
    print('Rebooting the application...')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    key = paramiko.RSAKey.from_private_key_file('c:/Users/user/Downloads/python_rsa')
    #for redhat your public key should be added to the ~/.ssh/authorized_keys
    ssh.connect(hostname = '192.168.111.136', username = 'root', pkey = key, look_for_keys = False)
    stdin, stdout, stderr = ssh.exec_command('docker start ac2569d530e4')
    print(stdout.readlines())
    ssh.close()
    print("Application restarted.")


def send_notification(email_msg):
    with smtplib.SMTP('smtp-mail.outlook.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD )
        message = f"Subject: SERVER DOWN\n{email_msg}"
        smtp.sendmail(EMAIL_ADDRESS, "iosama.amin@gmail.com", message)
        smtp.quit()

def monitor_application():
    try:
        response = requests.get('http://192.168.111.136:8080/', timeout=5)
        print(response.status_code)
        if response.status_code == 200:
            print("Application is running well.....")

        else:
            print("APPLICATION DOWN. FIX IT")
            msg = f'''Subject: Application down DOWN\n
            Hello Ibrahim,

            Application returned {response.status_code}.
            Fix the issue please.

            Best regards,
            Python monitoring script
            '''
            send_notification(msg)
            # restart the application 
            restart_container()

    except Exception as ex:
        print(f'Connection error happened: {ex}')
        msg = f'''Subject: SERVER DOWN\n
        Hello Ibrahim,

        Application is totally inaccessible. 
        Check the ports and the network please.

        Best regards,
        Python monitoring script
        '''
        send_notification(msg)


################################# MAIN #################################################
schedule.every(5).seconds.do(monitor_application)
while True:
    schedule.run_pending()

