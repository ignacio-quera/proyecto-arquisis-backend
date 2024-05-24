import json
import boto3
import time
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_pdf(data):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setFont("Helvetica", 11)
    page_center = letter[0] / 2
    pdf.drawString(30, 750, f"Grupo {data['groupNumber']}")
    pdf.drawString(page_center - pdf.stringWidth("Comprobante Compra de Acciones") / 2, 600, "Comprobante Compra de Acciones")
    pdf.drawString(page_center - pdf.stringWidth(f"Usuario: {data['username']}") / 2, 570, f"Usuario: {data['username']}")
    pdf.drawString(page_center - pdf.stringWidth(f"Stock: {data['stockName']}") / 2, 555, f"Stock: {data['stockName']}")
    pdf.drawString(page_center - pdf.stringWidth(f"Cantidad: {data['stockAmount']}") / 2, 540, f"Cantidad: {data['stockAmount']}")
    pdf.drawString(page_center - pdf.stringWidth(f"Total: ${data['paidMoney']}") / 2, 525, f"Total: ${data['paidMoney']}")
    pdf.save()
    buffer.seek(0)
    return buffer.getvalue()

def generate_receipt(event, context):
    receipt_data = json.loads(event['body'])
    pdf_buffer = generate_pdf(receipt_data)
    s3 = boto3.client('s3')
    bucket_name = 'arquisis-ifgg.me'
    key = f"receipts/{int(time.time())}.pdf"
    try:
        s3.upload_fileobj(BytesIO(pdf_buffer), bucket_name, key)
        download_url = f"https://{bucket_name}.s3.amazonaws.com/{key}"
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Receipt generated!',
                'downloadUrl': download_url
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Failed to upload PDF to S3',
                'error': str(e)
            })
        }
