(function () {
    var forms = document.querySelectorAll('form[data-validate]');

    forms.forEach(function (form) {
        var submitBtn = form.querySelector('[type="submit"]');
        var inputs = Array.from(form.querySelectorAll('[data-validate-field]'));

        function getErrorEl(input) {
            return document.getElementById(input.id + '-error');
        }

        function validate(input) {
            var value = input.value;
            var trimmed = value.trim();

            if (input.hasAttribute('required') && !trimmed) {
                return input.dataset.errorRequired || 'Este campo es obligatorio.';
            }

            if (input.hasAttribute('minlength')) {
                var min = parseInt(input.getAttribute('minlength'));
                if (value.length > 0 && value.length < min) {
                    return input.dataset.errorMinlength || 'Mínimo ' + min + ' caracteres.';
                }
            }

            return '';
        }

        function showError(input, message) {
            var errorEl = getErrorEl(input);
            if (errorEl) errorEl.textContent = message;
            input.classList.toggle('form-input--error', !!message);
        }

        function updateCounter(input) {
            var counterId = input.dataset.counter;
            if (!counterId) return;
            var counterEl = document.getElementById(counterId);
            if (!counterEl) return;

            var len = input.value.length;
            var min = parseInt(input.getAttribute('minlength')) || 0;

            if (len === 0) {
                counterEl.textContent = '';
            } else {
                counterEl.textContent = '(' + len + '/' + min + ')';
                counterEl.classList.toggle('char-count--ok', len >= min);
            }
        }

        function checkAll() {
            var valid = true;
            inputs.forEach(function (input) {
                if (validate(input)) valid = false;
            });
            submitBtn.disabled = !valid;
        }

        function validateField(input) {
            var error = validate(input);
            showError(input, error);
            updateCounter(input);
            checkAll();
        }

        inputs.forEach(function (input) {
            input.addEventListener('input', function () { validateField(input); });
            input.addEventListener('blur', function () { validateField(input); });
        });

        form.addEventListener('submit', function (e) {
            var hasError = false;
            inputs.forEach(function (input) {
                var error = validate(input);
                showError(input, error);
                if (error) hasError = true;
            });
            if (hasError) e.preventDefault();
        });

        checkAll();
    });
})();
