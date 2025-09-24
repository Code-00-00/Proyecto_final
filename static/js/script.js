
const restaurantesData = [
  { 
    id: 1, 
    nombre: "Milano Italiano", 
    rating: 4.8, 
    cocina: ["italiana"], 
    descripcion: "Auténtica cocina italiana.",
    menu: [
      {"nombre": "Pizza Margherita", "precio": 12, "categoria": "Pizzas"},
      {"nombre": "Pasta Carbonara", "precio": 14, "categoria": "Pastas"},
      {"nombre": "Tiramisú", "precio": 8, "categoria": "Postres"}
    ]
  },
  { 
    id: 2, 
    nombre: "Sakura Sushi", 
    rating: 4.9, 
    cocina: ["japonesa"], 
    descripcion: "Sushi fresco y auténtico.",
    menu: [
      {"nombre": "Nigiri Mixto", "precio": 18, "categoria": "Nigiri"},
      {"nombre": "Miso Soup", "precio": 6, "categoria": "Sopas"},
      {"nombre": "Tempura de Camarón", "precio": 15, "categoria": "Entradas"}
    ]
  },
  { 
    id: 3, 
    nombre: "Green Garden", 
    rating: 4.7, 
    cocina: ["vegetariana"], 
    descripcion: "Comida vegetariana y vegana.",
    menu: [
      {"nombre": "Bowl de Quinoa", "precio": 10, "categoria": "Platos Principales"},
      {"nombre": "Ensalada Mediterránea", "precio": 9, "categoria": "Ensaladas"},
      {"nombre": "Smoothie de Frutas", "precio": 7, "categoria": "Bebidas"}
    ]
  }
];

// ========================
// INICIALIZACIÓN
// ========================
document.addEventListener('DOMContentLoaded', function () {
  console.log('DOM cargado correctamente');
  
  // Inicializar búsqueda
  initSearch();
  
  // Inicializar modo oscuro
  initTheme();
  
  // Inicializar modales
  initModals();
  
  // Actualizar corazones de favoritos
  updateHeartIcons();
});

// ========================
// BÚSQUEDA
// ========================
function initSearch() {
  const searchInput = document.getElementById('searchInput');
  const searchBtn = document.querySelector('.search-btn');
  
  if (searchInput) {
    console.log('Input de búsqueda encontrado');
    
    // Buscar mientras se escribe
    searchInput.addEventListener('input', function(e) {
      console.log('Input event:', e.target.value);
      filterRestaurants();
    });
    
    // Buscar al presionar Enter
    searchInput.addEventListener('keypress', function(event) {
      if (event.key === 'Enter') {
        console.log('Enter presionado');
        filterRestaurants();
      }
    });
  }
  
  if (searchBtn) {
    searchBtn.addEventListener('click', function() {
      console.log('Botón de búsqueda clickeado');
      filterRestaurants();
    });
  }
}

function filterRestaurants() {
  const searchInput = document.getElementById('searchInput');
  if (!searchInput) {
    console.log('Input de búsqueda no encontrado');
    return;
  }
  
  const searchTerm = searchInput.value.toLowerCase().trim();
  console.log('Buscando:', searchTerm);
  
  const restaurantCards = document.querySelectorAll('.restaurant-card');
  
  // Si no hay texto, mostrar todos
  if (!searchTerm) {
    restaurantCards.forEach(card => {
      card.style.display = 'block';
    });
    removeNoResultsMessage();
    return;
  }
  
  let hasResults = false;
  
  restaurantCards.forEach(card => {
    const restaurantId = parseInt(card.getAttribute('onclick').match(/\d+/)[0]);
    const restaurant = restaurantesData.find(r => r.id === restaurantId);
    
    if (restaurant) {
      const name = restaurant.nombre.toLowerCase();
      const cuisine = restaurant.cocina.join(' ').toLowerCase();
      const description = restaurant.descripcion.toLowerCase();
      
      const matches = 
        name.includes(searchTerm) || 
        cuisine.includes(searchTerm) || 
        description.includes(searchTerm);
      
      card.style.display = matches ? 'block' : 'none';
      if (matches) hasResults = true;
    }
  });
  
  if (!hasResults && searchTerm) {
    showNoResultsMessage();
  } else {
    removeNoResultsMessage();
  }
}

