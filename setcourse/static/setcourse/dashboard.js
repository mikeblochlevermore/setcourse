function view_messages(module_id) {

    fetch(`/view_messages/${module_id}`)
    .then(response => response.json())
    .then(messages => {

      const chat_main = document.getElementById("chat_main");

      chat_main.innerHTML =
      `<form onsubmit="send_message(event, ${module_id})">
            <input class="inputfield" type="text" id="message_input" name="message" placeholder="Message"></input>
            <button type="submit" type="submit">Post</button>
      </form>`

      // Loop through each message and create HTML elements
      messages.forEach(message => {

            var element = document.createElement("div");

            // messages by the host of the course have specific styling
            if (message.by_host == true) {
                element.innerHTML =
                    `<div class="host_message">
                        <p class="host_message_text"><strong>${message.user} (host):</strong> ${message.message}</p>
                        <p class="message_time">${message.time}</p>
                    </div>`;
            }
            else {
                element.innerHTML =
                    `<div class="message">
                        <p class="message_text"><strong>${message.user}:</strong> ${message.message}</p>
                        <p class="message_time">${message.time}</p>
                    </div>`;
            }
            chat_main.append(element);
        })
    })
}


function send_message (event, module_id) {

    // Stops page refresh
    event.preventDefault();

    // Track input fields
    const message_input = document.querySelector('#message_input');

    fetch('/new_message', {
    method: 'POST',
        body: JSON.stringify({
        message: `${message_input.value}`,
        module_id: module_id,
    })
    })
    .then(() => view_messages(module_id));
}