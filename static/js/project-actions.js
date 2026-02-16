function updatePublicLabel() {
    var label = document.getElementById('project-public-label');
    var checked = document.getElementById('project-is-public').checked;
    label.textContent = checked ? 'Hacer proyecto privado' : 'Hacer proyecto p\u00fablico';
}

function openProjectCreateModal(actionUrl) {
    const modal = document.getElementById('modal-project');
    const form = document.getElementById('project-form');
    const title = document.getElementById('modal-project-title');
    const submitBtn = document.getElementById('project-submit-btn');

    form.reset();
    form.action = actionUrl;
    form.dataset.method = 'POST';
    title.textContent = 'Crear Proyecto';
    submitBtn.textContent = 'Crear Proyecto';

    document.querySelectorAll('.field-error').forEach(el => el.textContent = '');
    document.querySelectorAll('.form-input').forEach(el => el.classList.remove('input-error'));

    document.getElementById('project-call-group').style.display = 'block';
    document.getElementById('project-call-id').required = true;

    updatePublicLabel();
    modal.style.display = 'flex';
}

function openProjectEditModal(actionUrl, name, description, isPublic) {
    const modal = document.getElementById('modal-project');
    const form = document.getElementById('project-form');
    const title = document.getElementById('modal-project-title');
    const submitBtn = document.getElementById('project-submit-btn');

    form.reset();
    form.action = actionUrl;
    form.dataset.method = 'PUT';
    title.textContent = 'Editar Proyecto';
    submitBtn.textContent = 'Guardar Cambios';

    document.getElementById('project-name').value = name;
    document.getElementById('project-description').value = description || '';
    document.getElementById('project-is-public').checked = isPublic;
    updatePublicLabel();

    document.getElementById('project-call-group').style.display = 'none';
    document.getElementById('project-call-id').required = false;

    document.querySelectorAll('.field-error').forEach(el => el.textContent = '');
    document.querySelectorAll('.form-input').forEach(el => el.classList.remove('input-error'));

    if (typeof checkFormValidity === 'function') {
        checkFormValidity(form);
    } else {
        submitBtn.disabled = false;
    }

    modal.style.display = 'flex';
}

function submitProjectForm(event) {
    event.preventDefault();
    const form = event.target;
    const submitBtn = document.getElementById('project-submit-btn');
    const originalBtnText = submitBtn.textContent;

    // Validate if library exists
    if (typeof validateForm === 'function' && !validateForm(form)) {
        return false;
    }

    submitBtn.disabled = true;
    submitBtn.textContent = 'Procesando...';

    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    data.is_public = document.getElementById('project-is-public').checked;
    const method = form.dataset.method || 'POST';

    fetch(form.action, {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify(data)
    })
        .then(function (res) {
            if (!res.ok) {
                return res.json().then(function (data) {
                    var errorMsg = data.error || 'Error desconocido';
                    if (data.errors) {
                        errorMsg = Object.values(data.errors).join('\n');
                    }
                    showError(res.status, errorMsg);
                    throw new Error(errorMsg);
                });
            }
            return res.json();
        })
        .then(function (data) {
            window.location.reload();
        })
        .catch(function (error) {
            console.error('Error:', error);
            submitBtn.disabled = false;
            submitBtn.textContent = originalBtnText;
        });

    return false;
}
