// Navigation mobile
        const burger = document.querySelector('.burger');
        const navMenu = document.querySelector('.nav-menu');

        burger.addEventListener('click', () => {
            burger.classList.toggle('active');
            navMenu.classList.toggle('active');
        });

        // Fermeture du menu mobile lors du clic sur un lien
        document.querySelectorAll('.nav-menu a').forEach(link => {
            link.addEventListener('click', () => {
                burger.classList.remove('active');
                navMenu.classList.remove('active');
            });
        });

        // Smooth scrolling pour les liens de navigation
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });


        // Animation au scroll
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                }
            });
        }, observerOptions);

        // Observer tous les éléments avec la classe fade-in
        document.querySelectorAll('.fade-in').forEach(el => {
            observer.observe(el);
        });

        // Observer les éléments de timeline
        document.querySelectorAll('.timeline-item').forEach(el => {
            observer.observe(el);
        });

        // Validation du formulaire d'inscription
        const registrationForm = document.getElementById('registrationForm');
        
        // Fonction de validation email
        function isValidEmail(email) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return emailRegex.test(email);
        }

        // Fonction de validation téléphone
        function isValidPhone(phone) {
            const phoneRegex = /^[+]?[\d\s\-\(\)]{8,}$/;
            return phoneRegex.test(phone.trim());
        }

        // Fonction pour afficher les erreurs
        function showError(fieldId, message) {
            const errorElement = document.getElementById(fieldId + '-error');
            const field = document.getElementById(fieldId);
            
            errorElement.textContent = message;
            errorElement.style.display = 'block';
            field.style.borderColor = '#ff6b6b';
        }

        // Fonction pour masquer les erreurs
        function hideError(fieldId) {
            const errorElement = document.getElementById(fieldId + '-error');
            const field = document.getElementById(fieldId);
            
            errorElement.style.display = 'none';
            field.style.borderColor = 'transparent';
        }

        // Validation en temps réel
        ['nom', 'email', 'telephone'].forEach(fieldId => {
            const field = document.getElementById(fieldId);
            
            field.addEventListener('input', () => {
                hideError(fieldId);
            });

            field.addEventListener('blur', () => {
                validateField(fieldId);
            });
        });

        function validateField(fieldId) {
            const field = document.getElementById(fieldId);
            const value = field.value.trim();

            switch(fieldId) {
                case 'nom':
                    if (!value || value.length < 2) {
                        showError(fieldId, 'Le nom doit contenir au moins 2 caractères');
                        return false;
                    }
                    break;

                case 'email':
                    if (!value) {
                        showError(fieldId, 'L\'adresse email est requise');
                        return false;
                    }
                    if (!isValidEmail(value)) {
                        showError(fieldId, 'Veuillez saisir une adresse email valide');
                        return false;
                    }
                    break;

                case 'telephone':
                    if (!value) {
                        showError(fieldId, 'Le numéro de téléphone est requis');
                        return false;
                    }
                    if (!isValidPhone(value)) {
                        showError(fieldId, 'Veuillez saisir un numéro de téléphone valide');
                        return false;
                    }
                    break;
            }

            hideError(fieldId);
            return true;
        }

        // Soumission du formulaire
        registrationForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            // Validation de tous les champs obligatoires
            let isValid = true;
            
            ['nom', 'email', 'telephone'].forEach(fieldId => {
                if (!validateField(fieldId)) {
                    isValid = false;
                }
            });

            if (isValid) {
                // Simulation de l'envoi du formulaire
                const submitBtn = document.querySelector('.btn-submit');
                const originalText = submitBtn.textContent;
                
                submitBtn.textContent = 'Inscription en cours...';
                submitBtn.disabled = true;
                
                setTimeout(() => {
                    alert('🎉 Inscription réussie ! Nous vous contacterons bientôt avec les détails du hackathon.');
                    registrationForm.reset();
                    submitBtn.textContent = originalText;
                    submitBtn.disabled = false;
                }, 2000);
            } else {
                // Scroll vers le premier champ avec erreur
                const firstError = document.querySelector('.error-message[style*="block"]');
                if (firstError) {
                    const field = firstError.previousElementSibling;
                    field.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    field.focus();
                }
            }
        });

        // Header transparent/opaque au scroll
        window.addEventListener('scroll', () => {
            const header = document.querySelector('header');
            if (window.scrollY > 100) {
                header.style.background = 'rgba(255, 255, 255, 0.98)';
                header.style.boxShadow = '0 2px 30px rgba(0, 102, 204, 0.15)';
            } else {
                header.style.background = 'rgba(255, 255, 255, 0.95)';
                header.style.boxShadow = '0 2px 20px rgba(0, 102, 204, 0.1)';
            }
        });

        // Animation des compteurs (optionnel - pour les statistiques)
        function animateCounters() {
            const counters = document.querySelectorAll('.countdown-number');
            
            counters.forEach(counter => {
                const updateCounter = () => {
                    const target = parseInt(counter.textContent);
                    const increment = target / 100;
                    let current = 0;
                    
                    const timer = setInterval(() => {
                        current += increment;
                        if (current >= target) {
                            counter.textContent = target.toString().padStart(2, '0');
                            clearInterval(timer);
                        } else {
                            counter.textContent = Math.floor(current).toString().padStart(2, '0');
                        }
                    }, 20);
                };
            });
        }

        // Effet parallaxe léger pour la section hero
        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;
            const parallaxElements = document.querySelectorAll('.hero::before');
            
            parallaxElements.forEach(element => {
                const speed = 0.5;
                element.style.transform = `translateY(${scrolled * speed}px)`;
            });
        });

        // Préchargement des images et optimisation des performances
        window.addEventListener('load', () => {
            // Lazy loading pour les images (si vous ajoutez des images plus tard)
            const images = document.querySelectorAll('img[data-src]');
            
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.classList.remove('lazy');
                        imageObserver.unobserve(img);
                    }
                });
            });

            images.forEach(img => imageObserver.observe(img));
        });

        // Gestion des erreurs JavaScript
        window.addEventListener('error', (e) => {
            console.error('Erreur JavaScript:', e.error);
            // En production, vous pourriez envoyer ces erreurs à un service de monitoring
        });

        // Performance: Debounce pour les événements de scroll
        function debounce(func, wait) {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        }

        // Application du debounce au scroll
        const debouncedScroll = debounce(() => {
            // Logique de scroll optimisée
        }, 10);

        window.addEventListener('scroll', debouncedScroll);

        // Accessibilité: gestion du focus pour la navigation clavier
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                // Fermer le menu mobile avec Escape
                if (navMenu.classList.contains('active')) {
                    burger.classList.remove('active');
                    navMenu.classList.remove('active');
                }
            }
        });

        // Focus trap pour le menu mobile
        function trapFocus(element) {
            const focusableElements = element.querySelectorAll('a, button, input, textarea, select, [tabindex]:not([tabindex="-1"])');
            const firstElement = focusableElements[0];
            const lastElement = focusableElements[focusableElements.length - 1];

            element.addEventListener('keydown', (e) => {
                if (e.key === 'Tab') {
                    if (e.shiftKey) {
                        if (document.activeElement === firstElement) {
                            e.preventDefault();
                            lastElement.focus();
                        }
                    } else {
                        if (document.activeElement === lastElement) {
                            e.preventDefault();
                            firstElement.focus();
                        }
                    }
                }
            });
        }

        // Initialisation
        document.addEventListener('DOMContentLoaded', () => {
            // Vérifier si toutes les fonctionnalités sont supportées
            if (!window.IntersectionObserver) {
                // Fallback pour les navigateurs non compatibles
                document.querySelectorAll('.fade-in, .timeline-item').forEach(el => {
                    el.classList.add('visible');
                });
            }

            // Initialisation des tooltips ou autres fonctionnalités
            console.log('🎉 Site Hackathon ONEA 2025 chargé avec succès !');
        });