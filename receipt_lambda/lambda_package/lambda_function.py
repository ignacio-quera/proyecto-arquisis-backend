import boto3
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
import json

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Event details
    transaction_id = event['transactionId']
    amount = event['amount']
    date = event['date']
    email = event['email']

    # Create PDF in memory
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.drawString(100, 750, "Purchase Receipt")
    p.drawString(100, 725, f"Transaction ID: {transaction_id}")
    p.drawString(100, 700, f"Amount: ${amount}")
    p.drawString(100, 675, f"Date: {date}")
    p.drawString(100, 650, f"Email: {email}")
    p.showPage()
    p.save()

    buffer.seek(0)
    
    # Define S3 bucket and key (filename)
    bucket_name = 'ticket-receipt-bucket'
    key = f'receipts/{transaction_id}.pdf'

    try:
        s3.put_object(Bucket=bucket_name, Key=key, Body=buffer, ContentType='application/pdf')
        s3_url = f'https://{bucket_name}.s3.amazonaws.com/{key}'
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'PDF generated and uploaded', 'url': s3_url})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error uploading PDF', 'error': str(e)})
        }
