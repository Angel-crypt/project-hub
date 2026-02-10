<div align="center">

# 📚 Project Hub

### Plataforma de Gestión de Proyectos Académicos

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/) [![Flask](https://img.shields.io/badge/Flask-3.0.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/) [![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/) [![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](./LICENSE)

*Una solución centralizada y sencilla para gestionar proyectos, notas y archivos académicos*

[Características](#-características) • [Instalación](#-instalación) • [Uso](#-uso) • [Documentación](#-documentación-técnica)

</div>

---

## 📋 Descripción

**Project Hub** es una plataforma web diseñada específicamente para entornos universitarios, que permite a los estudiantes gestionar sus proyectos académicos de manera eficiente y organizada. Con una interfaz intuitiva y funcionalidades completas de CRUD, los usuarios pueden crear proyectos, tomar notas, subir archivos y colaborar compartiendo proyectos públicos.

### 🎯 Objetivo

Centralizar la gestión de proyectos académicos en una única plataforma, facilitando la organización, colaboración y seguimiento de trabajos universitarios.

---

## 🎬 Demo

> [!NOTE]
> *Proyecto en desarrollo - Capturas de pantalla próximamente*

<!-- Aquí puedes agregar un GIF o screenshot cuando tengas la aplicación funcionando:
![Dashboard](./docs/screenshot-dashboard.png)
-->

---

## ✨ Características

### 👤 Gestión de Usuarios
- ✅ Registro de nuevos usuarios
- ✅ Inicio de sesión seguro
- ✅ Cierre de sesión
- ✅ Perfiles de usuario personalizados

### 📁 Gestión de Proyectos
- ✅ **CRUD completo** (Crear, Leer, Actualizar, Eliminar)
- ✅ Proyectos **públicos** o **privados**
- ✅ Dashboard personalizado con vista de proyectos propios
- ✅ Exploración de proyectos públicos de otros usuarios

### 📝 Sistema de Notas
- ✅ Crear notas asociadas a cada proyecto
- ✅ Editar y eliminar notas
- ✅ Organización por proyecto

### 📎 Gestión de Archivos
- ✅ Subir archivos a proyectos
- ✅ Descargar archivos
- ✅ Eliminar archivos
- ✅ Almacenamiento organizado por proyecto

---

## 🛠️ Tecnologías

<table>
<tr>
<td align="center" width="33%">

### Backend
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) ![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)

Servidor web robusto y ligero

</td>
<td align="center" width="33%">

### Base de Datos
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white)

Base de datos relacional embebida

</td>
<td align="center" width="33%">

### Frontend
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white) ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white)

Diseño semántico y responsive

</td>
</tr>
</table>

---

## 🚀 Instalación

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git

### Pasos de Instalación

#### 1️⃣ Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/project-hub.git
cd project-hub
```

#### 2️⃣ Crear Entorno Virtual

**Linux / macOS:**
```bash
python -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

#### 3️⃣ Instalar Dependencias

```bash
pip install -r requirements.txt
```

#### 4️⃣ Ejecutar la Aplicación

```bash
python app.py
```

#### 5️⃣ Acceder a la Aplicación

Abre tu navegador y visita:
```
http://127.0.0.1:5000
```

> [!TIP]
> Si encuentras problemas con el puerto 5000, puedes modificar el puerto en `app.py` cambiando el parámetro `port` en `app.run()`.

---

## 📂 Estructura del Proyecto

```
project-hub/
│
├── 📁 static/                    # Archivos estáticos
│   ├── 📁 css/
│   │   └── styles.css           # Estilos CSS principales
│   ├── 📁 js/
│   │   └── scripts.js           # Scripts JavaScript
│   └── 📁 uploads/              # Archivos subidos por usuarios
│
├── 📁 templates/                 # Plantillas HTML
│   └── base.html                # Plantilla base
│
├── .gitignore                   # Archivos ignorados por Git
├── LICENSE                      # Licencia del proyecto
├── README.md                    # Este archivo
├── app.py                       # Aplicación principal Flask
├── models.py                    # Modelos de base de datos
└── requirements.txt             # Dependencias del proyecto
```