function showNoResultsMessage() {
  if (document.getElementById('noResults')) return;
  
  const gridContainer = document.querySelector('.restaurants-grid');
  if (gridContainer) {
    const noResultsDiv = document.createElement('div');
    noResultsDiv.id = 'noResults';
    noResultsDiv.innerHTML = `
      <div style="text-align: center; padding: 3rem; background-color: var(--card-bg); border-radius: var(--radius); margin: 2rem 0; border: 1px solid var(--border);">
        <h3>🔍 No se encontraron restaurantes</h3>
        <p>Intenta con otros términos de búsqueda</p>
      </div>
    `;
    gridContainer.parentNode.appendChild(noResultsDiv);
  }
}

function removeNoResultsMessage() {
  const noResults = document.getElementById('noResults');
  if (noResults) {
    noResults.remove();
  }
}

// ========================
// MODO OSCURO
// ========================
function initTheme() {
  const themeToggle = document.querySelector('.theme-toggle');
  const body = document.body;
  
  if (!themeToggle) return;
  
  const iconSun = `
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <circle cx="12" cy="12" r="5"></circle>
      <line x1="12" y1="1" x2="12" y2="3"></line>
      <line x1="12" y1="21" x2="12" y2="23"></line>
      <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
      <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
      <line x1="1" y1="12" x2="3" y2="12"></line>
      <line x1="21" y1="12" x2="23" y2="12"></line>
      <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
      <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
    </svg>
  `;
  
  const iconMoon = `
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
    </svg>
  `;
  
  function setTheme(theme) {
    if (theme === 'dark-mode') {
      body.classList.add('dark-mode');
      body.classList.remove('light-mode');
      themeToggle.innerHTML = iconSun;
    } else {
      body.classList.add('light-mode');
      body.classList.remove('dark-mode');
      themeToggle.innerHTML = iconMoon;
    }
  }
  
  function getSavedTheme() {
    try {
      return localStorage.getItem('theme');
    } catch (e) {
      return null;
    }
  }
  
  const savedTheme = getSavedTheme();
  const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  
  if (savedTheme === 'dark-mode') {
    setTheme('dark-mode');
  } else if (savedTheme === 'light-mode') {
    setTheme('light-mode');
  } else if (prefersDark) {
    setTheme('dark-mode');
  } else {
    setTheme('light-mode');
  }
  
  themeToggle.addEventListener('click', function () {
    if (body.classList.contains('dark-mode')) {
      setTheme('light-mode');
      try {
        localStorage.setItem('theme', 'light-mode');
      } catch (e) {}
    } else {
      setTheme('dark-mode');
      try {
        localStorage.setItem('theme', 'dark-mode');
      } catch (e) {}
    }
  });
}

// ========================
// MODALES
// ========================
function initModals() {
  // Botones del header
  const buttons = document.querySelectorAll('.auth-buttons .btn');
  buttons.forEach(btn => {
    if (btn.textContent.trim() === 'Iniciar sesión') {
      btn.onclick = openLoginModal;
    }
    if (btn.textContent.trim() === 'Registrarse') {
      btn.onclick = openRegisterModal;
    }
  });
}

function openLoginModal() {
  const modal = document.getElementById('loginModal');
  if (modal) {
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
  }
}

function openRegisterModal() {
  const modal = document.getElementById('registerModal');
  if (modal) {
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
  }
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
  }
}

window.onclick = function(event) {
  const loginModal = document.getElementById('loginModal');
  const registerModal = document.getElementById('registerModal');
  const restaurantModal = document.getElementById('restaurantModal');
  
  if (event.target === loginModal) closeModal('loginModal');
  if (event.target === registerModal) closeModal('registerModal');
  if (event.target === restaurantModal) closeModal('restaurantModal');
};

