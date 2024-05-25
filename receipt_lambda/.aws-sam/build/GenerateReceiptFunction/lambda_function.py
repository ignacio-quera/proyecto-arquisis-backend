import json
import boto3
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
    c.drawString(70, 590, f"Ticket ID: {ticket_data['ticket_id']}")
    c.drawString(70, 570, f"Passenger Name: {ticket_data['passenger_name']}")
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
        
        # Generate S3 file URL
        s3_url = f"https://{bucket_name}.s3.amazonaws.com/{object_key}"
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Receipt generated!',
                'download_url': s3_url
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Failed to generate receipt',
                'error': str(e)
            })
        }
