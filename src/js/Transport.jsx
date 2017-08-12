class Transport {
  constructor() {
    const isSecure = window.location.protocol === 'https:';
    const webSocketUrl = `ws${isSecure ? 's' : ''}://${window.location.host}/ws`;
    this.socket = new WebSocket(webSocketUrl);
    this.socket.onmessage = this.onMessage.bind(this);
    this.socket.onerror = this.onError.bind(this);

    window.onbeforeunload = function() {
      this.socket.close();
    }.bind(this);
  }

  onMessage(event) {
  }

  send(text) {
    this.socket.send(text);
  }

  sendJSON(obj) {
    this.send(JSON.stringify(obj));
  }

  onError(error) {
    console.error('WebSocket error', error);
  }
}

export default new Transport();
