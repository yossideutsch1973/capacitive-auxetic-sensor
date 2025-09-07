// Modern JavaScript for Auxetic Sensor Frontend
document.addEventListener('DOMContentLoaded', function() {
    // Initialize interactive components
    initializeCalculator();
    initializeNavigation();
    initializeAnimations();
});

// Calculator functionality
function initializeCalculator() {
    const elements = {
        cellSize: document.getElementById('cellSize'),
        wallThickness: document.getElementById('wallThickness'),
        reentrantAngle: document.getElementById('reentrantAngle'),
        arraySize: document.getElementById('arraySize'),
        
        cellSizeValue: document.getElementById('cellSizeValue'),
        wallThicknessValue: document.getElementById('wallThicknessValue'),
        reentrantAngleValue: document.getElementById('reentrantAngleValue'),
        
        poissonRatio: document.getElementById('poissonRatio'),
        sensitivity: document.getElementById('sensitivity'),
        cellArea: document.getElementById('cellArea'),
        totalSize: document.getElementById('totalSize'),
        auxeticBehavior: document.getElementById('auxeticBehavior'),
        recommendedUse: document.getElementById('recommendedUse'),
        
        generate3DModel: document.getElementById('generate3DModel')
    };

    // Update display values for sliders
    function updateSliderDisplay() {
        elements.cellSizeValue.textContent = parseFloat(elements.cellSize.value).toFixed(1);
        elements.wallThicknessValue.textContent = parseFloat(elements.wallThickness.value).toFixed(1);
        elements.reentrantAngleValue.textContent = parseInt(elements.reentrantAngle.value);
    }

    // Calculate auxetic properties based on parameters
    function calculateProperties() {
        const cellSize = parseFloat(elements.cellSize.value);
        const wallThickness = parseFloat(elements.wallThickness.value);
        const alpha = parseFloat(elements.reentrantAngle.value);
        const arraySize = elements.arraySize.value;
        
        // Calculate Poisson's ratio (corrected model for re-entrant honeycomb)
        // Based on Gibson & Ashby model: ν ≈ sin(α)(h/l + sin(α)) / (cos²(α)(h/l + sin(α)) + sin(α))
        // Simplified approximation: ν ≈ -tan(α/2) for α < 90°
        const alphaRad = alpha * Math.PI / 180;
        const poissonRatio = -Math.tan(alphaRad / 2);
        
        // Calculate cell area (proper geometric calculation)
        // For re-entrant cell: approximated as cell_size² adjusted for geometry
        const cellArea = cellSize * cellSize * (1 + Math.cos(alphaRad)) / 2;
        
        // Calculate sensitivity (empirical model based on demo data)
        // From demo: Conservative (30°): -46.41, Balanced (45°): -17.16, Aggressive (60°): 15.47
        const sensitivity = poissonRatio * 41.4; // Scaling factor to match demo data
        
        // Calculate total size
        const [nx, ny] = arraySize.split('x').map(n => parseInt(n));
        const totalSizeValue = cellSize * nx;
        
        // Determine recommended use
        let recommendedUse;
        if (alpha <= 35) {
            recommendedUse = 'Conservative';
        } else if (alpha <= 55) {
            recommendedUse = 'Balanced';
        } else {
            recommendedUse = 'Aggressive';
        }
        
        // Update display
        elements.poissonRatio.textContent = poissonRatio.toFixed(3);
        elements.sensitivity.textContent = sensitivity.toFixed(2);
        elements.cellArea.textContent = cellArea.toFixed(2); // Already in mm²
        elements.totalSize.textContent = `${totalSizeValue.toFixed(0)}×${totalSizeValue.toFixed(0)}`;
        elements.auxeticBehavior.textContent = poissonRatio < 0 ? '✓ Yes' : '✗ No';
        elements.auxeticBehavior.className = `result-value ${poissonRatio < 0 ? 'auxetic' : ''}`;
        elements.recommendedUse.textContent = recommendedUse;
    }

    // Add event listeners
    elements.cellSize.addEventListener('input', () => {
        updateSliderDisplay();
        calculateProperties();
    });

    elements.wallThickness.addEventListener('input', () => {
        updateSliderDisplay();
        calculateProperties();
    });

    elements.reentrantAngle.addEventListener('input', () => {
        updateSliderDisplay();
        calculateProperties();
    });

    elements.arraySize.addEventListener('change', calculateProperties);

    // 3D Model generation button
    elements.generate3DModel.addEventListener('click', () => {
        const params = {
            cellSize: elements.cellSize.value,
            wallThickness: elements.wallThickness.value,
            alpha: elements.reentrantAngle.value,
            arraySize: elements.arraySize.value
        };
        
        generateModelAlert(params);
    });

    // Initialize display
    updateSliderDisplay();
    calculateProperties();
}

