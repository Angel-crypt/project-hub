var _callActionUrl = '';
var _callMode = 'create';

function resetCallForm() {
    var form = document.getElementById('call-form');
    form.reset();

    var errors = form.querySelectorAll('.field-error');
    for (var i = 0; i < errors.length; i++) {
        errors[i].textContent = '';
    }

    var errorInputs = form.querySelectorAll('.form-input--error');
    for (var i = 0; i < errorInputs.length; i++) {
        errorInputs[i].classList.remove('form-input--error');
    }

    form.querySelector('[type="submit"]').disabled = true;
}

function openCallCreateModal(createUrl) {
    _callMode = 'create';
    _callActionUrl = createUrl;

    document.getElementById('modal-call-title').textContent = 'Crear Convocatoria';
    document.getElementById('call-submit-btn').textContent = 'Crear Convocatoria';

    resetCallForm();
    document.getElementById('modal-call').style.display = 'flex';
}

function openCallEditModal(actionUrl, title, description, openingDate, closingDate) {
    _callMode = 'edit';
    _callActionUrl = actionUrl;

    document.getElementById('modal-call-title').textContent = 'Editar Convocatoria';
    document.getElementById('call-submit-btn').textContent = 'Guardar';

    var titleInput = document.getElementById('call-title');
    var descInput = document.getElementById('call-description');
    var openInput = document.getElementById('call-opening_date');
    var closeInput = document.getElementById('call-closing_date');

    titleInput.value = title;
    descInput.value = description;
    openInput.value = openingDate;
    closeInput.value = closingDate;

    titleInput.dispatchEvent(new Event('input'));
    openInput.dispatchEvent(new Event('input'));
    closeInput.dispatchEvent(new Event('input'));

    document.getElementById('modal-call').style.display = 'flex';
}

function submitCallForm(e) {
    e.preventDefault();

    var title = document.getElementById('call-title').value.trim();
    if (!title) return false;

    fetch(_callActionUrl, {
        method: _callMode === 'create' ? 'POST' : 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            title: title,
            description: document.getElementById('call-description').value.trim(),
            opening_date: document.getElementById('call-opening_date').value,
            closing_date: document.getElementById('call-closing_date').value
        })
    })
        .then(function (res) {
            if (!res.ok) {
                return res.json().then(function (data) {
                    var errorMsg = data.error || 'Error desconocido';
                    if (data.errors) {
                        errorMsg = Object.values(data.errors).join('\n');
                    }
                    showError(res.status, errorMsg);
                    return { ok: false };
                });
            }
            return res.json().then(function (data) { return { ok: true, data: data }; });
        })
        .then(function (result) {
            if (result && result.ok) {
                location.reload();
            }
        })
        .catch(function (error) {
            console.error('Error:', error);
            showError(503, 'Error de conexión o del servidor.');
        });

    return false;
}
