from flask import Flask, request, jsonify
import smtplib
import os

app = Flask(__name__)

@app.route('/notify', methods=['POST'])
def notify():
    data = request.get_json()
    nombre = data.get('nombre')
    email = data.get('email')
    telefono = data.get('telefono')
    created_at = data.get('created_at')

    print(f"[NOTIFICACIÓN] Usuario registrado: {nombre} | {email} | {telefono} | {created_at}")
    return jsonify({'message': f'Notificación recibida para {nombre}'}), 200


def send_email(nombre, email):
    """Ejemplo básico de envío de correo (configurable por SMTP)."""
    try:
        smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", 587))
        smtp_user = os.getenv("SMTP_USER")
        smtp_pass = os.getenv("SMTP_PASS")

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            message = f"Subject: Nuevo usuario registrado\n\nEl usuario {nombre} ({email}) se ha registrado."
            server.sendmail(smtp_user, smtp_user, message)
            print(f"[EMAIL] Notificación enviada a {smtp_user}")
    except Exception as e:
        print(f"[ERROR] No se pudo enviar el correo: {e}")

@app.route("/health", methods=["GET"])
def health():
	return {"status": "ok"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
