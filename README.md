# Project Hub

## 1. Nombre del proyecto
**Project Hub** – Plataforma para gestión de proyectos académicos para estudiantes, permitiendo crear proyectos, notas y subir archivos de forma centralizada y sencilla.

---

## 2. Descripción
Project Hub es una plataforma de gestión de proyectos pensada para entornos universitarios. Permite:  

- Registro e inicio de sesión de usuarios.  
- Crear, editar, eliminar y ver proyectos propios.  
- Crear, editar y eliminar notas asociadas a cada proyecto.  
- Subir archivos asociados a proyectos.  
- Visualizar proyectos públicos de otros usuarios.  

---

## 3. Funcionalidades
- **Usuarios:** registro, login y logout.  
- **Proyectos:** CRUD completo con opción de público/privado.  
- **Notas:** CRUD dentro de cada proyecto.  
- **Archivos:** subir, descargar y eliminar archivos asociados a proyectos.  
- **Dashboard:** vista de proyectos propios y de otros usuarios (solo lectura).  

---

## 4. Tecnologías
- **Backend:** Python, Flask  
- **Base de datos:** SQLite  
- **Frontend:** HTML5, CSS3 (semántico y responsive)
- **Control de versiones:** Git / GitHub  

---

## 5. Instalación

1. Clonar el repositorio:  
```bash
git clone https://github.com/tu-usuario/project-hub.git
cd project-hub
```

2. Crear entorno virtual e instalar dependencias:
```bash
python -m venv venv
source venv/bin/activate       # Linux/macOS
venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

3. Ejecutar la aplicación:
```bash
python app.py
```

4. Abrir en el navegador:
```bash 
http://127.0.0.1:5000
```

## 6. Estructura del proyecto
project_hub/
│
├── 📁 static
│   ├── 📁 css
│   │   └── 🎨 styles.css
│   ├── 📁 js
│   │   └── 📄 scripts.js
│   └── 📁 uploads
├── 📁 templates
│   └── 🌐 base.html
├── ⚙️ .gitignore
├── 📄 LICENSE
├── 📝 README.md
├── 🐍 app.py
└── 🐍 models.py

## 7. Uso / Flujo
1. Registrar un usuario o iniciar sesión.
2. Acceder al dashboard para ver tus proyectos.
3. Crear un proyecto nuevo y definirlo como público o privado.
4. Dentro del proyecto:
- Crear y gestionar tareas.
- Subir archivos (opcional).
5. Visualizar proyectos públicos de otros usuarios en la sección correspondiente.

## 8. Licencia
Este proyecto se distribuye bajo la licencia MIT. Ver archivo [LICENSE](./LICENSE) para más detalles.