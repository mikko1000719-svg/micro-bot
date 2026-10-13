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

                // Show dashboard after successful login
                setTimeout(() => {
                    document.getElementById('loginForm').style.display = 'none';
                    document.getElementById('dashboard').style.display = 'block';
                    document.getElementById('dashboardServerId').textContent = data.guild_id;
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

// Load settings button
const loadSettingsBtn = document.getElementById('loadSettings');
if (loadSettingsBtn) {
    loadSettingsBtn.addEventListener('click', async function() {
        const guildId = document.getElementById('dashboardServerId').textContent;
        const saveMessage = document.getElementById('saveMessage');

        saveMessage.style.display = 'block';
        saveMessage.className = 'save-message';
        saveMessage.textContent = '載入中...';

        try {
            const response = await fetch(`/api/guild/${guildId}`);
            const data = await response.json();

            if (data.success) {
                const config = data.config;
                document.getElementById('antiSpamEnabled').checked = config.anti_spam_enabled;
                document.getElementById('timeWindow').value = config.time_window;
                document.getElementById('maxMessages').value = config.max_messages;
                document.getElementById('muteHours').value = config.mute_hours;

                saveMessage.className = 'save-message success';
                saveMessage.textContent = '✅ 設定載入成功';
            } else {
                saveMessage.className = 'save-message error';
                saveMessage.textContent = '❌ 載入失敗：' + data.message;
            }
        } catch (error) {
            saveMessage.className = 'save-message error';
            saveMessage.textContent = '❌ 載入失敗：無法連接到服務器';
        }
    });
}

// Anti-spam form handling
const antiSpamForm = document.getElementById('antiSpamForm');
if (antiSpamForm) {
    antiSpamForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        const guildId = document.getElementById('dashboardServerId').textContent;
        const saveMessage = document.getElementById('saveMessage');

        const newConfig = {
            anti_spam_enabled: document.getElementById('antiSpamEnabled').checked,
            time_window: parseFloat(document.getElementById('timeWindow').value),
            max_messages: parseInt(document.getElementById('maxMessages').value),
            mute_hours: parseInt(document.getElementById('muteHours').value)
        };

        saveMessage.style.display = 'block';
        saveMessage.className = 'save-message';
        saveMessage.textContent = '保存中...';

        try {
            const response = await fetch(`/api/guild/${guildId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(newConfig)
            });

            const data = await response.json();

            if (data.success) {
                saveMessage.className = 'save-message success';
                saveMessage.textContent = '✅ 設定保存成功';
            } else {
                saveMessage.className = 'save-message error';
                saveMessage.textContent = '❌ 保存失敗：' + data.message;
            }
        } catch (error) {
            saveMessage.className = 'save-message error';
            saveMessage.textContent = '❌ 保存失敗：無法連接到服務器';
        }
    });
}

// User management buttons
document.getElementById('btnBan')?.addEventListener('click', async function() {
    const userId = document.getElementById('userId').value;
    const reason = document.getElementById('actionReason').value;
    const guildId = document.getElementById('dashboardServerId').textContent;
    const actionMessage = document.getElementById('actionMessage');

    if (!userId || !guildId) {
        actionMessage.style.display = 'block';
        actionMessage.className = 'action-message error';
        actionMessage.textContent = '❌ 請輸入用戶 ID';
        return;
    }

    actionMessage.style.display = 'block';
    actionMessage.className = 'action-message';
    actionMessage.textContent = '正在封禁...';

    try {
        const response = await fetch('/api/discord/ban', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                user_id: userId,
                reason: reason,
                guild_id: guildId
            })
        });

        const data = await response.json();

        if (data.success) {
            actionMessage.className = 'action-message success';
            actionMessage.textContent = '✅ ' + data.message;
        } else {
            actionMessage.className = 'action-message error';
            actionMessage.textContent = '❌ ' + data.message;
        }
    } catch (error) {
        actionMessage.className = 'action-message error';
        actionMessage.textContent = '❌ 請求失敗: ' + error.message;
    }
});

document.getElementById('btnKick')?.addEventListener('click', async function() {
    const userId = document.getElementById('userId').value;
    const reason = document.getElementById('actionReason').value;
    const guildId = document.getElementById('dashboardServerId').textContent;
    const actionMessage = document.getElementById('actionMessage');

    if (!userId || !guildId) {
        actionMessage.style.display = 'block';
        actionMessage.className = 'action-message error';
        actionMessage.textContent = '❌ 請輸入用戶 ID';
        return;
    }

    actionMessage.style.display = 'block';
    actionMessage.className = 'action-message';
    actionMessage.textContent = '正在踢出...';

    try {
        const response = await fetch('/api/discord/kick', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                user_id: userId,
                reason: reason,
                guild_id: guildId
            })
        });

        const data = await response.json();

        if (data.success) {
            actionMessage.className = 'action-message success';
            actionMessage.textContent = '✅ ' + data.message;
        } else {
            actionMessage.className = 'action-message error';
            actionMessage.textContent = '❌ ' + data.message;
        }
    } catch (error) {
        actionMessage.className = 'action-message error';
        actionMessage.textContent = '❌ 請求失敗: ' + error.message;
    }
});

document.getElementById('btnMute')?.addEventListener('click', async function() {
    const userId = document.getElementById('userId').value;
    const reason = document.getElementById('actionReason').value;
    const guildId = document.getElementById('dashboardServerId').textContent;
    const actionMessage = document.getElementById('actionMessage');

    if (!userId || !guildId) {
        actionMessage.style.display = 'block';
        actionMessage.className = 'action-message error';
        actionMessage.textContent = '❌ 請輸入用戶 ID';
        return;
    }

    actionMessage.style.display = 'block';
    actionMessage.className = 'action-message';
    actionMessage.textContent = '正在禁言...';

    try {
        const response = await fetch('/api/discord/mute', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                user_id: userId,
                reason: reason,
                guild_id: guildId,
                duration: 3600  // 1 hour
            })
        });

        const data = await response.json();

        if (data.success) {
            actionMessage.className = 'action-message success';
            actionMessage.textContent = '✅ ' + data.message;
        } else {
            actionMessage.className = 'action-message error';
            actionMessage.textContent = '❌ ' + data.message;
        }
    } catch (error) {
        actionMessage.className = 'action-message error';
        actionMessage.textContent = '❌ 請求失敗: ' + error.message;
    }
});

// Whitelist management buttons
document.getElementById('btnAddWhitelist')?.addEventListener('click', async function() {
    const userId = document.getElementById('whitelistUserId').value;
    const reason = document.getElementById('whitelistReason').value;
    const guildId = document.getElementById('dashboardServerId').textContent;
    const whitelistMessage = document.getElementById('whitelistMessage');

    if (!userId || !guildId) {
        whitelistMessage.style.display = 'block';
        whitelistMessage.className = 'action-message error';
        whitelistMessage.textContent = '❌ 請輸入用戶 ID';
        return;
    }

    whitelistMessage.style.display = 'block';
    whitelistMessage.className = 'action-message';
    whitelistMessage.textContent = '正在添加...';

    try {
        const response = await fetch('/api/discord/whitelist_add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                user_id: userId,
                reason: reason,
                guild_id: guildId
            })
        });

        const data = await response.json();

        if (data.success) {
            whitelistMessage.className = 'action-message success';
            whitelistMessage.textContent = '✅ ' + data.message;
        } else {
            whitelistMessage.className = 'action-message error';
            whitelistMessage.textContent = '❌ ' + data.message;
        }
    } catch (error) {
        whitelistMessage.className = 'action-message error';
        whitelistMessage.textContent = '❌ 請求失敗: ' + error.message;
    }
});

document.getElementById('btnRemoveWhitelist')?.addEventListener('click', async function() {
    const userId = document.getElementById('whitelistUserId').value;
    const guildId = document.getElementById('dashboardServerId').textContent;
    const whitelistMessage = document.getElementById('whitelistMessage');

    if (!userId || !guildId) {
        whitelistMessage.style.display = 'block';
        whitelistMessage.className = 'action-message error';
        whitelistMessage.textContent = '❌ 請輸入用戶 ID';
        return;
    }

    whitelistMessage.style.display = 'block';
    whitelistMessage.className = 'action-message';
    whitelistMessage.textContent = '正在移除...';

    try {
        const response = await fetch('/api/discord/whitelist_remove', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                user_id: userId,
                guild_id: guildId
            })
        });

        const data = await response.json();

        if (data.success) {
            whitelistMessage.className = 'action-message success';
            whitelistMessage.textContent = '✅ ' + data.message;
        } else {
            whitelistMessage.className = 'action-message error';
            whitelistMessage.textContent = '❌ ' + data.message;
        }
    } catch (error) {
        whitelistMessage.className = 'action-message error';
        whitelistMessage.textContent = '❌ 請求失敗: ' + error.message;
    }
});

document.getElementById('btnListWhitelist')?.addEventListener('click', async function() {
    const guildId = document.getElementById('dashboardServerId').textContent;
    const whitelistMessage = document.getElementById('whitelistMessage');

    if (!guildId) {
        whitelistMessage.style.display = 'block';
        whitelistMessage.className = 'action-message error';
        whitelistMessage.textContent = '❌ 未登入';
        return;
    }

    whitelistMessage.style.display = 'block';
    whitelistMessage.className = 'action-message';
    whitelistMessage.textContent = '正在載入...';

    try {
        const response = await fetch(`/api/discord/whitelist_list?guild_id=${guildId}`);
        const data = await response.json();

        if (data.success) {
            whitelistMessage.className = 'action-message success';
            whitelistMessage.textContent = '✅ ' + data.message;
        } else {
            whitelistMessage.className = 'action-message error';
            whitelistMessage.textContent = '❌ ' + data.message;
        }
    } catch (error) {
        whitelistMessage.className = 'action-message error';
        whitelistMessage.textContent = '❌ 請求失敗: ' + error.message;
    }
});

// Log viewing button
document.getElementById('btnViewLogs')?.addEventListener('click', async function() {
    const limit = document.getElementById('logLimit').value;
    const guildId = document.getElementById('dashboardServerId').textContent;
    const logMessage = document.getElementById('logMessage');

    if (!guildId) {
        logMessage.style.display = 'block';
        logMessage.className = 'action-message error';
        logMessage.textContent = '❌ 未登入';
        return;
    }

    logMessage.style.display = 'block';
    logMessage.className = 'action-message';
    logMessage.textContent = '正在載入日誌...';

    try {
        const response = await fetch(`/api/discord/logs?guild_id=${guildId}&limit=${limit}`);
        const data = await response.json();

        if (data.success) {
            logMessage.className = 'action-message success';
            logMessage.textContent = '✅ ' + data.message;
        } else {
            logMessage.className = 'action-message error';
            logMessage.textContent = '❌ ' + data.message;
        }
    } catch (error) {
        logMessage.className = 'action-message error';
        logMessage.textContent = '❌ 請求失敗: ' + error.message;
    }
});

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
