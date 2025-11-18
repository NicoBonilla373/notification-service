# Notification Service - Flask Microservice

> Microservicio ligero para envío de notificaciones por correo electrónico

## Descripción

Microservicio independiente desarrollado con Flask que se encarga del envío de notificaciones por correo electrónico cuando se registra un nuevo usuario en el sistema. Utiliza Gmail SMTP para el envío de emails con formato HTML.

**Características principales:**
- Microservicio ligero y rápido
- Envío de emails con formato HTML
- Integración con Gmail SMTP
- Health check endpoint
- Logs detallados de operaciones
- Manejo robusto de errores
- Configuración mediante variables de entorno
- Dockerizado para producción

## Arquitectura

```
Backend (Django)
      │
      │ HTTP POST /notify
      │ Body: { nombre, email, telefono, created_at }
      ▼
Notification Service (Flask)
      │
      ├─ Validar datos
      ├─ Construir email HTML
      ├─ Conectar a SMTP
      └─ Enviar email
            │
            ▼
      Gmail SMTP Server
            │
            ▼
      Destinatario
```

## Estructura del Proyecto

```
notification-service/
├── app.py                  # Aplicación Flask principal
├── requirements.txt        # Dependencias Python
├── Dockerfile             # Configuración Docker
├── .env.example           # Ejemplo de variables de entorno
├── .gitignore             # Archivos ignorados
└── README.md              # Este archivo
```

## Tecnologías

- **Flask 3.0** - Framework web minimalista
- **smtplib** - Librería SMTP de Python
- **email** - Construcción de mensajes MIME
- **python-dotenv 1.0** - Gestión de variables de entorno

## Requisitos Previos

- Python 3.11 o superior
- Cuenta de Gmail con verificación en 2 pasos
- Contraseña de aplicación de Gmail

## Configurar Gmail SMTP

### 1. Activar verificación en 2 pasos

1. Ir a [Cuenta de Google](https://myaccount.google.com/)
2. Seguridad → Verificación en dos pasos
3. Activar verificación en 2 pasos

### 2. Generar contraseña de aplicación

1. En Seguridad → Contraseñas de aplicaciones
2. Seleccionar "Correo" y "Otro (nombre personalizado)"
3. Nombre: "Notification Service"
4. Copiar la contraseña de 16 caracteres generada

**Importante:** Esta contraseña solo se muestra una vez. Guárdala en un lugar seguro.

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/NicoBonilla373/notification-service.git
cd notification-service
```

### 2. Crear entorno virtual

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
# En Linux/Mac:
source venv/bin/activate

# En Windows:
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tus credenciales
nano .env
```

**Variables necesarias:**

```bash
# Configuración SMTP
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tu_email@gmail.com
SMTP_PASSWORD=tu_contraseña_de_aplicacion_16_caracteres
SMTP_FROM=tu_email@gmail.com

# Email de destino
ADMIN_EMAIL=destinatario@gmail.com
```

### 5. Ejecutar el servicio

```bash
python app.py

# El servicio estará disponible en:
# http://0.0.0.0:5000
```

**Salida esperada:**
```
==================================================
[INFO] 🚀 Iniciando Notification Service...
[INFO] 📧 SMTP configurado: smtp.gmail.com
[INFO] 👤 Usuario SMTP: tu_email@gmail.com
==================================================
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
```

## Docker

### Construir imagen

```bash
docker build -t notification-service:latest .
```

### Ejecutar contenedor

```bash
docker run -d \
  --name notification-service \
  -p 5000:5000 \
  -e SMTP_HOST=smtp.gmail.com \
  -e SMTP_PORT=587 \
  -e SMTP_USER=tu_email@gmail.com \
  -e SMTP_PASSWORD=tu_contraseña_app \
  -e SMTP_FROM=tu_email@gmail.com \
  -e ADMIN_EMAIL=admin@gmail.com \
  notification-service:latest
```

### Subir a ECR (AWS)

```bash
# Login a ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  [ACCOUNT_ID].dkr.ecr.us-east-1.amazonaws.com

# Tag
docker tag notification-service:latest \
  [ACCOUNT_ID].dkr.ecr.us-east-1.amazonaws.com/notification-service:latest

# Push
docker push [ACCOUNT_ID].dkr.ecr.us-east-1.amazonaws.com/notification-service:latest
```

## Endpoints

### Base URL (desarrollo)
```
http://localhost:5000
```

### 1. Health Check

**GET** `/health`

Verifica que el servicio esté funcionando.

**Request:**
```bash
curl http://localhost:5000/health
```

**Response (200 OK):**
```json
{
  "status": "ok",
  "service": "notification-service"
}
```

### 2. Root

**GET** `/`

Información del servicio y endpoints disponibles.

**Request:**
```bash
curl http://localhost:5000/
```

**Response (200 OK):**
```json
{
  "service": "Notification Service",
  "version": "1.0",
  "endpoints": {
    "health": "/health",
    "notify": "/notify (POST)"
  }
}
```

### 3. Enviar Notificación

**POST** `/notify`

Envía una notificación por email con los datos del usuario.

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "nombre": "Juan Pérez",
  "email": "juan@example.com",
  "telefono": "099123456",
  "created_at": "2025-11-14T10:30:00Z"
}
```

**Request (ejemplo con curl):**
```bash
curl -X POST http://localhost:5000/notify \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan Pérez",
    "email": "juan@example.com",
    "telefono": "099123456",
    "created_at": "2025-11-14T10:30:00Z"
  }'
