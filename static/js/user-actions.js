var _editUrl = '';
var _deleteUrl = '';

function openEditModal(actionUrl, currentName) {
    _editUrl = actionUrl;
    var nameInput = document.getElementById('edit-name');

    nameInput.value = currentName;
    nameInput.dispatchEvent(new Event('input'));
    document.getElementById('modal-edit').style.display = 'flex';
}

function submitEdit(e) {
    e.preventDefault();
    var name = document.getElementById('edit-name').value.trim();
    if (!name) return false;

    fetch(_editUrl, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: name })
    })
    .then(function (res) { return res.json().then(function (data) { return { ok: res.ok, data: data }; }); })
    .then(function (result) {
        if (result.ok) {
            location.reload();
        } else {
            alert(result.data.error || 'Error al actualizar.');
        }
    });

    return false;
}

function openConfirmModal(deleteUrl, userName) {
    _deleteUrl = deleteUrl;
    document.getElementById('confirm-message').textContent =
        '¿Estás seguro de eliminar a ' + userName + '? Esta acción no se puede deshacer.';
    document.getElementById('modal-confirm').style.display = 'flex';
}

function closeConfirmModal() {
    _deleteUrl = '';
    document.getElementById('modal-confirm').style.display = 'none';
}

function submitConfirm() {
    if (!_deleteUrl) return;

    fetch(_deleteUrl, { method: 'DELETE' })
    .then(function (res) { return res.json().then(function (data) { return { ok: res.ok, data: data }; }); })
    .then(function (result) {
        if (result.ok) {
            location.reload();
        } else {
            closeConfirmModal();
            alert(result.data.error || 'Error al eliminar.');
        }
    });
}
