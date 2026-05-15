// === NEXUS — main.js ===

document.addEventListener('DOMContentLoaded', function () {

    // === LIKE BUTTONS ===
    document.querySelectorAll('.like-btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const postId = btn.dataset.postId;
            const url = btn.dataset.url;
            const csrfToken = document.cookie.match(/csrftoken=([^;]+)/);

            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken ? csrfToken[1] : '',
                    'Content-Type': 'application/json',
                },
            })
            .then(function (res) { return res.json(); })
            .then(function (data) {
                const countEl = btn.querySelector('.like-count');
                if (countEl) countEl.textContent = data.count;
                if (data.liked) {
                    btn.classList.add('liked');
                } else {
                    btn.classList.remove('liked');
                }
            })
            .catch(function (err) { console.error('Erro ao dar like:', err); });
        });
    });

    // === CHAR COUNTER ===
    const textarea = document.querySelector('.post-textarea');
    const counter = document.getElementById('charCount');
    if (textarea && counter) {
        textarea.addEventListener('input', function () {
            counter.textContent = textarea.value.length;
            if (textarea.value.length > 450) {
                counter.style.color = '#f06b6b';
            } else {
                counter.style.color = '';
            }
        });
    }

    // === AUTO-DISMISS MESSAGES ===
    setTimeout(function () {
        document.querySelectorAll('.message').forEach(function (msg) {
            msg.style.transition = 'opacity 0.5s';
            msg.style.opacity = '0';
            setTimeout(function () { msg.remove(); }, 500);
        });
    }, 3500);

});