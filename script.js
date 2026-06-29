document.addEventListener('DOMContentLoaded', function() {
    const formCancion = document.getElementById('formCancion');
    const inputNombre = document.getElementById('nombreCancion');
    const inputDescripcion = document.getElementById('descripcionCancion');
    const selectCategoria = document.getElementById('categoriaCancion');
    const listaCanciones = document.getElementById('listaCanciones');
    const mensajeVacio = document.getElementById('mensajeVacio');
    const totalCancionesSpan = document.getElementById('totalCanciones');
    const estadisticasDiv = document.getElementById('estadisticasCanciones');
    const mensajeValidacion = document.getElementById('mensajeValidacion');

    let canciones = [];

    function actualizarContador() {
        const total = canciones.length;
        totalCancionesSpan.textContent = total;
        
        if (total === 0) {
            estadisticasDiv.textContent = 'No hay canciones registradas';
        } else {
            const categorias = {};
            canciones.forEach(c => {
                categorias[c.categoria] = (categorias[c.categoria] || 0) + 1;
            });
            
            let textoEstadisticas = `Total: ${total} canción${total > 1 ? 'es' : ''}\n`;
            for (const [categoria, cantidad] of Object.entries(categorias)) {
                textoEstadisticas += `• ${categoria}: ${cantidad}\n`;
            }
            estadisticasDiv.textContent = textoEstadisticas;
        }
    }

    function mostrarMensajeValidacion(mensaje, tipo = 'success') {
        mensajeValidacion.innerHTML = '';
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${tipo === 'success' ? 'success' : 'danger'} alert-dismissible fade show`;
        alertDiv.role = 'alert';
        alertDiv.innerHTML = `
            ${mensaje}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        mensajeValidacion.appendChild(alertDiv);
        
        if (tipo === 'success') {
            setTimeout(() => {
                const alert = mensajeValidacion.querySelector('.alert');
                if (alert) {
                    alert.classList.remove('show');
                    setTimeout(() => alert.remove(), 150);
                }
            }, 3000);
        }
    }

    function crearElementoCancion(cancion, index) {
        const div = document.createElement('div');
        div.className = 'cancion-item d-flex justify-content-between align-items-center p-3 mb-2 bg-white rounded shadow-sm';
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
        btnEliminar.innerHTML = '🗑️ Eliminar';
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
        items.forEach(item => item.remove());
        
        if (canciones.length === 0) {
            mensajeVacio.style.display = 'block';
        } else {
            mensajeVacio.style.display = 'none';
            canciones.forEach((cancion, index) => {
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
        mostrarMensajeValidacion(`✅ ¡"${nombre}" agregada correctamente!`, 'success');
    }

    function eliminarCancion(index) {
        if (index >= 0 && index < canciones.length) {
            const nombreEliminado = canciones[index].nombre;
            canciones.splice(index, 1);
            renderizarCanciones();
            mostrarMensajeValidacion(`🗑️ "${nombreEliminado}" eliminada correctamente`, 'success');
        }
    }

    function validarFormulario(nombre, descripcion, categoria) {
        mensajeValidacion.innerHTML = '';
        
        if (!nombre || nombre.trim() === '') {
            mostrarMensajeValidacion('❌ El nombre de la canción es obligatorio', 'danger');
            inputNombre.focus();
            return false;
        }
        
        if (nombre.trim().length < 2) {
            mostrarMensajeValidacion('❌ El nombre debe tener al menos 2 caracteres', 'danger');
            inputNombre.focus();
            return false;
        }
        
        if (!descripcion || descripcion.trim() === '') {
            mostrarMensajeValidacion('❌ La descripción es obligatoria', 'danger');
            inputDescripcion.focus();
            return false;
        }
        
        if (descripcion.trim().length < 5) {
            mostrarMensajeValidacion('❌ La descripción debe tener al menos 5 caracteres', 'danger');
            inputDescripcion.focus();
            return false;
        }
        
        if (!categoria || categoria === '') {
            mostrarMensajeValidacion('❌ Debes seleccionar una categoría', 'danger');
            selectCategoria.focus();
            return false;
        }
        
        return true;
    }

    function limpiarFormulario() {
        formCancion.reset();
        inputNombre.focus();
        mensajeValidacion.innerHTML = '';
    }

    formCancion.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const nombre = inputNombre.value;
        const descripcion = inputDescripcion.value;
        const categoria = selectCategoria.value;
        
        if (validarFormulario(nombre, descripcion, categoria)) {
            agregarCancion(nombre, descripcion, categoria);
            limpiarFormulario();
        }
    });

    formCancion.addEventListener('reset', function(e) {
        setTimeout(() => {
            mensajeValidacion.innerHTML = '';
            inputNombre.focus();
        }, 0);
    });
});