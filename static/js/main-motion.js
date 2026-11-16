document.addEventListener('DOMContentLoaded', () => {
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined') {
        gsap.registerPlugin(ScrollTrigger);
    }

    let lenis = null;
    if (!prefersReducedMotion && typeof Lenis !== 'undefined') {
        try {
            lenis = new Lenis({
                duration: 1.2,
                easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
                orientation: 'vertical',
                gestureOrientation: 'vertical',
                smoothWheel: true,
                wheelMultiplier: 0.95,
                touchMultiplier: 1.5,
                infinite: false,
                lerp: 0.1,
            });

            lenis.on('scroll', ScrollTrigger.update);

            gsap.ticker.add((time) => {
                lenis.raf(time * 1000);
            });
            gsap.ticker.lagSmoothing(0);

            window.lenis = lenis;
        } catch (e) {
            console.warn('Lenis smooth scroll could not be initialized:', e);
        }
    }

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

    function initHeroCounters() {
        document.querySelectorAll('.counter-val').forEach(el => {
            const rawTarget = el.getAttribute('data-target') || el.textContent;
            if (!rawTarget) return;

            const isFormatted = rawTarget.includes('.');
            const numericValue = parseInt(rawTarget.replace(/\D/g, ''), 10);
            if (isNaN(numericValue) || numericValue === 0) return;

            if (typeof gsap !== 'undefined' && !prefersReducedMotion) {
                const counterObj = { val: 0 };
                gsap.to(counterObj, {
                    val: numericValue,
                    duration: 1.8,
                    ease: "power2.out",
                    scrollTrigger: {
                        trigger: el,
                        start: "top 95%",
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
            } else {
                el.textContent = rawTarget;
            }
        });
    }

    initHeroCounters();

    if (prefersReducedMotion || typeof gsap === 'undefined') {
        return;
    }

    const heroSection = document.querySelector('.hero-section');
    const heroBgImg = document.querySelector('.hero-bg-img');

    if (heroSection) {
        gsap.fromTo('.hero-headline', 
            { y: 25 }, 
            { y: 0, duration: 0.8, ease: "power3.out", clearProps: "all" }
        );
        gsap.fromTo('.hero-subtext', 
            { y: 15 }, 
            { y: 0, duration: 0.8, delay: 0.1, ease: "power3.out", clearProps: "all" }
        );
        gsap.fromTo('.hero-cta-btn', 
            { y: 15 }, 
            { y: 0, duration: 0.6, delay: 0.2, stagger: 0.1, ease: "power2.out", clearProps: "all" }
        );
        gsap.fromTo('.hero-stat-card', 
            { y: 20 }, 
            { y: 0, duration: 0.6, delay: 0.3, stagger: 0.1, ease: "power2.out", clearProps: "all" }
        );

        if (heroBgImg && typeof ScrollTrigger !== 'undefined') {
            gsap.to(heroBgImg, {
                yPercent: 12,
                ease: "none",
                scrollTrigger: {
                    trigger: heroSection,
                    start: "top top",
                    end: "bottom top",
                    scrub: 0.6
                }
            });
        }
    }

    const dioramaContainer = document.querySelector('.diorama-scroll-wrapper');
    const dioramaCards = document.querySelectorAll('.diorama-card');
    const dioramaSteps = document.querySelectorAll('.diorama-step-item');

    if (dioramaContainer && dioramaCards.length > 0 && typeof ScrollTrigger !== 'undefined') {
        dioramaCards.forEach((card, index) => {
            ScrollTrigger.create({
                trigger: card,
                start: "top 55%",
                end: "bottom 55%",
                onEnter: () => activateStep(index),
                onEnterBack: () => activateStep(index),
            });
        });

        function activateStep(idx) {
            dioramaSteps.forEach((step, sIdx) => {
                if (sIdx === idx) {
                    step.classList.add('bg-brand-800', 'text-white', 'border-brand-800', 'shadow-md', 'scale-105');
                    step.classList.remove('bg-neutral-100', 'text-neutral-600', 'border-neutral-200', 'bg-neutral-200/80', 'text-neutral-700');
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

    document.querySelectorAll('.card-tilt').forEach(card => {
        let isHovered = false;

        card.addEventListener('mouseenter', () => {
            isHovered = true;
            card.style.willChange = 'transform';
            card.style.transition = 'transform 0.12s ease-out, box-shadow 0.25s ease-out';
        });

        card.addEventListener('mousemove', (e) => {
            if (!isHovered) return;
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left - (rect.width / 2);
            const y = e.clientY - rect.top - (rect.height / 2);
            
            const rotateX = -(y / rect.height) * 7.5;
            const rotateY = (x / rect.width) * 7.5;

            card.style.transform = `perspective(1000px) rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg) translateY(-5px)`;
        });

        card.addEventListener('mouseleave', () => {
            isHovered = false;
            card.style.transition = 'transform 0.5s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.3s ease-out';
            card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0px)';
        });
    });

    document.querySelectorAll('.btn-magnetic').forEach(btn => {
        btn.addEventListener('mousemove', (e) => {
            const rect = btn.getBoundingClientRect();
            const relX = e.clientX - rect.left - (rect.width / 2);
            const relY = e.clientY - rect.top - (rect.height / 2);

            gsap.to(btn, {
                x: relX * 0.25,
                y: relY * 0.25,
                duration: 0.3,
                ease: "power2.out"
            });
        });

        btn.addEventListener('mouseleave', () => {
            gsap.to(btn, {
                x: 0,
                y: 0,
                duration: 0.5,
                ease: "elastic.out(1.1, 0.4)"
            });
        });
    });

    gsap.to('.ambient-float', {
        y: -10,
        duration: 3.5,
        repeat: -1,
        yoyo: true,
        ease: "sine.inOut"
    });

    window.addEventListener('load', () => {
        if (typeof ScrollTrigger !== 'undefined') {
            ScrollTrigger.refresh();
        }
    });
});