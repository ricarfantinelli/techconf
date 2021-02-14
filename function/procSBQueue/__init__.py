import logging
import azure.functions as func
import psycopg2
import os
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def main(msg: func.ServiceBusMessage):
    notification_id = int(msg.get_body().decode('utf-8'))
    logging.info("Python ServiceBus queue trigger processed message: %s",notification_id)

    # TODO: Get connection to database
    conn = psycopg2.connect(os.environ['PostConn'])
    logging.info("Connectou")
    try:
        cursor = conn.cursor()
        sqlNotification = "SELECT subject, message FROM PUBLIC.NOTIFICATION WHERE ID = {0}".format(str(notification_id))
        logging.info(f"the notificationid is {str(notification_id)}")
        cursor.execute(sqlNotification)
        notification_rec = cursor.fetchall()
        for notif in notification_rec:
            subject_email = notif[0]
            message_email = notif[1]

        # TODO: Get attendees email and name
        sqlAttendees = "SELECT first_name, email FROM PUBLIC.ATTENDEE"
        cursor.execute(sqlAttendees)
        attendees_rec = cursor.fetchall()
        logging.info("selected all attendees")

        # TODO: Loop through each attendee and send an email with a personalized subject
        for attendee in attendees_rec:
            send_email_attendees(email_from="fantaere@gmail.com", email_to=attendee[1], 
                                 subject=subject_email, message=message_email, 
                                 attendee_name=attendee[0])

        # TODO: Update the notification table by setting the completed date and updating the 
        # status with the total number of attendees notified
        logging.info("Before updating notifications")
        update_status_completedate_notific(conexao=conn, cursor=cursor, nro_attendees=len(attendees_rec), not_id=str(notification_id))
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        cursor.close()
        conn.close()

# function to send emails to attendees
def send_email_attendees(email_from, email_to, subject, message, attendee_name):
    message = Mail(
                from_email=email_from,
                to_emails=email_to,
                subject=subject + " " + attendee_name,
                html_content=message)
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        logging.info(response.status_code)
        logging.info(response.body)
        logging.info(response.headers)
    except Exception as e:
        logging.error(e.message)


# function to update notification
def update_status_completedate_notific(conexao, cursor, nro_attendees, not_id) :
    datetime_obj = datetime.now()
    sql_update_not = ("update PUBLIC.NOTIFICATION " 
                      "SET STATUS = 'Nro de attendees is " + str(nro_attendees) + "',"
                      "COMPLETED_DATE = '" + str(datetime_obj) + "'"
                      "WHERE ID = " + str(not_id))
    cursor.execute(sql_update_not)
    conexao.commit()