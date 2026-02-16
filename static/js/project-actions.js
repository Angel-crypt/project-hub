function openProjectCreateModal(actionUrl) {
    const modal = document.getElementById('modal-project');
    const form = document.getElementById('project-form');
    const title = document.getElementById('modal-project-title');
    const submitBtn = document.getElementById('project-submit-btn');

    // Reset form
    form.reset();
    form.action = actionUrl;
    form.dataset.method = 'POST'; // Create uses POST
    title.textContent = 'Crear Proyecto';
    submitBtn.textContent = 'Crear Proyecto';

    // Clear errors
    document.querySelectorAll('.field-error').forEach(el => el.textContent = '');
    document.querySelectorAll('.form-input').forEach(el => el.classList.remove('input-error'));

    // Show call selector for creation
    document.getElementById('project-call-group').style.display = 'block';
    document.getElementById('project-call-id').required = true;

    modal.style.display = 'flex';
}

function openProjectEditModal(actionUrl, name, description) {
    const modal = document.getElementById('modal-project');
    const form = document.getElementById('project-form');
    const title = document.getElementById('modal-project-title');
    const submitBtn = document.getElementById('project-submit-btn');

    // Reset and populate form
    form.reset();
    form.action = actionUrl;
    form.dataset.method = 'PUT'; // Update uses PUT
    title.textContent = 'Editar Proyecto';
    submitBtn.textContent = 'Guardar Cambios';

    document.getElementById('project-name').value = name;
    document.getElementById('project-description').value = description || '';

    // Hide call selector for editing (cannot change call)
    document.getElementById('project-call-group').style.display = 'none';
    document.getElementById('project-call-id').required = false;

    // Clear errors
    document.querySelectorAll('.field-error').forEach(el => el.textContent = '');
    document.querySelectorAll('.form-input').forEach(el => el.classList.remove('input-error'));

    // Trigger validation to enable button if valid
    // (Assuming checkFormValidity is available if form-validation.js is included)
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
