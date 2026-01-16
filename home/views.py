from django.http import HttpResponse

def home(request):
    return HttpResponse('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Colibri Salud</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 50px; }
            h1 { color: #333; }
            .status { background-color: #e8f5e9; padding: 20px; border-radius: 5px; }
        </style>
    </head>
    <body>
        <h1>🏥 Colibri Salud</h1>
        <div class="status">
            <p><strong>✅ Django está funcionando correctamente en Vercel</strong></p>
            <p>Accede a <a href="/admin/">Panel de Administración</a> (requiere credenciales)</p>
        </div>
    </body>
    </html>
    ''')