### 📄 Descripción de Archivos Principales

| Archivo | Descripción |
|---------|-------------|
| `app.py` | Punto de entrada de la aplicación Flask. Contiene las rutas y lógica del servidor |
| `models.py` | Define los modelos de datos y funciones de base de datos usando SQLite3 |
| `requirements.txt` | Dependencias de Python necesarias para el proyecto |
| `static/` | Recursos estáticos (CSS, JavaScript, archivos subidos) |
| `templates/` | Plantillas HTML renderizadas por Flask |

---

## 💡 Uso

### Flujo de Trabajo Típico

```mermaid
graph LR
    A[Registro/Login] --> B[Dashboard]
    B --> C[Crear Proyecto]
    B --> D[Ver Mis Proyectos]
    B --> E[Explorar Públicos]
    C --> F[Agregar Notas/Archivos]
```

### 📖 Guía Paso a Paso

1. **Registro e Inicio de Sesión**
   - Accede a la página principal
   - Regístrate con tus credenciales o inicia sesión si ya tienes cuenta

2. **Dashboard**
   - Visualiza todos tus proyectos en un solo lugar
   - Accede rápidamente a proyectos recientes

3. **Crear un Proyecto**
   - Haz clic en "Nuevo Proyecto"
   - Completa la información del proyecto
   - Define si será **público** (visible para todos) o **privado** (solo para ti)

4. **Gestionar Proyecto**
   - **Notas:** Agrega notas para documentar avances, ideas o recordatorios
   - **Archivos:** Sube documentos, imágenes, código fuente, etc.
   - **Editar:** Modifica la información del proyecto en cualquier momento
   - **Eliminar:** Borra proyectos que ya no necesites

5. **Explorar Proyectos Públicos**
   - Descubre proyectos de otros estudiantes
   - Inspírate con trabajos de la comunidad
   - Modo solo lectura para respetar la autoría

---

## 📚 Documentación Técnica

### Arquitectura

**Project Hub** sigue el patrón **MVC (Model-View-Controller)**:

- **Model** (`models.py`): Define la estructura de datos y funciones de base de datos usando SQLite3
- **View** (`templates/`): Plantillas HTML que renderizan la interfaz de usuario
- **Controller** (`app.py`): Rutas Flask que manejan la lógica de negocio

### Base de Datos

#### Esquema de Datos

```mermaid
erDiagram
    USER ||--o{ PROJECT : creates
    PROJECT ||--o{ NOTE : contains
    PROJECT ||--o{ FILE : has
    
    USER {
        int id PK
        string username
        string email
        string password_hash
        datetime created_at
    }
    
    PROJECT {
        int id PK
        int user_id FK
        string title
        string description
        boolean is_public
        datetime created_at
    }
    
    NOTE {
        int id PK
        int project_id FK
        string title
        string content
        datetime created_at
    }
    
    FILE {
        int id PK
        int project_id FK
        string filename
        string filepath
        datetime uploaded_at
    }
```

### API Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/` | Página principal |
| `GET/POST` | `/register` | Registro de usuario |
| `GET/POST` | `/login` | Inicio de sesión |
| `GET` | `/logout` | Cierre de sesión |
| `GET` | `/dashboard` | Dashboard del usuario |
| `GET/POST` | `/project/new` | Crear nuevo proyecto |
| `GET` | `/project/<id>` | Ver proyecto |
| `POST` | `/project/<id>/edit` | Editar proyecto |
| `POST` | `/project/<id>/delete` | Eliminar proyecto |
| `POST` | `/project/<id>/note` | Agregar nota |
| `POST` | `/project/<id>/upload` | Subir archivo |

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para contribuir:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](./LICENSE) para más detalles.

---

<div align="center">

**Hecho con ❤️ para estudiantes universitarios**

</div>