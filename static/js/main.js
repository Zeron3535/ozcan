// Ana JavaScript Dosyası

// DOM yüklendikten sonra çalışacak kodlar
document.addEventListener('DOMContentLoaded', function() {
    // Mesajları 5 saniye sonra otomatik kapat
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
    
    // Tooltip'leri aktifleştir
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Mobil menüyü dışarıya tıklayınca kapat
    document.addEventListener('click', function(event) {
        var navbar = document.getElementById('navbarNav');
        var navbarButton = document.querySelector('.navbar-toggler');
        
        if (navbar && navbar.classList.contains('show') && 
            !navbar.contains(event.target) && 
            !navbarButton.contains(event.target)) {
            navbarButton.click();
        }
    });
    
    // Randevu form kontrolleri
    const appointmentForm = document.getElementById('appointment-form');
    if (appointmentForm) {
        appointmentForm.addEventListener('submit', function(event) {
            const phoneInput = document.getElementById('id_customer_phone');
            if (phoneInput && phoneInput.value) {
                // Basit telefon numarası doğrulama
                const phoneRegex = /^[0-9]{10,11}$/;
                if (!phoneRegex.test(phoneInput.value.replace(/\s+/g, ''))) {
                    event.preventDefault();
                    alert('Lütfen geçerli bir telefon numarası girin (10-11 rakam)');
                }
            }
        });
    }
}); 