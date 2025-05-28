document.addEventListener("DOMContentLoaded", function () {
    const chatSocket = new WebSocket(`ws://${window.location.host}/ws/chat/${chatId}/`);

    chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        let chatBody = document.querySelector(".chat-body .messages");

        let newMessage = document.createElement("div");
        newMessage.classList.add("chats");
        newMessage.innerHTML = `
            <div class="chat-avatar">
                <img src="/static/assets/img/profiles/avatar-06.jpg" class="rounded-circle" alt="image">
            </div>
            <div class="chat-content">
                <div class="chat-profile-name">
                    <h6>${data.sender} <span class="chat-time">${data.timestamp}</span></h6>
                </div>
                <div class="chat-info">
                    <div class="message-content">${data.message}</div>
                </div>
            </div>
        `;
        chatBody.appendChild(newMessage);
        chatBody.scrollTop = chatBody.scrollHeight; // Scroll pastga tushadi
    };

    document.getElementById("send-message").addEventListener("click", function () {
        let messageInput = document.getElementById("chat-message");
        let message = messageInput.value;
        let senderId = document.getElementById("user-id").value;

        chatSocket.send(JSON.stringify({
            "message": message,
            "sender_id": senderId,
        }));

        messageInput.value = "";
    });
});
