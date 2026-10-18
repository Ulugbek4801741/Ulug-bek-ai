<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ulug'bek AI - Autonomous Enterprise Platform</title>
    
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
        body { background: #050811; color: #f8fafc; font-family: 'Plus Jakarta Sans', sans-serif; }
        .glass-panel { background: rgba(13, 19, 33, 0.85); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.08); }
        .avatar-pulse { animation: pulse 1.8s infinite alternate; }
        @keyframes pulse { 
            0% { box-shadow: 0 0 15px rgba(16, 185, 129, 0.4); transform: scale(1); } 
            100% { box-shadow: 0 0 35px rgba(99, 102, 241, 0.8); transform: scale(1.05); } 
        }
        .speaking { animation: talk 0.3s infinite alternate; border-color: #10b981 !important; }
        @keyframes talk { 0% { border-width: 2px; } 100% { border-width: 6px; } }
        .terminal-scroll::-webkit-scrollbar { width: 4px; }
        .terminal-scroll::-webkit-scrollbar-thumb { background: #10b981; border-radius: 4px; }
    </style>
</head>
<body class="min-h-screen p-3 md:p-6 pb-20">

    <!-- AUTHENTICATION MODAL -->
    <div id="authModal" class="fixed inset-0 bg-black/90 backdrop-blur-xl flex items-center justify-center z-50 p-4">
        <div class="glass-panel max-w-md w-full rounded-3xl p-6 space-y-5 border border-indigo-500/30 shadow-2xl">
            <div class="text-center">
                <h2 class="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 via-indigo-400 to-purple-400">Ulug'bek AI</h2>
                <p class="text-xs text-slate-400 mt-1">Xalqaro Avtonom Platforma va AI Ekosistemasi</p>
            </div>
            <button onclick="loginUser()" class="w-full bg-gradient-to-r from-indigo-600 to-emerald-600 hover:from-indigo-500 hover:to-emerald-500 text-white font-extrabold py-3.5 rounded-xl text-xs shadow-lg transition">
                🚀 Platformaga Kirish
            </button>
        </div>
    </div>

    <!-- MAIN BRAND HEADER -->
    <header class="glass-panel rounded-3xl p-5 mb-6 max-w-7xl mx-auto flex flex-col lg:flex-row justify-between items-center gap-4 border border-indigo-500/20">
        <div>
            <div class="flex items-center gap-3">
                <span class="w-4 h-4 bg-emerald-500 rounded-full animate-pulse shadow-[0_0_12px_#10b981]"></span>
                <h1 class="text-2xl md:text-4xl font-extrabold tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 via-indigo-400 to-purple-400">
                    Ulug'bek AI
                </h1>
            </div>
            <p class="text-xs text-slate-400 mt-1 font-medium">Universal Autonomous No-Code Engine & Multi-Agent Ecosystem</p>
        </div>
        <div class="bg-slate-900/90 border border-slate-800 px-4 py-2 rounded-2xl text-xs text-slate-300 font-bold flex items-center gap-2">
            <i class="fa-solid fa-shield-halved text-emerald-400"></i> Status: <span class="text-emerald-400">ONLINE (70/30 Share Active)</span>
        </div>
    </header>

    <!-- MAIN PLATFORM GRID -->
    <main class="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-6">

        <!-- LEFT COLUMN: CHAT & FILE UPLOAD AGENT -->
        <section class="glass-panel rounded-3xl p-5 flex flex-col justify-between space-y-4">
            <div>
                <h2 class="text-base font-extrabold border-b border-slate-800 pb-3 flex items-center justify-between">
                    <span><i class="fa-solid fa-robot text-emerald-400 mr-2"></i> Ulug'bek AI Chat Agent</span>
                    <span class="text-[10px] bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded-full font-semibold">ONLINE</span>
                </h2>

                <!-- Interactive Avatar -->
                <div class="flex flex-col items-center justify-center my-4">
                    <div id="avatarCircle" class="w-24 h-24 rounded-full border-4 border-indigo-500 flex items-center justify-center bg-slate-900 avatar-pulse relative overflow-hidden">
                        <i id="avatarIcon" class="fa-solid fa-brain text-4xl text-emerald-400"></i>
                    </div>
                    <p class="text-xs text-slate-200 font-bold mt-2">Ulug'bek AI Agent</p>
                </div>

                <!-- Chat Box -->
                <div id="chatBox" class="h-48 overflow-y-auto bg-slate-950/90 rounded-2xl p-3 space-y-2 border border-slate-800 text-xs terminal-scroll">
                    <div class="bg-indigo-950/50 p-2.5 rounded-xl border border-indigo-500/30 text-slate-300">
                        <span class="font-extrabold text-indigo-300">Ulug'bek AI:</span> Salom, Ulug'bek aka! Menga istalgan savolni yozing yoki fayl yuboring.
                    </div>
                </div>
            </div>

            <!-- Chat Input & File Upload Controls -->
            <div class="space-y-2 pt-2">
                <div id="fileNameDisplay" class="hidden text-[10px] text-emerald-400 bg-emerald-950/40 p-1.5 rounded-lg border border-emerald-500/30 flex justify-between items-center">
                    <span id="attachedFileName">Fayl biriktirildi</span>
                    <button onclick="removeAttachedFile()" class="text-red-400 font-bold hover:text-red-300">✕ O'chirish</button>
                </div>

                <div class="flex gap-2 items-center">
                    <!-- File Upload Button -->
                    <label class="bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-300 px-3 py-2.5 rounded-xl text-xs cursor-pointer transition flex items-center justify-center" title="Fayl yuklash">
                        <i class="fa-solid fa-paperclip text-indigo-400"></i>
                        <input type="file" id="chatFileInput" class="hidden" onchange="handleFileUpload(event)">
                    </label>

                    <input type="text" id="userInput" placeholder="Xabar yozing..." class="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-3 py-2.5 text-xs text-slate-200 focus:outline-none focus:border-indigo-500">
                    
                    <button onclick="sendChatMessage()" class="bg-indigo-600 hover:bg-indigo-500 text-white px-3.5 py-2.5 rounded-xl text-xs font-bold shadow-md transition">
                        <i class="fa-solid fa-paper-plane"></i>
                    </button>
                </div>
            </div>
        </section>

        <!-- RIGHT COLUMN: NO-CODE ENGINE -->
        <section class="glass-panel rounded-3xl p-5 lg:col-span-2 flex flex-col justify-between space-y-4">
            <div>
                <h2 class="text-base font-extrabold border-b border-slate-800 pb-3 flex items-center justify-between">
                    <span><i class="fa-solid fa-wand-magic-sparkles text-indigo-400 mr-2"></i> Ulug'bek AI No-Code App Engine</span>
                    <span class="text-[10px] bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded-full font-semibold">Auto-Build</span>
                </h2>

                <div class="mt-4 space-y-3">
                    <label class="block text-xs font-semibold text-slate-300">Ilova yoki O'yin Prompt Tavsifi:</label>
                    <textarea id="appPrompt" rows="4" class="w-full bg-slate-950/90 border border-slate-800 rounded-2xl p-3.5 text-xs text-slate-200 focus:outline-none focus:border-indigo-500" placeholder="Masalan: Bank xizmatlari va valyuta kursini hisoblovchi ilova yozib ber..."></textarea>
                </div>

                <div class="grid grid-cols-2 md:grid-cols-4 gap-2.5 mt-3 text-xs">
                    <label class="flex items-center gap-2 bg-slate-950 p-2.5 rounded-xl border border-slate-800 cursor-pointer"><input type="checkbox" checked class="accent-indigo-500"> Android (.apk)</label>
                    <label class="flex items-center gap-2 bg-slate-950 p-2.5 rounded-xl border border-slate-800 cursor-pointer"><input type="checkbox" checked class="accent-indigo-500"> iOS App</label>
                    <label class="flex items-center gap-2 bg-slate-950 p-2.5 rounded-xl border border-slate-800 cursor-pointer"><input type="checkbox" checked class="accent-indigo-500"> Web App</label>
                    <label class="flex items-center gap-2 bg-slate-950 p-2.5 rounded-xl border border-slate-800 cursor-pointer"><input type="checkbox" checked class="accent-indigo-500"> Windows EXE</label>
                </div>
            </div>

            <!-- NO-CODE SUBMIT BUTTON & TERMINAL -->
            <div class="space-y-3 pt-2">
                <button onclick="startAppGeneration()" class="w-full bg-gradient-to-r from-indigo-600 via-purple-600 to-emerald-600 hover:from-indigo-500 hover:to-emerald-500 text-white font-extrabold py-4 rounded-2xl text-sm flex items-center justify-center gap-2 shadow-2xl transition">
                    <i class="fa-solid fa-rocket"></i> 🚀 Avtonom Ilovani Yaratish (No-Code Submit)
                </button>

                <div id="buildMonitor" class="hidden bg-slate-950 p-4 rounded-2xl border border-slate-800 space-y-3 text-xs">
                    <div class="flex justify-between items-center">
                        <span id="buildStatus" class="font-bold text-indigo-400">🔍 AI Serveridan Javob Olinmoqda...</span>
                        <span id="buildPercent" class="font-extrabold text-emerald-400">20%</span>
                    </div>

                    <div id="terminalOutput" class="h-32 overflow-y-auto bg-black p-3 rounded-xl font-mono text-[11px] text-emerald-400 border border-slate-900 terminal-scroll">
                        <p class="text-slate-500">[SYSTEM]: Ulug'bek AI Engine Initialized...</p>
                    </div>

                    <div id="downloadArea" class="hidden pt-2 border-t border-slate-800 flex gap-2">
                        <a id="downloadLink" href="#" class="bg-emerald-600 hover:bg-emerald-500 text-white font-extrabold px-4 py-2.5 rounded-xl text-xs flex items-center gap-2 shadow-lg">
                            📲 Yaratilgan Ilovani (.html) Yuklab Olish
                        </a>
                    </div>
                </div>
            </div>
        </section>

    </main>

    <!-- SYSTEM JAVASCRIPT -->
    <script>
        // SIZ YUBORGAN HAQIQIY GEMINI API KALITI KO'CHIRILDI
        const SYSTEM_API_KEY = "AQ.Ab8RN6IBmKYdQGq1Fraa3yiPNIEjJBBohAgokd-RsqopZDvSEQ"; 

        let attachedFileData = null;

        function loginUser() {
            document.getElementById('authModal').classList.add('hidden');
        }

        function handleFileUpload(event) {
            const file = event.target.files[0];
            if(file) {
                attachedFileData = file.name;
                document.getElementById('attachedFileName').innerText = "Biriktirildi: " + file.name;
                document.getElementById('fileNameDisplay').classList.remove('hidden');
            }
        }

        function removeAttachedFile() {
            attachedFileData = null;
            document.getElementById('fileNameDisplay').classList.add('hidden');
            document.getElementById('chatFileInput').value = "";
        }

        // UNIVERSAL API CALL FUNCTION (SUPPORTING NEW GOOGLE API KEY FORMATS)
        async function callGeminiAPI(promptText) {
            // URL orqali API kalitni yuborish
            const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${SYSTEM_API_KEY}`;
            const payload = { contents: [{ parts: [{ text: promptText }] }] };

            let response = await fetch(url, {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${SYSTEM_API_KEY}` // Yangi formatlar uchun qo'shimcha Authorization sarlavhasi
                },
                body: JSON.stringify(payload)
            });

            return await response.json();
        }

        // CHAT AGENT SERVER REQUEST
        async function sendChatMessage() {
            const input = document.getElementById('userInput');
            let text = input.value.trim();
            const chatBox = document.getElementById('chatBox');

            if(!text && !attachedFileData) return;

            let displayMsg = text;
            if(attachedFileData) {
                displayMsg += ` [Fayl: ${attachedFileData}]`;
            }

            chatBox.innerHTML += `<div class="bg-slate-900 p-2.5 rounded-xl text-right"><span class="font-bold text-slate-300">Siz:</span> ${displayMsg}</div>`;
            input.value = '';
            chatBox.scrollTop = chatBox.scrollHeight;

            let promptToSend = text;
            if(attachedFileData) {
                promptToSend += ` (Fayl biriktirildi: ${attachedFileData})`;
                removeAttachedFile();
            }

            try {
                const data = await callGeminiAPI(promptToSend);

                if(data.candidates && data.candidates[0]) {
                    const aiReply = data.candidates[0].content.parts[0].text;
                    chatBox.innerHTML += `<div class="bg-indigo-950/50 p-2.5 rounded-xl border border-indigo-500/30 text-slate-200"><span class="font-extrabold text-indigo-300">Ulug'bek AI:</span> ${aiReply}</div>`;
                } else if(data.error) {
                    chatBox.innerHTML += `<div class="bg-red-950/60 p-2.5 rounded-xl text-red-300">❌ Server Javobi: ${data.error.message}</div>`;
                } else {
                    chatBox.innerHTML += `<div class="bg-red-950/60 p-2.5 rounded-xl text-red-300">❌ Server kutilmagan javob qaytardi.</div>`;
                }
            } catch(err) {
                chatBox.innerHTML += `<div class="bg-red-950/60 p-2.5 rounded-xl text-red-300">❌ Serverga ulanishda xatolik yuz berdi.</div>`;
            }
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        // NO-CODE GENERATOR ENGINE
        async function startAppGeneration() {
            const prompt = document.getElementById('appPrompt').value.trim();
            const monitor = document.getElementById('buildMonitor');
            const terminal = document.getElementById('terminalOutput');
            const downloadArea = document.getElementById('downloadArea');

            if(!prompt) { alert("Iltimos, ilova g'oyasini kiriting!"); return; }

            monitor.classList.remove('hidden');
            downloadArea.classList.add('hidden');
            document.getElementById('buildPercent').innerText = "40%";
            terminal.innerHTML = `<p class="text-emerald-400">[SYSTEM]: Ulug'bek AI Engine serverga ulanmoqda...</p>`;

            try {
                const data = await callGeminiAPI("O'zbek tilida ushbu ilova uchun to'liq HTML, CSS va JS kodi yozib ber: " + prompt);

                document.getElementById('buildPercent').innerText = "85%";

                if(data.candidates && data.candidates[0]) {
                    const generatedCode = data.candidates[0].content.parts[0].text;

                    document.getElementById('buildPercent').innerText = "100%";
                    document.getElementById('buildStatus').innerText = "🎉 Muvaffaqiyatli Yaratildi!";
                    terminal.innerText = generatedCode;

                    const blob = new Blob([generatedCode], { type: 'text/html' });
                    document.getElementById('downloadLink').href = URL.createObjectURL(blob);
                    document.getElementById('downloadLink').download = "Ulugbek_AI_App.html";
                    downloadArea.classList.remove('hidden');
                } else if(data.error) {
                    terminal.innerHTML += `<p class="text-red-400">[ERROR]: ${data.error.message}</p>`;
                    document.getElementById('buildStatus').innerText = "❌ AI Xatosi!";
                } else {
                    throw new Error("Empty response");
                }
            } catch(err) {
                terminal.innerHTML += `<p class="text-red-400">[ERROR]: Serverga ulanishda xatolik yuz berdi!</p>`;
                document.getElementById('buildStatus').innerText = "❌ Xatolik!";
            }
        }
    </script>
</body>
</html>
