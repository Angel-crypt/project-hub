// error-handler.js - Manejo centralizado de errores con http.cat

/**
 * Muestra un error con imagen de http.cat
 * @param {number} statusCode - Código de estado HTTP
 * @param {string} message - Mensaje de error a mostrar
 */
function showError(statusCode, message) {
    const errorDisplay = document.getElementById('error-display');
    const errorCat = document.getElementById('error-cat');
    const errorMessage = document.getElementById('error-message');

    // Solo mostrar imagen para códigos de error (400+)
    if (statusCode >= 400) {
        errorCat.src = `https://http.cat/${statusCode}`;
        errorMessage.textContent = message;
        errorDisplay.style.display = 'block';

        // Ocultar después de 5 segundos
        setTimeout(() => {
            errorDisplay.style.display = 'none';
        }, 5000);
    }
}