// ========================
// DETALLE DE RESTAURANTE
// ========================
function openRestaurantDetail(id) {
  const modal = document.getElementById('restaurantModal');
  const content = document.getElementById('restaurantDetailContent');
  
  const restaurante = restaurantesData.find(r => r.id === id);
  
  if (!restaurante) {
    alert('Restaurante no encontrado');
    return;
  }

  // Agrupar menú por categorías
  const menuByCategory = {};
  restaurante.menu.forEach(item => {
    if (!menuByCategory[item.categoria]) {
      menuByCategory[item.categoria] = [];
    }
    menuByCategory[item.categoria].push(item);
  });

  let menuHtml = '';
  for (const [categoria, items] of Object.entries(menuByCategory)) {
    menuHtml += `<h3 style="margin: 1.5rem 0 1rem; color: var(--primary);">${categoria}</h3>`;
    items.forEach(item => {
      menuHtml += `
        <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid var(--border);">
          <span>${item.nombre}</span>
          <span style="font-weight: 600; color: var(--primary);">$${item.precio}</span>
        </div>
      `;
    });
  }

  content.innerHTML = `
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-bottom: 2rem;">
      <div>
        <div style="width: 100%; height: 250px; background-color: #d32f2f; display: flex; align-items: center; justify-content: center; color: white; font-size: 1.5rem; font-weight: bold; border-radius: 1rem; position: relative;">
          ${restaurante.nombre}
          <div style="position: absolute; top: 10px; right: 10px; background-color: rgba(0,0,0,0.7); color: white; padding: 0.3rem 0.6rem; border-radius: 20px; font-size: 0.9rem;">
            ★ ${restaurante.rating}
          </div>
        </div>
      </div>
      <div>
        <h2 style="margin-bottom: 0.5rem;">${restaurante.nombre}</h2>
        <div style="display: flex; gap: 0.8rem; margin: 0.5rem 0;">
          ${restaurante.cocina.map(c => `<span style="background-color: rgba(243, 122, 0, 0.1); color: var(--primary); padding: 0.2rem 0.6rem; border-radius: 20px; font-size: 0.8rem; font-weight: 500;">${c.charAt(0).toUpperCase() + c.slice(1)}</span>`).join('')}
        </div>
        <p style="margin: 1rem 0; line-height: 1.6; color: #666;">${restaurante.descripcion}</p>
        <div style="display: flex; gap: 1rem; margin: 1rem 0; flex-wrap: wrap;">
          <span style="background-color: #e8f5e8; color: #2e7d32; padding: 0.2rem 0.5rem; border-radius: 50%; font-size: 0.8rem;">🚚 Delivery</span>
          <span style="background-color: #e3f2fd; color: #1565c0; padding: 0.2rem 0.5rem; border-radius: 50%; font-size: 0.8rem;">📦 Pickup</span>
          <span style="background-color: #f3e5f5; color: #7b1fa2; padding: 0.2rem 0.5rem; border-radius: 50%; font-size: 0.8rem;">🍽️ En el local</span>
        </div>
        <div style="margin: 1.5rem 0;">
          <p><strong>📍 Dirección:</strong> Av. Principal 123</p>
          <p><strong>📞 Teléfono:</strong> +56 9 1234 5678</p>
          <p><strong>🕒 Horario:</strong> 12:00 - 23:00</p>
        </div>
        <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
          <button class="btn btn-primary" style="flex: 1;" onclick="openReservationModal(${restaurante.id}, '${restaurante.nombre}')">Reservar mesa</button>
          <button class="btn btn-outline" style="flex: 1;" onclick="openOrderModal(${restaurante.id}, '${restaurante.nombre}')">Pedir online</button>
          <button class="btn btn-outline" style="width: 50px; height: 50px; padding: 0;" onclick="toggleFavorite(${restaurante.id}, event)">
            <span style="font-size: 1.5rem;">♥</span>
          </button>
        </div>
      </div>
    </div>
    <h3 style="color: var(--primary); margin: 1rem 0;">Menú</h3>
    <div style="background-color: var(--card-bg); padding: 1.5rem; border-radius: var(--radius); border: 1px solid var(--border);">
      ${menuHtml}
    </div>
  `;

  modal.style.display = 'flex';
  document.body.style.overflow = 'hidden';
  
  setTimeout(updateHeartIcons, 100);
}

