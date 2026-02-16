function showError(statusCode, message) {
    const errorDisplay = document.getElementById('error-display');
    const errorCat = document.getElementById('error-cat');
    const errorMessage = document.getElementById('error-message');

    if (statusCode >= 400) {
        errorCat.src = `https://http.cat/${statusCode}`;
        errorMessage.textContent = message;
        errorDisplay.style.display = 'flex';

        setTimeout(() => {
            errorDisplay.style.display = 'none';
        }, 5000);
    }
}