```

**Response (200 OK - Email enviado):**
```json
{
  "message": "Notificación enviada para Juan Pérez",
  "email_sent": true
}
```

**Response (200 OK - Email no enviado):**
```json
{
  "message": "Notificación recibida para Juan Pérez",
  "email_sent": false,
  "warning": "No se pudo enviar el email"
}
```

**Response (400 Bad Request):**
```json
{
  "error": "No se recibieron datos"
}
```

## Formato del Email

### Asunto
```
🎉 Nuevo usuario registrado: [Nombre del Usuario]
```

### Cuerpo (HTML)

```html
<!DOCTYPE html>
<html>
<body style="font-family: Arial, sans-serif; padding: 20px;">
  <h2 style="color: #667eea;">¡Nuevo usuario registrado!</h2>
  
  <div style="background-color: #f7fafc; padding: 20px; border-radius: 8px;
              border-left: 4px solid #667eea;">
    <h3>📋 Detalles del Usuario:</h3>
    <p><strong>👤 Nombre:</strong> Juan Pérez</p>
    <p><strong>📧 Email:</strong> juan@example.com</p>
    <p><strong>📱 Teléfono:</strong> 099123456</p>
    <p><strong>📅 Fecha de registro:</strong> 2025-11-14T10:30:00Z</p>
  </div>
  
  <hr style="margin: 20px 0; border: none; border-top: 1px solid #e2e8f0;">
  
  <p style="color: #718096; font-size: 14px;">
    Este es un mensaje automático del 
    <strong>Sistema de Gestión de Usuarios</strong>.
  </p>
</body>
</html>
```

## Logs

### Logs de consola

El servicio genera logs detallados de todas las operaciones:

```
[NOTIFICACIÓN] Usuario registrado: Juan Pérez | juan@example.com | 099123456
[EMAIL] 📤 Conectando a smtp.gmail.com:587...
[EMAIL] 🔐 Autenticando como tu_email@gmail.com...
[EMAIL] 📨 Enviando email a admin@gmail.com...
[EMAIL] ✅ Notificación enviada exitosamente a admin@gmail.com
```

### Logs de error

```
[ERROR] ❌ Error de autenticación SMTP
[INFO] Verifica tu email y contraseña de aplicación de Gmail
```

```
[ERROR] ❌ Error SMTP: [535] Username and Password not accepted
```

```
[ERROR] ❌ Error al enviar correo: Connection refused
```

### Logs en Kubernetes

```bash
# Ver logs en tiempo real
kubectl logs -f deployment/notification-service -n users-app

# Ver logs de un pod específico
kubectl logs notification-service-[pod-id] -n users-app

# Filtrar logs de emails enviados
kubectl logs -l app=notification-service -n users-app | grep "EMAIL"

# Ver últimas 50 líneas
kubectl logs -l app=notification-service -n users-app --tail=50
```

## Pruebas

### Test manual con curl

```bash
# 1. Verificar que el servicio esté corriendo
curl http://localhost:5000/health

# 2. Enviar notificación de prueba
curl -X POST http://localhost:5000/notify \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Test Usuario",
    "email": "test@example.com",
    "telefono": "099999999",
    "created_at": "2025-11-14T10:00:00Z"
  }'

# 3. Verificar el email en tu bandeja de entrada
```

### Test con Python

```python
import requests

url = "http://localhost:5000/notify"
data = {
    "nombre": "Test Usuario",
    "email": "test@example.com",
    "telefono": "099999999",
    "created_at": "2025-11-14T10:00:00Z"
}

