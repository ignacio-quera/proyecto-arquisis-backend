from fastapi import APIRouter, Depends, HTTPException, Query, Body, BackgroundTasks, Request
from sqlalchemy.orm import Session
from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions, IntegrationCommerceCodes, IntegrationApiKeys
from pydantic import EmailStr, BaseModel
from transbank.common.integration_type import IntegrationType
from app.db import crud
import requests
from app.db.database import SessionLocal
from typing import List
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import httpx

PUBLISHER_URL = "http://publisher_container:9001"

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587  # Puerto para TLS
SMTP_USERNAME = 'flightmailer@gmail.com'
SMTP_PASSWORD = 'npojawaqqasjzvoo'


router = APIRouter()
# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# async def send_email(user_email: str, subject: str, message: str):
#     email_message = MessageSchema(
#         subject=subject,
#         recipients=[user_email],  # Lista de destinatarios
#         body=message,
#         subtype="html"
#     )
#     await fm.send_message(email_message)

def send_email(to_email, subject, body):
    print("funcion send_mail")
    try:
        print("try")
        msg = MIMEMultipart()
        msg['From'] = SMTP_USERNAME
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Error al enviar correo: {e}")
        return False

@router.post('/webpayconfirm')
async def webpay_confirm(event_data: dict = Body(...), db: Session = Depends(get_db)):
    try:
        print("confirmacion de webpay")
        print(event_data)
        transaction = Transaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS, IntegrationApiKeys.WEBPAY, IntegrationType.TEST))
        token_ws = event_data["token_ws"]
        mail = event_data["mail"]
        user_id = event_data["user_id"]
        print(mail)
        if not token_ws:
            return {'message': 'Transaction cancelled by user'}
        
        response = transaction.commit(token_ws)
        if response["status"] == 'AUTHORIZED':
            #enviar correo
            try:
                print("sending email")
                send_email(mail, "Confirmación de Pago", "Su pago ha sido confirmado exitosamente.")
            except Exception as e:
                print("Error sending email: ", e)
            message = {
                'request_id': response["session_id"],
                'valid': True,
            }
            crud.update_ticket(db, response["session_id"], "valid")
            requests.post(f'{PUBLISHER_URL}/validations', json=message)

            #Hacer predicción
            async with httpx.AsyncClient() as client:
                print("HAGAMOS UNA PREDCICCION")
                make_prediction_response = await client.post("http://localhost:8000/predictions/make_prediction", json={"user_id": user_id})
                make_prediction_result = make_prediction_response.json()
                print("PREDICCION REALIZADA")
                print(make_prediction_result)

            return {'message': 'Transaction confirmed'}
        else:
            crud.update_ticket(db, response["session_id"], "invalid")
            message = {
                'request_id': response["session_id"],
                'valid': False,
            }
            requests.post(f'{PUBLISHER_URL}/validations', json=message)
            return {'message': 'Transaction cancelled'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))