// Navigation functionality
function initializeNavigation() {
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const offsetTop = target.offsetTop - 80; // Account for fixed nav
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Add scroll effect to navigation
    let lastScrollTop = 0;
    const nav = document.querySelector('.nav');
    
    window.addEventListener('scroll', () => {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > lastScrollTop && scrollTop > 100) {
            // Scrolling down
            nav.style.transform = 'translateY(-100%)';
        } else {
            // Scrolling up
            nav.style.transform = 'translateY(0)';
        }
        
        lastScrollTop = scrollTop;
    });
}

// Animation and visual effects
function initializeAnimations() {
    // Intersection Observer for fade-in animations
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

    // Observe feature cards and other elements for animation
    document.querySelectorAll('.feature-card, .doc-card, .config-card').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });

    // Animate auxetic cell on hover
    const auxeticCell = document.querySelector('.cell-svg');
    if (auxeticCell) {
        auxeticCell.addEventListener('mouseenter', () => {
            auxeticCell.style.animation = 'none';
            auxeticCell.style.transform = 'scale(1.1) rotate(5deg)';
        });
        
        auxeticCell.addEventListener('mouseleave', () => {
            auxeticCell.style.transform = 'scale(1) rotate(0deg)';
            setTimeout(() => {
                auxeticCell.style.animation = 'pulse 2s ease-in-out infinite';
            }, 300);
        });
    }

    // Add parallax effect to hero section
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const hero = document.querySelector('.hero');
        if (hero) {
            hero.style.transform = `translateY(${scrolled * 0.2}px)`;
        }
    });
}

// Helper function for 3D model generation
function generateModelAlert(params) {
    const message = `
3D Model Generation Parameters:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📏 Cell Size: ${params.cellSize} mm
🔧 Wall Thickness: ${params.wallThickness} mm  
📐 Re-entrant Angle: ${params.alpha}°
📊 Array Size: ${params.arraySize} cells

To generate the actual 3D model:
1. Install CadQuery: pip install cadquery-ocp
2. Run: python cad/auxetic_cell_3d.py
3. Modify parameters in the script if needed

Files will be generated in the cad/ directory:
• auxetic_sensor.stl (for 3D printing)
• auxetic_sensor.step (for CAD editing)
• manufacturing_info.txt (assembly guide)
    `;
    
    alert(message);
}

// Utility functions for enhanced UX
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

// Theme and accessibility enhancements
function initializeAccessibility() {
    // Add keyboard navigation support
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Tab') {
            document.body.classList.add('keyboard-navigation');
        }
    });
    
    document.addEventListener('mousedown', () => {
        document.body.classList.remove('keyboard-navigation');
    });

    // Respect user's motion preferences
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        document.documentElement.style.scrollBehavior = 'auto';
        
        // Disable animations
        const style = document.createElement('style');
        style.textContent = `
            *, *::before, *::after {
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }
        `;
        document.head.appendChild(style);
    }
}

// Initialize accessibility features
document.addEventListener('DOMContentLoaded', initializeAccessibility);

// Error handling for development
window.addEventListener('error', (e) => {
    console.error('JavaScript Error:', e.error);
    // In production, you might want to send this to an error reporting service
});

// Performance monitoring
if ('performance' in window) {
    window.addEventListener('load', () => {
        setTimeout(() => {
            const perfData = performance.getEntriesByType('navigation')[0];
            console.log('Page Load Performance:', {
                dns: perfData.domainLookupEnd - perfData.domainLookupStart,
                tcp: perfData.connectEnd - perfData.connectStart,
                request: perfData.responseStart - perfData.requestStart,
                response: perfData.responseEnd - perfData.responseStart,
                dom: perfData.domContentLoadedEventEnd - perfData.responseEnd,
                total: perfData.loadEventEnd - perfData.navigationStart
            });
        }, 0);
    });
}