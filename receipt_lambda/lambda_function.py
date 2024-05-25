import json
import boto3
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

s3 = boto3.client('s3')

def generate_pdf(ticket_data):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Draw the text on the PDF
    c.drawString(50, 750, f"Flight Ticket Receipt")
    c.drawString(50, 730, f"Passenger Name: {ticket_data['passenger_name']}")
    c.drawString(50, 710, f"Flight Number: {ticket_data['flight_number']}")
    c.drawString(50, 690, f"Departure: {ticket_data['departure']}")
    c.drawString(50, 670, f"Arrival: {ticket_data['arrival']}")
    c.drawString(50, 650, f"Seat: {ticket_data['seat']}")
    c.drawString(50, 630, f"Price: ${ticket_data['price']}")
    
    c.showPage()
    c.save()
    
    buffer.seek(0)
    return buffer

def lambda_handler(event, context):
    try:
        print(event)
        print(context)
        ticket_data = json.loads(event['body'])
        
        # Generate the PDF
        pdf_buffer = generate_pdf(ticket_data)
        
        # Define S3 bucket and object key
        bucket_name = 'your-s3-bucket-name'
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
