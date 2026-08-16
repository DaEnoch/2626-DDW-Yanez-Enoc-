document.addEventListener('DOMContentLoaded', function() {

    // Referencias a elementos
    const formCancion = document.getElementById('formCancion');
    const inputNombre = document.getElementById('nombreCancion');
    const inputDescripcion = document.getElementById('descripcionCancion');
    const selectCategoria = document.getElementById('categoriaCancion');
    const listaCanciones = document.getElementById('listaCanciones');
    const mensajeVacio = document.getElementById('mensajeVacio');
    const totalCancionesSpan = document.getElementById('totalCanciones');
    const estadisticasDiv = document.getElementById('estadisticasCanciones');
    const mensajeValidacion = document.getElementById('mensajeValidacion');
    const nombreContador = document.getElementById('nombreContador');
    const descripcionContador = document.getElementById('descripcionContador');
    const alertaEstado = document.getElementById('alertaEstado');
    const spinnerContainer = document.getElementById('spinnerContainer');

    // Modal
    const modalConfirmacion = new bootstrap.Modal(document.getElementById('modalConfirmacion'));
    const modalCancionNombre = document.getElementById('modalCancionNombre');
    const modalCancionCategoria = document.getElementById('modalCancionCategoria');
    const modalMensaje = document.getElementById('modalMensaje');

    let canciones = [];

    // ============================================
    // FUNCIONES DE VALIDACION
    // ============================================

    function validarNombre(nombre) {
        const feedback = document.getElementById('nombreFeedback');
        const contador = document.getElementById('nombreContador');

        contador.textContent = nombre.length + '/50 caracteres';

        if (nombre.length === 0) {
            inputNombre.classList.remove('is-valid', 'is-invalid');
            feedback.textContent = 'El nombre es obligatorio';
            return false;
        }

        if (nombre.length < 2) {
            inputNombre.classList.remove('is-valid');
            inputNombre.classList.add('is-invalid');
            feedback.innerHTML = '<i class="bi bi-exclamation-circle me-1"></i>El nombre debe tener al menos 2 caracteres';
            return false;
        }

        if (nombre.length > 50) {
            inputNombre.classList.remove('is-valid');
            inputNombre.classList.add('is-invalid');
            feedback.innerHTML = '<i class="bi bi-exclamation-circle me-1"></i>El nombre no puede tener más de 50 caracteres';
            return false;
        }

        inputNombre.classList.remove('is-invalid');
        inputNombre.classList.add('is-valid');
        feedback.innerHTML = '<i class="bi bi-check-circle me-1"></i>¡Nombre válido!';
        return true;
    }

    function validarDescripcion(descripcion) {
        const feedback = document.getElementById('descripcionFeedback');
        const contador = document.getElementById('descripcionContador');

        contador.textContent = descripcion.length + '/200 caracteres';

        if (descripcion.length === 0) {
            inputDescripcion.classList.remove('is-valid', 'is-invalid');
            feedback.textContent = 'La descripción es obligatoria';
            return false;
        }

        if (descripcion.length < 5) {
            inputDescripcion.classList.remove('is-valid');
            inputDescripcion.classList.add('is-invalid');
            feedback.innerHTML = '<i class="bi bi-exclamation-circle me-1"></i>La descripción debe tener al menos 5 caracteres';
            return false;
        }

        if (descripcion.length > 200) {
            inputDescripcion.classList.remove('is-valid');
            inputDescripcion.classList.add('is-invalid');
            feedback.innerHTML = '<i class="bi bi-exclamation-circle me-1"></i>La descripción no puede tener más de 200 caracteres';
            return false;
        }

        inputDescripcion.classList.remove('is-invalid');
        inputDescripcion.classList.add('is-valid');
        feedback.innerHTML = '<i class="bi bi-check-circle me-1"></i>¡Descripción válida!';
        return true;
    }

    function validarCategoria(categoria) {
        const feedback = document.getElementById('categoriaFeedback');

        if (!categoria || categoria === '') {
            selectCategoria.classList.remove('is-valid');
            selectCategoria.classList.add('is-invalid');
            feedback.innerHTML = '<i class="bi bi-exclamation-circle me-1"></i>Debes seleccionar una categoría';
            return false;
        }

        selectCategoria.classList.remove('is-invalid');
        selectCategoria.classList.add('is-valid');
        feedback.innerHTML = '<i class="bi bi-check-circle me-1"></i>¡Categoría seleccionada!';
        return true;
    }

    function validarFormularioCompleto() {
        const nombreValido = validarNombre(inputNombre.value);
        const descripcionValida = validarDescripcion(inputDescripcion.value);
        const categoriaValida = validarCategoria(selectCategoria.value);

        return nombreValido && descripcionValida && categoriaValida;
    }

    // ============================================
    // EVENTOS DE VALIDACION EN TIEMPO REAL
    // ============================================

    inputNombre.addEventListener('input', function() {
        validarNombre(this.value);
    });

    inputNombre.addEventListener('blur', function() {
        if (this.value.length > 0) {
            validarNombre(this.value);
        }
    });

    inputDescripcion.addEventListener('input', function() {
        validarDescripcion(this.value);
    });

    inputDescripcion.addEventListener('blur', function() {
        if (this.value.length > 0) {
            validarDescripcion(this.value);
        }
    });

    selectCategoria.addEventListener('change', function() {
        validarCategoria(this.value);
    });

    // ============================================
    // ALERTA CONDICIONAL
    // ============================================

    function actualizarAlertaEstado() {
        const total = canciones.length;

        if (total === 0) {
            alertaEstado.innerHTML = `
                <div class="alert alert-warning" role="alert">
                    <i class="bi bi-exclamation-triangle me-2"></i>
                    Playlist vacía. Agrega tu primera canción para comenzar.
                </div>
            `;
        } else if (total < 3) {
            alertaEstado.innerHTML = `
                <div class="alert alert-info" role="alert">
                    <i class="bi bi-lightbulb me-2"></i>
                    Tienes ${total} canción${total > 1 ? 'es' : ''}. Agrega más canciones para crear una gran playlist.
                </div>
            `;
        } else {
            alertaEstado.innerHTML = `
                <div class="alert alert-success" role="alert">
                    <i class="bi bi-check-circle-fill me-2"></i>
                    ¡Excelente playlist! Tienes ${total} canciones. ¡Sigue así!
                </div>
            `;
        }
    }

    // ============================================
    // SPINNER
    // ============================================

    function mostrarSpinner(mostrar) {
        spinnerContainer.style.display = mostrar ? 'block' : 'none';
    }

    // ============================================
    // FUNCIONES DE GESTION DE CANCIONES
    // ============================================

    function actualizarContador() {
        const total = canciones.length;
        totalCancionesSpan.textContent = total;

        if (total === 0) {
            estadisticasDiv.textContent = '0 canciones';
            estadisticasDiv.className = 'fw-semibold text-muted';
        } else {
            const categorias = {};
            canciones.forEach(c => {
                categorias[c.categoria] = (categorias[c.categoria] || 0) + 1;
            });

            let textoEstadisticas = total + ' canción' + (total > 1 ? 'es' : '');
            let categoriasTexto = [];
            for (const [categoria, cantidad] of Object.entries(categorias)) {
                categoriasTexto.push(categoria + ': ' + cantidad);
            }
            if (categoriasTexto.length > 0) {
                textoEstadisticas += ' | ' + categoriasTexto.join(' • ');
            }
            estadisticasDiv.textContent = textoEstadisticas;
            estadisticasDiv.className = 'fw-semibold';
        }

        actualizarAlertaEstado();
    }

    function mostrarMensajeValidacion(mensaje, tipo) {
        mensajeValidacion.innerHTML = '';
        const alertDiv = document.createElement('div');
        alertDiv.className = 'alert alert-' + tipo + ' alert-dismissible fade show';
        alertDiv.role = 'alert';
        alertDiv.innerHTML = mensaje + ' <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>';
        mensajeValidacion.appendChild(alertDiv);

        if (tipo === 'success') {
            setTimeout(function() {
                const alert = mensajeValidacion.querySelector('.alert');
                if (alert) {
                    alert.classList.remove('show');
                    setTimeout(function() { alert.remove(); }, 150);
                }
            }, 3000);
        }
    }

    function crearElementoCancion(cancion, index) {
        const div = document.createElement('div');
        div.className = 'cancion-item d-flex justify-content-between align-items-center p-3 mb-2';
        div.setAttribute('data-index', index);

        const infoDiv = document.createElement('div');
        infoDiv.className = 'flex-grow-1';

        const titulo = document.createElement('h6');
        titulo.className = 'mb-1 fw-bold';
        titulo.textContent = cancion.nombre;

        const descripcion = document.createElement('p');
        descripcion.className = 'mb-0 text-muted small';
        descripcion.textContent = cancion.descripcion;

        const categoriaSpan = document.createElement('span');
        categoriaSpan.className = 'badge-categoria ms-2';
        categoriaSpan.textContent = cancion.categoria;

        infoDiv.appendChild(titulo);
        infoDiv.appendChild(descripcion);
        infoDiv.appendChild(categoriaSpan);

        const btnEliminar = document.createElement('button');
        btnEliminar.className = 'btn btn-outline-danger btn-sm btn-eliminar';
        btnEliminar.innerHTML = '<i class="bi bi-trash me-1"></i>Eliminar';
        btnEliminar.setAttribute('aria-label', 'Eliminar canción');

        btnEliminar.addEventListener('click', function(e) {
            e.stopPropagation();
            eliminarCancion(index);
        });

        div.appendChild(infoDiv);
        div.appendChild(btnEliminar);

        return div;
    }

    function renderizarCanciones() {
        const items = listaCanciones.querySelectorAll('.cancion-item');
        items.forEach(function(item) { item.remove(); });

        if (canciones.length === 0) {
            mensajeVacio.style.display = 'block';
        } else {
            mensajeVacio.style.display = 'none';
            canciones.forEach(function(cancion, index) {
                const elemento = crearElementoCancion(cancion, index);
                listaCanciones.appendChild(elemento);
            });
        }

        actualizarContador();
    }

    function agregarCancion(nombre, descripcion, categoria) {
        const nuevaCancion = {
            nombre: nombre.trim(),
            descripcion: descripcion.trim(),
            categoria: categoria
        };

        canciones.push(nuevaCancion);
        renderizarCanciones();

        // Mostrar modal con la información
        modalCancionNombre.textContent = nuevaCancion.nombre;
        modalCancionCategoria.textContent = 'Categoría: ' + nuevaCancion.categoria;
        modalMensaje.textContent = '"' + nuevaCancion.nombre + '" se ha agregado exitosamente.';
        modalConfirmacion.show();

        mostrarMensajeValidacion('"' + nombre + '" agregada a tu playlist', 'success');
    }

    function eliminarCancion(index) {
        if (index >= 0 && index < canciones.length) {
            const nombreEliminado = canciones[index].nombre;
            canciones.splice(index, 1);
            renderizarCanciones();
            mostrarMensajeValidacion('"' + nombreEliminado + '" eliminada de tu playlist', 'success');
        }
    }

    // ============================================
    // EVENTO SUBMIT DEL FORMULARIO
    // ============================================

    formCancion.addEventListener('submit', function(e) {
        e.preventDefault();

        if (validarFormularioCompleto()) {
            const nombre = inputNombre.value;
            const descripcion = inputDescripcion.value;
            const categoria = selectCategoria.value;

            mostrarSpinner(true);

            // Simular proceso de carga
            setTimeout(function() {
                agregarCancion(nombre, descripcion, categoria);
                mostrarSpinner(false);

                formCancion.reset();
                inputNombre.classList.remove('is-valid', 'is-invalid');
                inputDescripcion.classList.remove('is-valid', 'is-invalid');
                selectCategoria.classList.remove('is-valid', 'is-invalid');
                document.getElementById('nombreFeedback').textContent = 'El nombre es obligatorio';
                document.getElementById('descripcionFeedback').textContent = 'La descripción es obligatoria';
                document.getElementById('categoriaFeedback').textContent = 'Debes seleccionar una categoría';
                nombreContador.textContent = '0/50 caracteres';
                descripcionContador.textContent = '0/200 caracteres';
                inputNombre.focus();
            }, 800);

        } else {
            mostrarMensajeValidacion('Completa todos los campos correctamente', 'danger');
        }
    });

    // Evento reset
    formCancion.addEventListener('reset', function(e) {
        setTimeout(function() {
            inputNombre.classList.remove('is-valid', 'is-invalid');
            inputDescripcion.classList.remove('is-valid', 'is-invalid');
            selectCategoria.classList.remove('is-valid', 'is-invalid');
            mensajeValidacion.innerHTML = '';
            document.getElementById('nombreFeedback').textContent = 'El nombre es obligatorio';
            document.getElementById('descripcionFeedback').textContent = 'La descripción es obligatoria';
            document.getElementById('categoriaFeedback').textContent = 'Debes seleccionar una categoría';
            nombreContador.textContent = '0/50 caracteres';
            descripcionContador.textContent = '0/200 caracteres';
            inputNombre.focus();
        }, 0);
    });

    // Inicializar alerta condicional
    actualizarAlertaEstado();

});
