// --- Animasi Hujan Biner ---
const canvas = document.getElementById('binaryCanvas');
const ctx = canvas.getContext('2d');

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

const binary = "01";
const fontSize = 14;
const columns = canvas.width / fontSize;
const drops = Array(Math.floor(columns)).fill(1);

function drawBinary() {
    ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    ctx.fillStyle = '#00ff66';
    ctx.font = fontSize + 'px monospace';

    for (let i = 0; i < drops.length; i++) {
        const text = binary.charAt(Math.floor(Math.random() * binary.length));
        ctx.fillText(text, i * fontSize, drops[i] * fontSize);

        if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
            drops[i] = 0;
        }
        drops[i]++;
    }
}
setInterval(drawBinary, 33);

// --- Logika Chat Exelyn ---
async function sendMessage() {
    const input = document.getElementById('userInput');
    const message = input.value.trim();
    if (!message) return;

    const chatBox = document.getElementById('chatBox');
    
    // Tampilkan pesan user
    chatBox.innerHTML += `<div class="user-msg"><b>[YOU]:</b> ${escapeHtml(message)}</div>`;
    input.value = '';
    chatBox.scrollTop = chatBox.scrollHeight;

    // Loading indicator
    const loadingId = 'loading-' + Date.now();
    chatBox.innerHTML += `<div class="bot-msg" id="${loadingId}"><b>[EXELYN]:</b> Menganalisis data...</div>`;
    
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message })
        });
        
        const data = await response.json();
        document.getElementById(loadingId).remove();
        
        chatBox.innerHTML += `<div class="bot-msg"><b>[EXELYN]:</b> ${escapeHtml(data.response)}</div>`;
    } catch (error) {
        document.getElementById(loadingId).remove();
        chatBox.innerHTML += `<div class="bot-msg" style="color: red;"><b>[EXELYN_ERROR]:</b> Gagal terhubung ke server.</div>`;
    }
    chatBox.scrollTop = chatBox.scrollHeight;
}

function handleKeyPress(e) {
    if (e.key === 'Enter') sendMessage();
}

function escapeHtml(text) {
    return text.replace(/</g, "&lt;").replace(/>/g, "&gt;");
}
