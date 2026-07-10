/* ============================================
   SOLAR PANEL DETECTION — INTERACTIONS & ANIMATIONS
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {
    initNavbar();
    initScrollAnimations();
    initParticles();
    initUploadZone();
});

/* ---------- NAVBAR ---------- */
function initNavbar() {
    const navbar = document.querySelector('.navbar');
    const toggle = document.querySelector('.nav-toggle');
    const links = document.querySelector('.nav-links');

    // Scroll effect
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Mobile toggle
    if (toggle && links) {
        toggle.addEventListener('click', () => {
            links.classList.toggle('open');
            toggle.classList.toggle('active');
        });

        // Close on link click
        links.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                links.classList.remove('open');
                toggle.classList.remove('active');
            });
        });
    }
}

/* ---------- SCROLL ANIMATIONS ---------- */
function initScrollAnimations() {
    const elements = document.querySelectorAll('.animate-on-scroll');

    if (!elements.length) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -40px 0px'
    });

    elements.forEach(el => observer.observe(el));
}

/* ---------- PARTICLES ---------- */
function initParticles() {
    const container = document.querySelector('.particles');
    if (!container) return;

    const count = 20;
    for (let i = 0; i < count; i++) {
        const particle = document.createElement('div');
        particle.classList.add('particle');
        particle.style.left = Math.random() * 100 + '%';
        particle.style.width = (Math.random() * 3 + 2) + 'px';
        particle.style.height = particle.style.width;
        particle.style.animationDuration = (Math.random() * 15 + 10) + 's';
        particle.style.animationDelay = (Math.random() * 10) + 's';
        container.appendChild(particle);
    }
}

/* ---------- UPLOAD ZONE ---------- */
function initUploadZone() {
    const zone = document.querySelector('.upload-zone');
    const input = document.getElementById('imageInput');
    const preview = document.querySelector('.preview-container');
    const previewImg = document.getElementById('previewImage');
    const detectBtnContainer = document.querySelector('.detect-btn-container');
    const detectBtn = document.getElementById('detectBtn');
    const resultContainer = document.querySelector('.result-container');
    const loading = document.querySelector('.loading-overlay');

    if (!zone || !input) return;

    // Drag & drop visual feedback
    ['dragenter', 'dragover'].forEach(evt => {
        zone.addEventListener(evt, (e) => {
            e.preventDefault();
            zone.classList.add('drag-over');
        });
    });

    ['dragleave', 'drop'].forEach(evt => {
        zone.addEventListener(evt, (e) => {
            e.preventDefault();
            zone.classList.remove('drag-over');
        });
    });

    zone.addEventListener('drop', (e) => {
        const files = e.dataTransfer.files;
        if (files.length) {
            input.files = files;
            handleFileSelect(files[0]);
        }
    });

    input.addEventListener('change', (e) => {
        if (e.target.files.length) {
            handleFileSelect(e.target.files[0]);
        }
    });

    function handleFileSelect(file) {
        if (!file.type.startsWith('image/')) {
            showToast('Please upload an image file.', 'error');
            return;
        }

        const reader = new FileReader();
        reader.onload = (e) => {
            previewImg.src = e.target.result;
            preview.classList.add('active');
            detectBtnContainer.classList.add('active');
            resultContainer.classList.remove('active');
        };
        reader.readAsDataURL(file);
    }

    // Detect button
    if (detectBtn) {
        detectBtn.addEventListener('click', async () => {
            const file = input.files[0];
            if (!file) {
                showToast('Please select an image first.', 'error');
                return;
            }

            const formData = new FormData();
            formData.append('image', file);

            loading.classList.add('active');

            try {
                const response = await fetch('/detect', {
                    method: 'POST',
                    body: formData,
                });

                if (!response.ok) {
                    let errorMsg = `Server error (${response.status})`;
                    try {
                        const errData = await response.json();
                        errorMsg = errData.error || errorMsg;
                    } catch (e) {}
                    showToast(errorMsg, 'error');
                    return;
                }

                const data = await response.json();

                if (data.success) {
                    document.getElementById('resultImage').src = data.result_image + '?t=' + Date.now();
                    document.getElementById('panelCount').textContent = data.panel_count;
                    document.getElementById('avgConfidence').textContent = data.avg_confidence + '%';
                    document.getElementById('processingTime').textContent = data.processing_time + 's';
                    resultContainer.classList.add('active');
                    showToast('Detection complete!', 'success');

                    // Scroll to results
                    setTimeout(() => {
                        resultContainer.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    }, 300);
                } else {
                    showToast(data.error || 'Detection failed.', 'error');
                }
            } catch (err) {
                showToast('Network error. Please try again.', 'error');
                console.error(err);
            } finally {
                loading.classList.remove('active');
            }
        });
    }
}

/* ---------- TOAST ---------- */
function showToast(message, type = 'info') {
    // Remove existing
    document.querySelectorAll('.toast').forEach(t => t.remove());

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);

    requestAnimationFrame(() => {
        toast.classList.add('show');
    });

    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 400);
    }, 3500);
}
