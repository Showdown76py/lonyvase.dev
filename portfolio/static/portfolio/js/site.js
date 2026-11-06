(() => {
    const root = document.documentElement;

    function setTheme(theme) {
        root.dataset.theme = theme;
        document.cookie = `theme=${theme}; path=/; max-age=31536000; samesite=lax`;
        document.dispatchEvent(new Event('themechange'));
    }

    // first visit: follow the system, server already rendered dark as default
    if (!/(?:^|;\s*)theme=/.test(document.cookie)) {
        const light = window.matchMedia('(prefers-color-scheme: light)').matches;
        if (light) setTheme('light');
    }

    document.querySelectorAll('.theme-btn').forEach(btn => {
        btn.addEventListener('click', () => setTheme(root.dataset.theme === 'light' ? 'dark' : 'light'));
    });

    // address is base64(reversed) server side, mailto only exists once a human points at the link
    document.querySelectorAll('[data-m]').forEach(a => {
        const addr = () => atob(a.dataset.m).split('').reverse().join('');
        const arm = () => { a.href = 'mailto:' + addr(); };
        ['pointerenter', 'focus', 'touchstart'].forEach(ev => a.addEventListener(ev, arm, { once: true, passive: true }));
        const label = a.querySelector('.mail-label');
        if (!label) return;
        // headless harvesters rarely scroll down to the contact block
        const io = new IntersectionObserver(es => {
            if (es[0].isIntersecting) { label.textContent = addr(); io.disconnect(); }
        });
        io.observe(a);
    });

    const clock = document.querySelector('.clock');
    if (clock) {
        const fmt = new Intl.DateTimeFormat('en-GB', { hour: '2-digit', minute: '2-digit', hour12: false, timeZone: 'Europe/Paris' });
        const tick = () => { clock.textContent = fmt.format(new Date()); };
        tick();
        setInterval(tick, 10000);
    }

    const canvas = document.querySelector('.ambient');
    if (!canvas) return;

    const shell = canvas.parentElement;
    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const lines = [
        '$ pvecm status',
        '$ qm start 117 && qm status 117',
        '$ pct exec 216 -- df -h /',
        '@mcp.tool()',
        'async def list_nodes() -> list[dict]:',
        '    return await proxmox.nodes.get()',
        '$ docker compose up -d --build',
        '$ systemctl restart cloudflared',
        '$ ssh root@pve2 "uptime"',
        'from django.shortcuts import render',
        'yield f"data: {chunk}\\n\\n"',
        '$ strings ./chall | grep -i flag',
        '(module (memory (export "mem") 1))',
        '$ wasm-objdump -x game.wasm',
        '$ git commit -m "pin kernel"',
        '$ python -m pytest -q',
        '$ nmap -sV 10.0.0.0/24',
        'lancache: HIT steam depot',
    ];
    const glyphs = '01<>/{}[]#$%&*+=;:~';
    const mouse = { x: -9999, y: -9999, on: false };
    const R = 160;
    let ctx, w, h, cw, cols, rowText = [], muted, accent, baseA, peakA, lens = 0, visible = true, last = 0;
    const lh = 22;

    function readColors() {
        const st = getComputedStyle(canvas);
        muted = st.getPropertyValue('--muted').trim() || '#a99bc4';
        accent = st.getPropertyValue('--accent').trim() || '#c9a2ff';
        baseA = parseFloat(st.getPropertyValue('--ambient-base')) || 0.12;
        peakA = parseFloat(st.getPropertyValue('--ambient-peak')) || 0.45;
    }

    function setup() {
        const r = canvas.getBoundingClientRect();
        if (!r.width || !r.height) return;
        const dpr = Math.min(window.devicePixelRatio || 1, 2);
        canvas.width = Math.round(r.width * dpr);
        canvas.height = Math.round(r.height * dpr);
        ctx = canvas.getContext('2d');
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
        ctx.font = '13px ui-monospace, "SF Mono", Menlo, Consolas, monospace';
        ctx.textBaseline = 'top';
        w = r.width;
        h = r.height;
        cw = ctx.measureText('M').width;
        cols = Math.ceil(w / cw) + 2;
        rowText = [];
        const rows = Math.ceil(h / lh);
        for (let i = 0; i < rows; i++) {
            let t = '';
            let k = (i * 7) % lines.length;
            while (t.length < cols * 2) { t += lines[k] + '      '; k = (k + 3) % lines.length; }
            rowText.push(t);
        }
        readColors();
    }

    function hash(a, b, c) {
        let x = (Math.imul(a, 374761393) + Math.imul(b, 668265263) + Math.imul(c, 1442695041)) | 0;
        x = Math.imul(x ^ (x >>> 13), 1274126177);
        x ^= x >>> 16;
        return (x >>> 0) / 4294967296;
    }

    function draw(now) {
        if (!ctx) return;
        const t = now / 1000;
        lens += ((mouse.on && !reduce ? 1 : 0) - lens) * 0.15;
        const tick = Math.floor(now / 110);
        ctx.clearRect(0, 0, w, h);
        for (let i = 0; i < rowText.length; i++) {
            const y = i * lh;
            const fade = Math.max(0, 1 - y / h);
            const base = baseA * fade * fade;
            if (base < 0.004) continue;
            const text = rowText[i];
            const L = text.length;
            // alternate scroll direction per row, speed 5..13 px/s
            const speed = (i % 2 ? 1 : -1) * (5 + ((i * 7) % 9));
            const span = L * cw;
            const px = (((t * speed) % span) + span) % span;
            const k0 = Math.floor(px / cw);
            const x0 = -(px - k0 * cw);
            const near = lens > 0.02 && Math.abs(y + lh / 2 - mouse.y) < R;
            if (!near) {
                ctx.globalAlpha = base;
                ctx.fillStyle = muted;
                ctx.fillText((text + text).substr(k0, cols), x0, y);
                continue;
            }
            for (let j = 0; j < cols; j++) {
                let ch = text.charAt((k0 + j) % L);
                const x = x0 + j * cw;
                const dx = x + cw / 2 - mouse.x;
                const dy = y + lh / 2 - mouse.y;
                const d = Math.sqrt(dx * dx + dy * dy);
                if (d < R) {
                    let k = 1 - d / R;
                    k = k * k * (3 - 2 * k) * lens;
                    if (ch !== ' ' && hash(k0 + j, i, tick) < k * 0.55) {
                        ch = glyphs.charAt(Math.floor(hash(j, i, tick + 7) * glyphs.length));
                    }
                    if (ch === ' ') continue;
                    ctx.globalAlpha = base + (peakA - base) * k;
                    ctx.fillStyle = k > 0.08 ? accent : muted;
                } else {
                    if (ch === ' ') continue;
                    ctx.globalAlpha = base;
                    ctx.fillStyle = muted;
                }
                ctx.fillText(ch, x, y);
            }
        }
        ctx.globalAlpha = 1;
    }

    shell.addEventListener('mousemove', e => {
        const r = canvas.getBoundingClientRect();
        mouse.x = e.clientX - r.left;
        mouse.y = e.clientY - r.top;
        mouse.on = true;
    });
    shell.addEventListener('mouseleave', () => { mouse.on = false; });
    document.addEventListener('themechange', () => { readColors(); if (reduce) draw(0); });

    setup();
    if (reduce) {
        draw(0);
    } else {
        const loop = now => {
            requestAnimationFrame(loop);
            // ~30fps is plenty for a background
            if (!visible || now - last < 33) return;
            last = now;
            draw(now);
        };
        requestAnimationFrame(loop);
    }
    new ResizeObserver(() => { setup(); if (reduce) draw(0); }).observe(canvas);
    new IntersectionObserver(es => { visible = es[0].isIntersecting; }).observe(canvas);
})();
