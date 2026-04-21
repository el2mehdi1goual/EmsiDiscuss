/* ============================================
   EMSI_Discuss - Script Principal
   ============================================ */

// Attendre que le DOM soit chargé
document.addEventListener('DOMContentLoaded', function() {
    console.log('EMSI_Discuss - Application chargée');
    
    // Fermer automatiquement les alertes après 5 secondes
    const alertElements = document.querySelectorAll('.alert');
    alertElements.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            // bsAlert.close(); // Décommentez pour fermer automatiquement
        }, 5000);
    });
    
    // Ajouter des interactions au défilement
    window.addEventListener('scroll', () => {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
});

// Fonction pour afficher les notifications
function showNotification(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.querySelector('main .container').insertBefore(alertDiv, document.querySelector('main .container').firstChild);
}

// Fonction utilitaire pour les requêtes AJAX
function sendAjaxRequest(url, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        }
    };
    
    if (data && method !== 'GET') {
        options.headers['Content-Type'] = 'application/json';
        options.body = JSON.stringify(data);
    }
    
    return fetch(url, options).then(response => response.json());
}

console.log('Scripts EMSI_Discuss chargés avec succès');
