// Smooth scrolling for navigation links
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

// Command search functionality
const commandSearch = document.getElementById('commandSearch');
if (commandSearch) {
    commandSearch.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        const commandItems = document.querySelectorAll('.command-item');
        
        commandItems.forEach(item => {
            const commandText = item.textContent.toLowerCase();
            if (commandText.includes(searchTerm)) {
                item.style.display = 'flex';
            } else {
                item.style.display = 'none';
            }
        });
    });
}

// Login form handling
const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        const serverId = document.getElementById('serverId').value;
        const adminCode = document.getElementById('adminCode').value;
        const loginMessage = document.getElementById('loginMessage');

        // Show loading state
        loginMessage.style.display = 'block';
        loginMessage.className = 'login-message';
        loginMessage.textContent = '登入中...';

        try {
            const response = await fetch('/api/admin/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    guild_id: serverId,
                    code: adminCode
                })
            });

            const data = await response.json();

            if (data.success) {
                loginMessage.className = 'login-message success';
                loginMessage.textContent = '✅ ' + data.message;

                // Redirect to dashboard after successful login
                setTimeout(() => {
                    alert('登入成功！\n伺服器 ID: ' + data.guild_id + '\n\n管理面板功能開發中...');
                }, 1000);
            } else {
                loginMessage.className = 'login-message error';
                loginMessage.textContent = '❌ ' + data.message;
            }
        } catch (error) {
            loginMessage.className = 'login-message error';
            loginMessage.textContent = '❌ 登入失敗：無法連接到服務器\n請確保網站已部署到後端服務器';
        }
    });
}

// Add scroll effect to navbar
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.background = 'rgba(10, 14, 39, 0.98)';
    } else {
        navbar.style.background = 'rgba(10, 14, 39, 0.95)';
    }
});

// Add animation on scroll for elements
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe all feature cards
document.querySelectorAll('.feature-card, .info-card, .command-category').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(30px)';
    card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(card);
});

// Particle effect for hero section
function createParticles() {
    const hero = document.querySelector('.hero');
    if (!hero) return;
    
    const particleCount = 50;
    
    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.style.cssText = `
            position: absolute;
            width: ${Math.random() * 4 + 1}px;
            height: ${Math.random() * 4 + 1}px;
            background: rgba(79, 172, 254, ${Math.random() * 0.5 + 0.2});
            border-radius: 50%;
            pointer-events: none;
            left: ${Math.random() * 100}%;
            top: ${Math.random() * 100}%;
            animation: float ${Math.random() * 10 + 10}s infinite ease-in-out;
        `;
        hero.appendChild(particle);
    }
}

// Create particles on load
window.addEventListener('load', createParticles);

// Add hover effect to bot avatar
const botAvatar = document.querySelector('.bot-avatar');
if (botAvatar) {
    botAvatar.addEventListener('mouseenter', function() {
        this.querySelector('.avatar-image').style.animation = 'none';
        this.querySelector('.avatar-image').style.transform = 'scale(1.2)';
    });
    
    botAvatar.addEventListener('mouseleave', function() {
        this.querySelector('.avatar-image').style.animation = 'float 3s infinite ease-in-out';
        this.querySelector('.avatar-image').style.transform = 'scale(1)';
    });
}

// Add typing effect to hero description
const heroDescription = document.querySelector('.hero-description');
if (heroDescription) {
    const text = heroDescription.textContent;
    heroDescription.textContent = '';
    
    let i = 0;
    function typeWriter() {
        if (i < text.length) {
            heroDescription.textContent += text.charAt(i);
            i++;
            setTimeout(typeWriter, 50);
        }
    }
    
    // Start typing after a delay
    setTimeout(typeWriter, 1000);
}

// Add counter animation for stats
function animateCounter(element, target, duration) {
    let start = 0;
    const increment = target / (duration / 16);
    
    function updateCounter() {
        start += increment;
        if (start < target) {
            element.textContent = Math.floor(start);
            requestAnimationFrame(updateCounter);
        } else {
            element.textContent = target;
        }
    }
    
    updateCounter();
}

// Observe elements to animate counters
const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const highlightElements = entry.target.querySelectorAll('.highlight');
            highlightElements.forEach(el => {
                const finalValue = parseInt(el.textContent);
                if (!isNaN(finalValue)) {
                    animateCounter(el, finalValue, 2000);
                }
            });
            counterObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.5 });

document.querySelectorAll('.info-card').forEach(card => {
    counterObserver.observe(card);
});
