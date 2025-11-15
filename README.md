# Kubernetes Manifests - Users App

Manifiestos de Kubernetes para el despliegue de la aplicación de gestión de usuarios en AWS EKS.

## Estructura
```
├── backend/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── migration-job.yaml
├── frontend/
│   ├── deployment.yaml
│   └── service.yaml
├── notification/
│   ├── deployment.yaml
│   └── service.yaml
└── backend-env-config.yaml
```

## Uso
```bash
# Crear namespace
kubectl create namespace users-app

# Aplicar ConfigMaps
kubectl apply -f backend-env-config.yaml

# Desplegar servicios
kubectl apply -f backend/
kubectl apply -f frontend/
kubectl apply -f notification/
```

## Notas de Seguridad

⚠️ **IMPORTANTE**: Los Secrets (db-credentials, smtp-credentials) NO están incluidos en este repositorio por seguridad. Deben crearse manualmente:
```bash
kubectl create secret generic db-credentials \
  --from-literal=DB_HOST=<your-rds-endpoint> \
  --from-literal=DB_PORT=5432 \
  --from-literal=DB_NAME=postgres \
  --from-literal=DB_USER=<username> \
  --from-literal=DB_PASSWORD=<password> \
  -n users-app
```
