// Efeito de fade nos cards ao carregar
window.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.card').forEach(function(card) {
        card.style.opacity = 0;
        card.style.transform = 'translateY(30px)';
        setTimeout(function() {
            card.style.transition = 'opacity 0.7s, transform 0.7s';
            card.style.opacity = 1;
            card.style.transform = 'translateY(0)';
        }, 100);
    });

    // Efeito de foco suave nos inputs
    document.querySelectorAll('input, textarea, select').forEach(function(el) {
        el.addEventListener('focus', function() {
            this.parentElement.classList.add('input-focus');
        });
        el.addEventListener('blur', function() {
            this.parentElement.classList.remove('input-focus');
        });
    });
}); 