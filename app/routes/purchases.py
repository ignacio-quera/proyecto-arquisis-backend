from fastapi import APIRouter, Depends, HTTPException, Query, Body, BackgroundTasks, Request
from sqlalchemy.orm import Session
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions, IntegrationCommerceCodes, IntegrationApiKeys
from pydantic import EmailStr, BaseModel
from transbank.common.integration_type import IntegrationType
import requests
import boto3
import json
from app.db import crud
from app.db.database import SessionLocal
from typing import List

PUBLISHER_URL = "http://publisher_container:9001"


class EmailSchema(BaseModel):
    email: List[EmailStr]


conf = ConnectionConfig(
    MAIL_USERNAME = "flightmailer@gmail.com",
    MAIL_PASSWORD = "flightclave1",
    MAIL_FROM = "flightmailer@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_FROM_NAME="Flight Mailer",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)


fm = FastMail(conf)

router = APIRouter()
# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def send_email(user_email: str, subject: str, message: str):
    email_message = MessageSchema(
        subject=subject,
        recipients=[user_email],  # Lista de destinatarios
        body=message,
        subtype="html"
    )
    await fm.send_message(email_message)

@router.post('/webpayconfirm')
async def webpay_confirm(event_data: dict = Body(...), db: Session = Depends(get_db)):
    try:
        print("confirmacion de webpay")
        transaction = Transaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS, IntegrationApiKeys.WEBPAY, IntegrationType.TEST))
        token_ws = event_data["token_ws"]
        mail = event_data["mail"]
        try:
            await send_email(mail, "Confirmación de Pago", "Su pago ha sido confirmado exitosamente.")
        except Exception as e:
            print("Error sending email: ", e)
        if not token_ws:
            return {'message': 'Transaction cancelled by user'}
        response = transaction.commit(token_ws)
        if response["status"] == 'AUTHORIZED':
            message = {
                'request_id': response["session_id"],
                'valid': True,
            }
            crud.update_ticket(db, response["session_id"], "valid")
            requests.post(f'{PUBLISHER_URL}/validations', json=message)
            return {'message': 'Transaction confirmed'}
        else:
            crud.update_ticket(db, response["session_id"], "invalid")
            message = {
                'request_id': response["session_id"],
                'valid': False,
            }
            requests.post(f'{PUBLISHER_URL}/validations', json=message)
            await send_email("correo_del_usuario@example.com", "Error en Pago", "Su transacción ha sido rechazada.")
            return {'message': 'Transaction cancelled'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
lambda_client = boto3.client('lambda', region_name='us-east-2')

@router.post("/generate-receipt/")
async def generate_receipt(event_data: dict = Body(...), db: Session = Depends(get_db)):
    transaction_id = event_data["transaction_id"]
    amount = event_data["amount"]
    date = event_data["date"]
    email = event_data["email"]
    payload = {
        "transactionId": transaction_id,
        "amount": amount,
        "date": date,
        "email": email
    }
    try:
        response = lambda_client.invoke(
            FunctionName='ReceiptCreator',
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
        )
        response_payload = json.loads(response['Payload'].read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    if response_payload['statusCode'] == 200:
        return response_payload['body']
    else:
        raise HTTPException(status_code=500, detail=response_payload['body'])