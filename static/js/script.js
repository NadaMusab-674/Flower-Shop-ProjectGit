// Mobile menu toggle
document.addEventListener('DOMContentLoaded', function () {
    const menuBtn = document.getElementById('menu-btn');
    const navbar  = document.getElementById('navbar');

    if (menuBtn && navbar) {
        menuBtn.addEventListener('click', function () {
            navbar.classList.toggle('active');
            menuBtn.classList.toggle('active');
            const icon = menuBtn.querySelector('i');
            if (icon.classList.contains('fa-bars')) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-times');
            } else {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        });
    }

    // close menu when clicking a link
    const navLinks = document.querySelectorAll('#navbar a');
    navLinks.forEach(link => {
        link.addEventListener('click', function () {
            if (navbar) {
                navbar.classList.remove('active');
                if (menuBtn) {
                    menuBtn.classList.remove('active');
                    const icon = menuBtn.querySelector('i');
                    if (icon) {
                        icon.classList.remove('fa-times');
                        icon.classList.add('fa-bars');
                    }
                }
            }
        });
    });

    // ----- AJAX: التحقق من اسم المستخدم أثناء التسجيل -----
    const usernameField = document.getElementById('id_username');
    const feedback = document.getElementById('username-feedback');

    if (usernameField && feedback) {
        usernameField.addEventListener('keyup', function () {
            const username = this.value.trim();

            if (username.length === 0) {
                feedback.textContent = '';
                return;
            }
        
            if (username.length < 3) {
                feedback.textContent = '❌ Must be at least 3 characters';
                feedback.style.color = 'red';
                return;
            }
            
            fetch(`/accounts/check-username/?username=${encodeURIComponent(username)}`)
                .then(response => response.json())
                .then(data => {
                    if (data.exists) {
                        feedback.textContent = '❌ Username not available';
                        feedback.style.color = 'red';
                    } else {
                        feedback.textContent = '✅ Username available';
                        feedback.style.color = 'green';
                    }
                })
                .catch(error => {
                    feedback.textContent = '⚠️ Connection error';
                    feedback.style.color = 'orange';
                });
        });
    }

    // ----- Cart & Wishlist AJAX -----
    function getCSRFToken() {
        let cookies = document.cookie.split(';');
        for (let c of cookies) {
            c = c.trim();
            if (c.startsWith('csrftoken=')) return c.substring('csrftoken='.length);
        }
        return '';
    }

    // Add to cart
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('add-to-cart')) {
            e.preventDefault();
            const productId = e.target.dataset.productId;
            fetch(`/cart/add/${productId}/`, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCSRFToken(),
                },
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    const badge = document.getElementById('cart-count');
                    if (badge) {
                        badge.textContent = data.cart_count;
                        badge.style.display = 'inline';
                    }
                }
            });
        }
    });

    // Wishlist toggle (heart icon & remove button)
    document.body.addEventListener('click', function(e) {
        if (e.target.classList.contains('heart-icon')) {
            e.preventDefault();
            const heart = e.target;
            const productId = heart.dataset.productId;
            fetch(`/cart/wishlist/toggle/${productId}/`, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCSRFToken(),
                },
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    if (data.liked) {
                        heart.classList.add('fas', 'liked');
                        heart.classList.remove('far');
                    } else {
                        heart.classList.add('far');
                        heart.classList.remove('fas', 'liked');
                    }
                }
            });
        }

        if (e.target.classList.contains('remove-from-wishlist')) {
            e.preventDefault();
            const productId = e.target.dataset.productId;
            fetch(`/cart/wishlist/toggle/${productId}/`, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCSRFToken(),
                },
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                }
            });
        }
    });

    // ---- Account Dropdown ----
    const accountBtn = document.getElementById('account-btn');
    const accountDropdown = document.getElementById('account-dropdown');

    if (accountBtn && accountDropdown) {
        accountBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            accountDropdown.classList.toggle('show');
        });

        window.addEventListener('click', function() {
            accountDropdown.classList.remove('show');
        });

        accountDropdown.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    }
});