response = requests.post(url, json=data)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
```

## Seguridad

### Mejores prácticas implementadas

1. **Variables de entorno:** Credenciales nunca en código
2. **Contraseña de aplicación:** No usar contraseña principal de Gmail
3. **TLS/SSL:** Conexión encriptada con SMTP (starttls)
4. **Timeout:** Límite de 5 segundos para conexiones SMTP
5. **Manejo de errores:** Errores capturados y logueados

### Configuración en Kubernetes

```bash
# Crear secret con credenciales SMTP
kubectl create secret generic smtp-credentials \
  --from-literal=SMTP_HOST=smtp.gmail.com \
  --from-literal=SMTP_PORT=587 \
  --from-literal=SMTP_USER=tu_email@gmail.com \
  --from-literal=SMTP_PASSWORD=contraseña_app \
  --from-literal=SMTP_FROM=tu_email@gmail.com \
  --from-literal=ADMIN_EMAIL=admin@gmail.com \
  -n users-app

# Verificar secret (sin mostrar valores)
kubectl describe secret smtp-credentials -n users-app
```

### Rotar contraseñas

```bash
# 1. Generar nueva contraseña de aplicación en Google
# 2. Actualizar secret en Kubernetes
kubectl delete secret smtp-credentials -n users-app
kubectl create secret generic smtp-credentials \
  --from-literal=SMTP_PASSWORD=nueva_contraseña \
  # ... otros valores
  -n users-app

# 3. Reiniciar deployment
kubectl rollout restart deployment/notification-service -n users-app
```

## Troubleshooting

### Error: "SMTP Authentication Failed"

**Causa:** Credenciales incorrectas o contraseña de aplicación mal configurada

**Solución:**
1. Verificar que la verificación en 2 pasos esté activada
2. Generar nueva contraseña de aplicación
3. Verificar que `SMTP_PASSWORD` tenga los 16 caracteres (sin espacios)

```bash
# Verificar variable
echo $SMTP_PASSWORD
# Debe tener 16 caracteres sin espacios
```

### Error: "Connection timed out"

**Causa:** Firewall bloqueando puerto 587

**Solución:**
```bash
# Verificar conectividad SMTP
telnet smtp.gmail.com 587

# Si falla, verificar security groups en AWS
aws ec2 describe-security-groups --group-ids [SG_ID]
```

### Error: "Must specify at least one recipient"

**Causa:** `ADMIN_EMAIL` no configurado

**Solución:**
```bash
export ADMIN_EMAIL=tu_email@gmail.com
```

### Los emails no llegan

**Posibles causas:**
1. **Spam:** Verificar carpeta de spam
2. **Límite de Gmail:** Gmail tiene límites de envío diario
3. **Email bloqueado:** El destinatario bloqueó al remitente

**Verificar logs:**
```bash
kubectl logs -l app=notification-service -n users-app | grep ERROR
```

## Monitoreo

### Métricas importantes

```bash
# Número de notificaciones enviadas
kubectl logs -l app=notification-service -n users-app | grep "✅" | wc -l

# Número de errores
kubectl logs -l app=notification-service -n users-app | grep "❌" | wc -l

# Últimas notificaciones
kubectl logs -l app=notification-service -n users-app --tail=20 | grep NOTIFICACIÓN
```

### Health check desde Kubernetes

```bash
# Verificar desde dentro del cluster
kubectl run test-notif --rm -it --image=curlimages/curl -n users-app -- \
  curl http://notification-service:5000/health
```

## Personalización

### Cambiar plantilla de email

Edita la función `send_email()` en `app.py`:

```python
body = f"""
<html>
<body>
  <!-- Tu plantilla HTML aquí -->
  <h1>Nuevo usuario: {nombre}</h1>
  <p>Email: {email}</p>
</body>
</html>
"""
```

### Agregar más tipos de notificaciones

```python
@app.route('/notify-deletion', methods=['POST'])
def notify_deletion():
    data = request.get_json()
    # Lógica para email de eliminación
    return jsonify({'message': 'Notificación de eliminación enviada'})
```

### Usar otro proveedor SMTP

```python
# Para Outlook
SMTP_HOST = "smtp-mail.outlook.com"
SMTP_PORT = 587

# Para SendGrid
SMTP_HOST = "smtp.sendgrid.net"
SMTP_PORT = 587
```


## Autor

**Nicolás Bonilla** - [NicoBonilla373](https://github.com/NicoBonilla373)

## Enlaces

- [Repositorio Principal](https://github.com/NicoBonilla373/infraestructura)
- [Backend](https://github.com/NicoBonilla373/users-backend)
- [Frontend](https://github.com/NicoBonilla373/users-frontend)
- [Manifiestos K8s](https://github.com/NicoBonilla373/k8s-manifiests)
