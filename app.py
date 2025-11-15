from flask import Flask, request, jsonify
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

@app.route('/notify', methods=['POST'])
def notify():
    data = request.get_json()
    nombre = data.get('nombre', 'Usuario')
    email = data.get('email', 'No especificado')
    telefono = data.get('telefono', 'No especificado')
    created_at = data.get('created_at', 'Ahora')

    print(f"[NOTIFICACIÓN] Usuario registrado: {nombre} | {email} | {telefono} | {created_at}")
    
    # Enviar el email
    result = send_email(nombre, email, telefono, created_at)
    
    if result:
        return jsonify({'message': f'Notificación enviada para {nombre}', 'email_sent': True}), 200
    else:
        return jsonify({'message': f'Notificación recibida para {nombre}', 'email_sent': False}), 200


def send_email(nombre, email, telefono, created_at):
    """Envío de correo con configuración SMTP."""
    try:
        # Leer variables de entorno (con nombres correctos)
        smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", 587))
        smtp_user = os.getenv("SMTP_USER")
        smtp_password = os.getenv("SMTP_PASSWORD")
        smtp_from = os.getenv("SMTP_FROM", smtp_user)
        admin_email = os.getenv("ADMIN_EMAIL", smtp_user)

        if not smtp_user or not smtp_password:
            print("[ERROR] SMTP_USER o SMTP_PASSWORD no configurados")
            return False

        # Crear mensaje
        msg = MIMEMultipart()
        msg['From'] = smtp_from
        msg['To'] = admin_email
        msg['Subject'] = f"🎉 Nuevo usuario registrado: {nombre}"

        body = f"""
        ¡Nuevo usuario registrado en el sistema!
        
        📋 Detalles:
        - Nombre: {nombre}
        - Email: {email}
        - Teléfono: {telefono}
        - Fecha: {created_at}
        
        ---
        Este es un mensaje automático del sistema de notificaciones.
        """
        
        msg.attach(MIMEText(body, 'plain'))

        # Enviar email
        print(f"[EMAIL] Conectando a {smtp_host}:{smtp_port}...")
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            print(f"[EMAIL] Autenticando como {smtp_user}...")
            server.login(smtp_user, smtp_password)
            print(f"[EMAIL] Enviando email a {admin_email}...")
            server.send_message(msg)
            print(f"[EMAIL] ✅ Notificación enviada exitosamente a {admin_email}")
            return True
            
    except Exception as e:
        print(f"[ERROR] ❌ No se pudo enviar el correo: {e}")
        return False

@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}, 200

if __name__ == "__main__":
    print("[INFO] Iniciando servidor de notificaciones...")
    print(f"[INFO] SMTP configurado: {os.getenv('SMTP_HOST')}:{os.getenv('SMTP_PORT')}")
    print(f"[INFO] Usuario SMTP: {os.getenv('SMTP_USER')}")
    app.run(host="0.0.0.0", port=5000)
