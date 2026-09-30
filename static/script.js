const chatBox = document.getElementById("chatBox");
const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const micBtn = document.getElementById("micBtn");
const voiceBtn = document.getElementById("voiceBtn");
const newChatBtn = document.getElementById("newChatBtn");
const timeDisplay = document.getElementById("timeDisplay");


// -------------------------
// Current Date & Time
// -------------------------

function updateTime() {
    const now = new Date();

    const options = {
        weekday: "short",
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit"
    };

    timeDisplay.textContent = now.toLocaleString("en-IN", options);
}

updateTime();
setInterval(updateTime, 1000);


// -------------------------
// Add Message
// -------------------------

function addMessage(message, sender) {

    const messageDiv = document.createElement("div");

    messageDiv.classList.add("message");

    if (sender === "user") {
        messageDiv.classList.add("user-message");
    } else {
        messageDiv.classList.add("bot-message");
    }

    messageDiv.innerHTML = `
        <div class="message-content">
            ${message}
        </div>
    `;

    chatBox.appendChild(messageDiv);

    chatBox.scrollTop = chatBox.scrollHeight;
}


// -------------------------
// Typing Indicator
// -------------------------

function showTyping() {

    const typing = document.createElement("div");

    typing.id = "typingIndicator";
    typing.classList.add("message", "bot-message");

    typing.innerHTML = `
        <div class="message-content typing">
            <span></span>
            <span></span>
            <span></span>
        </div>
    `;

    chatBox.appendChild(typing);

    chatBox.scrollTop = chatBox.scrollHeight;
}


function removeTyping() {

    const typing = document.getElementById("typingIndicator");

    if (typing) {
        typing.remove();
    }
}


// -------------------------
// Send Message
// -------------------------

async function sendMessage() {

    const message = userInput.value.trim();

    if (message === "") {
        return;
    }

    addMessage(message, "user");

    userInput.value = "";

    showTyping();

    try {

        const response = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })
        });


        const data = await response.json();

        removeTyping();

        if (data.reply) {

            addMessage(data.reply, "bot");

        } else {

            addMessage(
                "Sorry, something went wrong. Please try again.",
                "bot"
            );
        }

    } catch (error) {

        removeTyping();

        addMessage(
            "Server connection problem. Please check whether Flask is running.",
            "bot"
        );

        console.error(error);
    }
}


// -------------------------
// Send Button
// -------------------------

sendBtn.addEventListener("click", sendMessage);


// -------------------------
// Enter Key
// -------------------------

userInput.addEventListener("keydown", function(event) {

    if (event.key === "Enter") {

        event.preventDefault();

        sendMessage();
    }
});


// -------------------------
// New Chat
// -------------------------

newChatBtn.addEventListener("click", function() {

    chatBox.innerHTML = "";

    addMessage(
        "Hello! 👋 I'm your College AI Assistant.<br><br>" +
        "You can ask me about college departments, courses, admission, " +
        "fees, hostel, transport, placement, faculty, events and more.",
        "bot"
    );

    userInput.focus();
});


// ==============================
// VOICE INPUT
// ==============================

let recognition;

const SpeechRecognition =
    window.SpeechRecognition ||
    window.webkitSpeechRecognition;

if (SpeechRecognition) {

    recognition = new SpeechRecognition();

    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = "en-IN";

    recognition.onstart = function () {
        micBtn.classList.add("recording");
        micBtn.innerHTML = "🔴";
    };

    recognition.onresult = function (event) {

    const transcript =
        event.results[0][0].transcript;

    alert("You said: " + transcript);

    userInput.value = transcript;

    micBtn.classList.remove("recording");
    micBtn.innerHTML = "🎤";

    sendMessage();
};

    recognition.onerror = function (event) {

        console.log("Speech recognition error:", event.error);

        micBtn.classList.remove("recording");
        micBtn.innerHTML = "🎤";

        if (event.error === "not-allowed") {
            alert("Microphone permission allow pannunga.");
        }
    };

    recognition.onend = function () {
        micBtn.classList.remove("recording");
        micBtn.innerHTML = "🎤";
    };

    micBtn.addEventListener("click", function () {

        try {
            recognition.start();
        } catch (error) {
            console.log(error);
        }

    });

} else {

    micBtn.addEventListener("click", function () {

        alert(
            "Voice input Chrome browser-la try pannunga."
        );

    });

}



// -------------------------
// Voice Output
// -------------------------

voiceBtn.addEventListener("click", function() {

    const messages =
        document.querySelectorAll(".bot-message");

    if (messages.length === 0) {
        return;
    }

    const lastMessage =
        messages[messages.length - 1]
            .innerText;

    const speech =
        new SpeechSynthesisUtterance(lastMessage);

    speech.lang = "en-IN";

    speech.rate = 0.95;

    speech.pitch = 1;

    window.speechSynthesis.cancel();

    window.speechSynthesis.speak(speech);
});


// -------------------------
// Welcome Message
// -------------------------

if (chatBox.children.length === 0) {

    addMessage(
        "Hello! 👋 I'm your College AI Assistant.<br><br>" +
        "Ask me anything about your college. " +
        "I can help with departments, courses, admission, " +
        "fees, hostel, transport, placement and more.",
        "bot"
    );
}

// ==============================
// DARK MODE
// ==============================

const themeBtn = document.getElementById("themeBtn");

if (themeBtn) {

    themeBtn.addEventListener("click", function () {

        document.body.classList.toggle("dark-mode");

        if (document.body.classList.contains("dark-mode")) {
            themeBtn.innerHTML = "☀️";
        } else {
            themeBtn.innerHTML = "🌙";
        }

    });

}