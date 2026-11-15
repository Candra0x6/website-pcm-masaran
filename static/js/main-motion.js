/**
 * PCM Masaran — Awwwards-Tier Motion Design System
 * Inspired by Waabi Design Architecture & Apple Motion Guidelines
 * Integrates Lenis Smooth Scroll, GSAP 3, ScrollTrigger, Parallax & Micro-interactions
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Accessibility: Check for reduced motion preference
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // 2. Register GSAP Plugins
    if (typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined') {
        gsap.registerPlugin(ScrollTrigger);
    }

    // 3. Initialize Lenis Smooth Scrolling (Only if reduced-motion is not requested)
    let lenis = null;
    if (!prefersReducedMotion && typeof Lenis !== 'undefined') {
        try {
            lenis = new Lenis({
                duration: 1.2,
                easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
                orientation: 'vertical',
                gestureOrientation: 'vertical',
                smoothWheel: true,
                wheelMultiplier: 1.0,
                touchMultiplier: 1.5,
                infinite: false,
            });

            // Synchronize Lenis with GSAP ScrollTrigger
            lenis.on('scroll', ScrollTrigger.update);

            gsap.ticker.add((time) => {
                lenis.raf(time * 1000);
            });
            gsap.ticker.lagSmoothing(0);

            // Expose globally for smooth anchors
            window.lenis = lenis;
        } catch (e) {
            console.warn('Lenis smooth scroll could not be initialized:', e);
        }
    }

    // 4. Back-To-Top and Circular Scroll Progress Tracker
    const progressContainer = document.getElementById('scroll-progress-widget');
    const progressCircle = document.getElementById('scroll-progress-circle');

    if (progressContainer && progressCircle) {
        const radius = progressCircle.r.baseVal.value;
        const circumference = 2 * Math.PI * radius;
        progressCircle.style.strokeDasharray = `${circumference} ${circumference}`;
        progressCircle.style.strokeDashoffset = circumference;

        window.addEventListener('scroll', () => {
            const scrollTop = window.scrollY || document.documentElement.scrollTop;
            const scrollHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const progress = scrollHeight > 0 ? scrollTop / scrollHeight : 0;
            const offset = circumference - (progress * circumference);
            progressCircle.style.strokeDashoffset = offset;

            if (scrollTop > 350) {
                progressContainer.classList.remove('opacity-0', 'pointer-events-none', 'translate-y-4');
                progressContainer.classList.add('opacity-100', 'pointer-events-auto', 'translate-y-0');
            } else {
                progressContainer.classList.add('opacity-0', 'pointer-events-none', 'translate-y-4');
                progressContainer.classList.remove('opacity-100', 'pointer-events-auto', 'translate-y-0');
            }
        }, { passive: true });

        progressContainer.addEventListener('click', () => {
            if (lenis) {
                lenis.scrollTo(0, { duration: 1.2 });
            } else {
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }
        });
    }

    // If reduced motion is requested, stop here to avoid aggressive animations
    if (prefersReducedMotion || typeof gsap === 'undefined') {
        // Immediate display for counters
        document.querySelectorAll('.counter-val').forEach(el => {
            const target = el.getAttribute('data-target');
            if (target) el.textContent = target;
        });
        return;
    }

    // 5. Hero Entry Animation & Parallax Scrub
    const heroSection = document.querySelector('.hero-section');
    const heroBgImg = document.querySelector('.hero-bg-img');

    if (heroSection) {
        // Hero Content Entrance Timeline
        const heroTl = gsap.timeline({ defaults: { ease: "power3.out" } });

        heroTl.from('.hero-badge-item', {
            y: -20,
            opacity: 0,
            duration: 0.7,
            stagger: 0.1,
            delay: 0.1
        })
        .from('.hero-headline', {
            y: 40,
            opacity: 0,
            filter: 'blur(8px)',
            duration: 0.9,
        }, "-=0.4")
        .from('.hero-subtext', {
            y: 25,
            opacity: 0,
            duration: 0.8,
        }, "-=0.6")
        .from('.hero-cta-btn', {
            y: 20,
            opacity: 0,
            scale: 0.95,
            stagger: 0.12,
            duration: 0.6,
        }, "-=0.5")
        .from('.hero-stat-card', {
            y: 30,
            opacity: 0,
            stagger: 0.1,
            duration: 0.7,
            onComplete: initHeroCounters
        }, "-=0.4");

        // Hero Background Parallax on Scroll
        if (heroBgImg) {
            gsap.to(heroBgImg, {
                yPercent: 18,
                scale: 1.12,
                ease: "none",
                scrollTrigger: {
                    trigger: heroSection,
                    start: "top top",
                    end: "bottom top",
                    scrub: 0.8
                }
            });
        }
    } else {
        initHeroCounters();
    }

    // 6. Rolling Number Counter Function
    function initHeroCounters() {
        document.querySelectorAll('.counter-val').forEach(el => {
            const rawTarget = el.getAttribute('data-target');
            if (!rawTarget) return;

            // Clean number and determine if has plus or formatting
            const isFormatted = rawTarget.includes('.');
            const numericValue = parseInt(rawTarget.replace(/\D/g, ''), 10);
            if (isNaN(numericValue)) return;

            const counterObj = { val: 0 };
            gsap.to(counterObj, {
                val: numericValue,
                duration: 2.0,
                ease: "power2.out",
                scrollTrigger: {
                    trigger: el,
                    start: "top 90%",
                    once: true
                },
                onUpdate: () => {
                    const currentInt = Math.floor(counterObj.val);
                    if (isFormatted && numericValue >= 1000) {
                        el.textContent = currentInt.toLocaleString('id-ID');
                    } else {
                        el.textContent = currentInt.toString();
                    }
                },
                onComplete: () => {
                    el.textContent = rawTarget;
                }
            });
        });
    }

    // 7. Pinned Scroll Showcase ("Empat Pilar Masaran")
    const dioramaContainer = document.querySelector('.diorama-scroll-wrapper');
    const dioramaCards = document.querySelectorAll('.diorama-card');
    const dioramaSteps = document.querySelectorAll('.diorama-step-item');

    if (dioramaContainer && dioramaCards.length > 0) {
        dioramaCards.forEach((card, index) => {
            // Card scroll reveal and stacking scale
            if (index < dioramaCards.length - 1) {
                gsap.to(card, {
                    scale: 0.94,
                    opacity: 0.45,
                    filter: "blur(2px)",
                    scrollTrigger: {
                        trigger: dioramaCards[index + 1],
                        start: "top 60%",
                        end: "top 25%",
                        scrub: true,
                    }
                });
            }

            // Update Left Sticky Step Indicators
            ScrollTrigger.create({
                trigger: card,
                start: "top 50%",
                end: "bottom 50%",
                onEnter: () => activateStep(index),
                onEnterBack: () => activateStep(index),
            });
        });

        function activateStep(idx) {
            dioramaSteps.forEach((step, sIdx) => {
                if (sIdx === idx) {
                    step.classList.add('bg-brand-800', 'text-white', 'border-brand-800', 'shadow-md', 'scale-105');
                    step.classList.remove('bg-neutral-100', 'text-neutral-600', 'border-neutral-200');
                    const bar = step.querySelector('.step-bar');
                    if (bar) bar.style.width = '100%';
                } else if (sIdx < idx) {
                    step.classList.remove('bg-brand-800', 'text-white', 'border-brand-800', 'scale-105');
                    step.classList.add('bg-neutral-200/80', 'text-neutral-700', 'border-neutral-300');
                    const bar = step.querySelector('.step-bar');
                    if (bar) bar.style.width = '100%';
                } else {
                    step.classList.remove('bg-brand-800', 'text-white', 'border-brand-800', 'scale-105', 'bg-neutral-200/80', 'text-neutral-700');
                    step.classList.add('bg-neutral-100', 'text-neutral-600', 'border-neutral-200');
                    const bar = step.querySelector('.step-bar');
                    if (bar) bar.style.width = '0%';
                }
            });
        }
    }

    // 8. Staggered Entrance for Grids (News, Agenda, Ranting, AUM)
    document.querySelectorAll('.animate-stagger-grid').forEach(grid => {
        const items = grid.children;
        if (items.length > 0) {
            gsap.from(items, {
                y: 35,
                opacity: 0,
                duration: 0.75,
                stagger: 0.1,
                ease: "power2.out",
                scrollTrigger: {
                    trigger: grid,
                    start: "top 85%",
                    once: true
                }
            });
        }
    });

    // 9. Interactive 3D Card Tilt on Hover (.card-tilt)
    document.querySelectorAll('.card-tilt').forEach(card => {
        let isHovered = false;

        card.addEventListener('mouseenter', () => {
            isHovered = true;
            card.style.transition = 'transform 0.15s ease-out, box-shadow 0.25s ease-out';
        });

        card.addEventListener('mousemove', (e) => {
            if (!isHovered) return;
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left - (rect.width / 2);
            const y = e.clientY - rect.top - (rect.height / 2);
            
            // Limit tilt angle to subtle 6 degrees
            const rotateX = -(y / rect.height) * 8;
            const rotateY = (x / rect.width) * 8;

            card.style.transform = `perspective(1000px) rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg) translateY(-4px)`;
        });

        card.addEventListener('mouseleave', () => {
            isHovered = false;
            card.style.transition = 'transform 0.5s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.4s ease-out';
            card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0px)';
        });
    });

    // 10. Magnetic Micro-Interaction for Primary Buttons (.btn-magnetic)
    document.querySelectorAll('.btn-magnetic').forEach(btn => {
        btn.addEventListener('mousemove', (e) => {
            const rect = btn.getBoundingClientRect();
            const relX = e.clientX - rect.left - (rect.width / 2);
            const relY = e.clientY - rect.top - (rect.height / 2);

            gsap.to(btn, {
                x: relX * 0.28,
                y: relY * 0.28,
                duration: 0.3,
                ease: "power2.out"
            });
        });

        btn.addEventListener('mouseleave', () => {
            gsap.to(btn, {
                x: 0,
                y: 0,
                duration: 0.6,
                ease: "elastic.out(1.1, 0.4)"
            });
        });
    });

    // 11. Subtle Float Micro-Animation for Decorative Watermarks
    gsap.to('.ambient-float', {
        y: -12,
        duration: 3.5,
        repeat: -1,
        yoyo: true,
        ease: "sine.inOut"
    });
});
