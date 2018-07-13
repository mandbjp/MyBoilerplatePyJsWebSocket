var ws = null;

var COMMON = {
  name: "noname",
  reconnectHandler: null,
};


var ws_connect = function () {
  return new Promise((resolve, reject) => {

    var host = location.host;
    if (host === "") host = "localhost:8888";
    var path = "/";
    var protocol = "ws" + location.protocol.substr(4);
    if (!path.endsWith("/")) {
      path += "/"
    }
    ws = new WebSocket(protocol + host + path + "websocket");

    ws.onopen = function () {
      resolve();
    };

    ws.onclose = function () {
      console.warn("socket closed");
      ws = null;
      if (COMMON.reconnectHandler) {
        clearInterval(COMMON.reconnectHandler);
      }
      COMMON.reconnectHandler = setInterval(() => {
        connectSocket()
      }, 1000);
    };

    ws.onmessage = function (evt) {
      var data = JSON.parse(evt.data);
      var command = data.command;
      var payload = data.payload;
      console.info('[WS]', command);

      switch (command) {

        case "PONG":
          console.log('PONG');
          setTimeout(sendPing, pingInterval);
          break;

        case "TEXT_CHAT":
          uiAddChat(payload.message);
          uiAddNiconicoChat(payload.message);
          break;
  
        case "IINE":
          // uiAddChat(payload.message);
          uiAddNiconicoChat(payload.message);
          window.navigator.vibrate(200);
          break;

        case "GIVE-ME-NAME":
          COMMON.name = localStorage["name"] = payload.name;
          console.log("my name is", payload.name);
          break;

        default:
          console.log('unknown command: ' + command);
          break;
      }
    }
  })
}


var pingInterval = 30 * 1000;

var sendCommand = function (command, payload) {
  var data = {
    command: command,
    payload: payload
  };
  if (ws === null) {
    console.warn("websocket is not available");
    return;
  }
  ws.send(JSON.stringify(data));
}

function sendPing() {
  sendCommand("PING", {})
}


function connectSocket() {
  ws_connect()
    .then(() => {
      if (COMMON.reconnectHandler) {
        clearInterval(COMMON.reconnectHandler);
        COMMON.reconnectHandler = null;
      }

      COMMON.name = localStorage["name"];
      if (!localStorage["name"]) {
        sendCommand("GIVE-ME-NAME", {});
      }

      console.log("WebSocket connected.");
      setTimeout(sendPing, pingInterval, ws);

    });
}


var uiSendChat = () => {
  let $myChat = $("#chat-message");
  let message = $myChat.val().trim();

  if (message.length === 0){
    return;
  }

  let $template = uiAddChat(message);
  $myChat.val("");
  sendCommand("TEXT_CHAT", {
    "name": COMMON.name,
    "message": message,
  });

  let $niconico = uiAddNiconicoChat(message);
  $niconico.addClass("my-message");
  uiScrollToElement($template);
};

var uiAddChat = (message) => {
  let $chatList = $("ul.chat-list");
  let $template = $chatList.find("li[chat-template]").clone();
  $template.removeAttr("chat-template hidden");
  $template.text(message);
  $chatList.append($template);
  return $template;
};

var uiAddNiconicoChat = (message) => {
  let $chatList = $("div.niconico-container");
  let $template = $chatList.find("div[chat-template]").clone();
  $template.removeAttr("chat-template hidden");
  $template.text(message);
  $template.css({
    "top": "calc(" + Math.random() + " * 100vh - 4em)",
    "left": "calc(100vw + 2em)"
  });
  $chatList.append($template);
  $template.animate({
    "left": -$template.width()
  }, {
    "easing": "linear",
    "duration": 3000,
    "complete": function () {
      this.remove();
    }
  });
  return $template;
};

var uiScrollToElement = ($el) => {
  $el[0].scrollIntoView();
};

var loadChatHistory = () => {
  $.ajax({
    url: "/api/history",
  })
  .then(response => {
    response.history.forEach( e => uiAddChat(e.message));
  });
};

$(function () {
  connectSocket();
  loadChatHistory();

  $("#send-chat").click(() => {
    uiSendChat();
  });
  $("#chat-message").keypress(function (e) {
    var c = e.which ? e.which : e.keyCode; // クロスブラウザ対応
    if (c !== 13) {
      return;
    }
    uiSendChat();
    return;
  });
  $("#iine-btn").click(()=>{
    sendCommand("IINE", {
      "name": COMMON.name,
      "message": "👍",
    });
    uiAddNiconicoChat("👍");
    window.navigator.vibrate(200);
  });

});
