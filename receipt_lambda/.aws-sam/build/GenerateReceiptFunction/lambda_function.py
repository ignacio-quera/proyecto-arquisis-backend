import json
import boto3
import base64
from botocore.exceptions import NoCredentialsError
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
import datetime

s3 = boto3.client('s3')

def generate_pdf(ticket_data):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Define FlightApp logo

    # Define current date
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Set font
    c.setFont("Helvetica", 12)

    # Draw current date
    c.drawString(400, 780, f"Date: {current_date}")

    # Draw ticket information
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 650, "Flight Ticket")
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 620, "Ticket Information:")
    c.setFont("Helvetica", 12)
    c.drawString(70, 590, f"Name: {ticket_data['name']}")
    c.drawString(70, 570, f"Group Number: 23")
    c.drawString(70, 550, f"Flight Number: {ticket_data['flight_number']}")
    c.drawString(70, 530, f"Departure: {ticket_data['departure']}")
    c.drawString(70, 510, f"Arrival: {ticket_data['arrival']}")
    c.drawString(70, 490, f"Seat: {ticket_data['seat']}")
    c.drawString(70, 470, f"Price: {ticket_data['price']}")
    
    c.showPage()
    c.save()
    
    buffer.seek(0)
    return buffer

def lambda_handler(event, context):
    try:
        # Parse the event data, which is a dictionary
        event = json.dumps(event)
        ticket_data = json.loads(event)
        
        # Generate the PDF
        pdf_buffer = generate_pdf(ticket_data)
        
        # Define S3 bucket and object key
        bucket_name = 'ticket-receipt-bucket'
        object_key = f"receipts/{ticket_data['ticket_id']}.pdf"
        
        # Upload PDF to S3  
        s3.put_object(
            Bucket=bucket_name,
            Key=object_key,
            Body=pdf_buffer,
            ContentType='application/pdf'
        )
        
        
        pdf_file = s3.get_object(Bucket=bucket_name, Key=object_key)
        pdf_content = pdf_file['Body'].read()
        encoded_pdf = base64.b64encode(pdf_content).decode('utf-8')
        ticket_id = ticket_data['ticket_id']
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/pdf',
                'Content-Disposition': f'attachment; filename=receipts/{ticket_id}.pdf'
            },
            'body': encoded_pdf,
            'isBase64Encoded': False
        }
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Receipt generated!',
                'download_url': url
            })
        }
    except NoCredentialsError:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Credentials not available'}),
            'headers': {'Content-Type': 'application/json'}
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {'Content-Type': 'application/json'}
        }
