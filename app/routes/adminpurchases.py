from fastapi import APIRouter, Depends, HTTPException, Query, Body, BackgroundTasks, Request
from sqlalchemy.orm import Session
from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions, IntegrationCommerceCodes, IntegrationApiKeys
from pydantic import EmailStr, BaseModel
from transbank.common.integration_type import IntegrationType
import requests
import boto3
import json
from app.db import crud
from app.db.database import SessionLocal
from typing import List
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import httpx

BACKEND_URL = "http://fastapi_app_e2:8000"

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


def send_email(to_email, subject, body):
    try:
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

@router.post('/')
async def webpay_confirm(event_data: dict = Body(...), db: Session = Depends(get_db)):
    try:
        transaction = Transaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS, IntegrationApiKeys.WEBPAY, IntegrationType.TEST))
        token_ws = event_data["token_ws"]
        mail = event_data["mail"]
        user_id = event_data["user_id"]
        if not token_ws:
            session_id = event_data["session_id"]
            crud.update_ticket(db, session_id, "invalid")
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

            #Hacer predicción
            try:
                async with httpx.AsyncClient() as client:
                    print("HAGAMOS UNA PREDCICCION")
                    make_prediction_response = await client.post(f"{BACKEND_URL}/predictions/", json={"user_id": user_id})
                    make_prediction_result = make_prediction_response.json()
                    print("PREDICCION REALIZADA")
                    print(make_prediction_result)
            except Exception as e:
                print("Error making prediction: ", e)

            return {'message': 'Transaction confirmed'}
        else:
            crud.update_ticket(db, response["session_id"], "invalid")
            message = {
                'request_id': response["session_id"],
                'valid': False,
            }
            return {'message': 'Transaction cancelled'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
lambda_client = boto3.client('lambda', region_name='us-east-2')