// ========================
// FAVORITOS
// ========================
function toggleFavorite(id, event) {
  if (event) {
    event.stopPropagation();
  }
  
  // Enviar solicitud al servidor
  fetch(`/toggle_favorite/${id}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    }
  })
  .then(response => response.json())
  .then(data => {
    if (data.error) {
      alert('Error: ' + data.error);
      return;
    }
    
    // Actualizar visualmente
    updateHeartIcons();
    
    if (data.action === 'added') {
      showMessage('Restaurante agregado a favoritos', 'success');
    } else {
      showMessage('Restaurante eliminado de favoritos', 'info');
    }
  })
  .catch(error => {
    console.error('Error:', error);
    alert('Error al actualizar favorito');
  });
}

function updateHeartIcons() {
  // Actualizar corazones en las tarjetas
  const hearts = document.querySelectorAll('.restaurant-card .heart');
  hearts.forEach(heart => {
    const card = heart.closest('.restaurant-card');
    if (card) {
      const idMatch = card.getAttribute('onclick').match(/\d+/);
      if (idMatch) {
        const id = parseInt(idMatch[0]);
        // Aquí normalmente verificaríamos contra el servidor
        // Por ahora simulamos con localStorage
        try {
          const favorites = JSON.parse(localStorage.getItem('favorites')) || [];
          if (favorites.includes(id)) {
            heart.classList.add('active');
          } else {
            heart.classList.remove('active');
          }
        } catch (e) {
          heart.classList.remove('active');
        }
      }
    }
  });
  
  // Actualizar corazón en el modal
  const detailHeart = document.querySelector('#restaurantModal .heart');
  if (detailHeart) {
    const content = document.getElementById('restaurantDetailContent');
    const idMatch = content.innerHTML.match(/toggleFavorite\((\d+)/);
    if (idMatch) {
      const id = parseInt(idMatch[1]);
      try {
        const favorites = JSON.parse(localStorage.getItem('favorites')) || [];
        if (favorites.includes(id)) {
          detailHeart.classList.add('active');
        } else {
          detailHeart.classList.remove('active');
        }
      } catch (e) {
        detailHeart.classList.remove('active');
      }
    }
  }
}

// ========================
// RESERVAS
// ========================
function openReservationModal(restaurantId, restaurantName) {
  // Crear modal de reserva
  const modal = document.createElement('div');
  modal.id = 'reservationModal';
  modal.className = 'modal';
  modal.style.display = 'flex';
  
  modal.innerHTML = `
    <div class="modal-content" style="max-width: 500px;">
      <span class="close" onclick="closeModal('reservationModal')">×</span>
      <h2>Reservar en ${restaurantName}</h2>
      <form id="reservationForm">
        <input type="hidden" name="restaurant_id" value="${restaurantId}">
        <div class="form-group">
          <label class="form-label">Fecha</label>
          <input type="date" name="date" class="form-input" required min="${new Date().toISOString().split('T')[0]}">
        </div>
        <div class="form-group">
          <label class="form-label">Hora</label>
          <select name="time" class="form-input" required>
            <option value="">Selecciona una hora</option>
            <option value="12:00">12:00 PM</option>
            <option value="13:00">1:00 PM</option>
            <option value="14:00">2:00 PM</option>
            <option value="15:00">3:00 PM</option>
            <option value="19:00">7:00 PM</option>
            <option value="20:00">8:00 PM</option>
            <option value="21:00">9:00 PM</option>
            <option value="22:00">10:00 PM</option>
          </select>
        </div>
        <div class="form-group">
          <label class="form-label">Número de personas</label>
          <input type="number" name="guests" class="form-input" min="1" max="20" value="2" required>
        </div>
        <div class="form-group">
          <label class="form-label">Notas especiales (opcional)</label>
          <textarea name="special_requests" class="form-input" rows="3" placeholder="Alguna solicitud especial..."></textarea>
        </div>
        <button type="submit" class="btn btn-primary" style="width: 100%;">Confirmar Reserva</button>
      </form>
    </div>
  `;
  
  document.body.appendChild(modal);
  document.body.style.overflow = 'hidden';
  
  // Manejar el formulario
  const form = document.getElementById('reservationForm');
  form.addEventListener('submit', function(e) {
    e.preventDefault();
    submitReservation(form);
  });
}

function submitReservation(form) {
  const submitBtn = form.querySelector('button[type="submit"]');
  const originalText = submitBtn.innerHTML;
  submitBtn.innerHTML = 'Procesando...';
  submitBtn.disabled = true;
  
  const formData = new FormData(form);
  
  fetch('/reserve', {
    method: 'POST',
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      showMessage(data.message, 'success');
      closeModal('reservationModal');
    } else {
      showMessage('Error: ' + data.error, 'error');
    }
  })
  .catch(error => {
    console.error('Error:', error);
    showMessage('Error al procesar la reserva', 'error');
  })
  .finally(() => {
    submitBtn.innerHTML = originalText;
    submitBtn.disabled = false;
  });
}

// ========================
// PEDIDOS ONLINE
// ========================
function openOrderModal(restaurantId, restaurantName) {
  const restaurante = restaurantesData.find(r => r.id === restaurantId);
  if (!restaurante) return;

  // Crear modal de pedido
  const modal = document.createElement('div');
  modal.id = 'orderModal';
  modal.className = 'modal';
  modal.style.display = 'flex';
  
  // Agrupar menú por categorías
  const menuByCategory = {};
  restaurante.menu.forEach(item => {
    if (!menuByCategory[item.categoria]) {
      menuByCategory[item.categoria] = [];
    }
    menuByCategory[item.categoria].push(item);
  });

  let menuHtml = '';
  for (const [categoria, items] of Object.entries(menuByCategory)) {
    menuHtml += `<h3 style="margin: 1.5rem 0 1rem; color: var(--primary);">${categoria}</h3>`;
    items.forEach(item => {
      menuHtml += `
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.5rem 0; border-bottom: 1px solid var(--border);">
          <div>
            <div style="font-weight: 500;">${item.nombre}</div>
            <div style="font-size: 0.9rem; color: #666;">$${item.precio}</div>
          </div>
          <div style="display: flex; align-items: center; gap: 0.5rem;">
            <button class="btn btn-outline" style="padding: 0.2rem 0.5rem;" onclick="updateQuantity(${item.precio}, -1, ${item.precio})">-</button>
            <span id="qty-${item.precio}" style="min-width: 20px; text-align: center;">0</span>
            <button class="btn btn-outline" style="padding: 0.2rem 0.5rem;" onclick="updateQuantity(${item.precio}, 1, ${item.precio})">+</button>
          </div>
        </div>
      `;
    });
  }

  modal.innerHTML = `
    <div class="modal-content" style="max-width: 600px; max-height: 90vh;">
      <span class="close" onclick="closeModal('orderModal')">×</span>
      <h2>Pedir de ${restaurantName}</h2>
      <div style="margin-bottom: 1rem;">
        <h3 style="color: var(--primary);">Menú</h3>
        <div style="background-color: var(--card-bg); padding: 1rem; border-radius: var(--radius); border: 1px solid var(--border);">
          ${menuHtml}
        </div>
      </div>
      <div style="background-color: var(--card-bg); padding: 1rem; border-radius: var(--radius); border: 1px solid var(--border); margin-top: 1rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
          <h3 style="margin: 0; color: var(--primary);">Total</h3>
          <div style="font-size: 1.5rem; font-weight: bold;">$<span id="orderTotal">0</span></div>
        </div>
        <button class="btn btn-primary" style="width: 100%;" onclick="placeOrder(${restaurantId})">
          Confirmar Pedido - $<span id="confirmTotal">0</span>
        </button>
      </div>
    </div>
  `;
  
  document.body.appendChild(modal);
  document.body.style.overflow = 'hidden';
}

function updateQuantity(itemId, change, price) {
  const qtyElement = document.getElementById(`qty-${itemId}`);
  if (!qtyElement) return;
  
  let currentQty = parseInt(qtyElement.textContent) || 0;
  let newQty = Math.max(0, currentQty + change);
  qtyElement.textContent = newQty;
  
  updateOrderTotal();
}

function updateOrderTotal() {
  let total = 0;
  const qtyElements = document.querySelectorAll('[id^="qty-"]');
  
  qtyElements.forEach(element => {
    const price = parseFloat(element.id.split('-')[1]);
    const qty = parseInt(element.textContent) || 0;
    total += price * qty;
  });
  
  document.getElementById('orderTotal').textContent = total.toFixed(2);
  document.getElementById('confirmTotal').textContent = total.toFixed(2);
}

function placeOrder(restaurantId) {
  const items = [];
  const qtyElements = document.querySelectorAll('[id^="qty-"]');
  
  qtyElements.forEach(element => {
    const qty = parseInt(element.textContent) || 0;
    if (qty > 0) {
      const price = parseFloat(element.id.split('-')[1]);
      items.push({
        id: price, // Usamos precio como ID temporal
        quantity: qty,
        price: price
      });
    }
  });
  
  if (items.length === 0) {
    showMessage('Agrega al menos un producto al pedido', 'error');
    return;
  }
  
  const total = items.reduce((sum, item) => sum + (item.quantity * item.price), 0);
  
  // En producción, esto enviaría los datos al servidor
  showMessage(`Pedido confirmado! Total: $${total.toFixed(2)}`, 'success');
  closeModal('orderModal');
}

// ========================
// FUNCIONES AUXILIARES
// ========================
function showMessage(message, type = 'info') {
  // Crear mensaje flotante
  const messageDiv = document.createElement('div');
  messageDiv.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 1rem 1.5rem;
    border-radius: 0.5rem;
    color: white;
    font-weight: 500;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    z-index: 2000;
    background-color: ${type === 'success' ? '#4caf50' : type === 'error' ? '#d32f2f' : '#1976d2'};
  `;
  messageDiv.textContent = message;
  
  document.body.appendChild(messageDiv);
  
  // Auto-ocultar después de 3 segundos
  setTimeout(() => {
    messageDiv.style.opacity = '0';
    setTimeout(() => messageDiv.remove(), 300);
  }, 3000);
}