function sendMessage() {
  var sound = document.getElementById("messageSound");
  sound.play(); // Play the sound

  var userInput = document.getElementById("user-input").value.trim();
  if (userInput !== "") {
    appendMessage("user", userInput);
    document.getElementById("user-input").value = "";
    fetchResponse(userInput);
  }
}




function startSpeechRecognition() {
  var recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition || window.mozSpeechRecognition || window.msSpeechRecognition)();
  recognition.lang = 'en-US';

  recognition.onstart = function() {
    console.log('Speech recognition started...');
  };

  recognition.onresult = function(event) {
    var transcript = event.results[0][0].transcript;
    console.log('Transcript:', transcript);
    appendMessage("user", transcript);
    fetchResponse(transcript);
  };

  recognition.onerror = function(event) {
    console.error('Speech recognition error:', event.error);
  };

  recognition.onend = function() {
    console.log('Speech recognition ended.');
  };

  recognition.start();
}









function appendMessage(sender, message, imageUrl) {
  var chatContainer = document.getElementById("chat-container");
  var messageContainer = document.createElement("div");
  var messageElement = document.createElement("div");
  var profilePicture = document.createElement("img"); 
  var timeElement = document.createElement("div")

  messageContainer.classList.add("message-container");
  messageElement.textContent = message;

  if (sender === "bot") {
    messageElement.classList.add("bot-message");
    if (imageUrl) {
      var image = document.createElement("img");
      image.src = imageUrl;
      messageContainer.appendChild(messageElement);
      messageContainer.appendChild(image); 
    } else {
      messageContainer.appendChild(messageElement); 
    }
    // Add the current time below the bot's message
    timeElement.textContent = getCurrentTime();
    timeElement.classList.add("message-time");
    messageContainer.appendChild(timeElement);
  } else {
    messageElement.classList.add("user-message");
    messageContainer.appendChild(messageElement);
    // Add the profile picture below the user's message
    profilePicture.src = "MICA_chathead4.png"; // Set the profile picture source
    profilePicture.classList.add("profile-picture");
    messageContainer.appendChild(profilePicture); 
  }

  chatContainer.appendChild(messageContainer);
  chatContainer.scrollTop = chatContainer.scrollHeight;
}








// Function to get the current time
function getCurrentTime() {
  var now = new Date();
  var hours = now.getHours();
  var minutes = now.getMinutes();
  var ampm = hours >= 12 ? "PM" : "AM";
  hours = hours % 12;
  hours = hours ? hours : 12; // Handle midnight
  minutes = minutes < 10 ? "0" + minutes : minutes; // Add leading zero to minutes
  var timeString = hours + ":" + minutes + " " + ampm;
  return timeString;
}







function fetchResponse(message) {
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/get_response", true);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.onreadystatechange = function () {
    if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
      var data = JSON.parse(xhr.responseText);
      appendBotMessage(data.response, data.image);
      speakBotMessage(data.response); // Speak the bot's message
    }
  };
  xhr.send(JSON.stringify({ message: message }));
}

function appendBotMessage(message, imageUrl) {
  appendMessage("bot", message, imageUrl);
}





function speakBotMessage(message) {
  // Remove emoji from the message
  var textOnlyMessage = message.replace(/[\uD800-\uDBFF][\uDC00-\uDFFF]/g, '');

  var speech = new SpeechSynthesisUtterance(textOnlyMessage);
  speechSynthesis.speak(speech);
}










  function handleKeyPress(event) {
    if (event.key === "Enter") {
      sendMessage(); // Call sendMessage function when Enter key is pressed
    }
  }







  function handlePromptClick(prompt) {
    document.getElementById("user-input").value = prompt;
    sendMessage(); 
  }
  
  // Add event listener to input field
  var userInput = document.getElementById("user-input");
  userInput.addEventListener("keypress", handleKeyPress);

  // Add event listener to prompt items
  var promptItems = document.getElementsByClassName("prompt-item");
  for (var i = 0; i < promptItems.length; i++) {
    promptItems[i].addEventListener("click", function() {
      handlePromptClick(this.textContent);
    });
  }

  // Add event listener to microphone button
  var micButton = document.getElementById("mic-button");
  micButton.addEventListener("click", function() {
    startSpeechRecognition(); 
  });

  setInterval(changeText, 4000); // Call every 4 seconds












  
  
  
  
  
  
  
