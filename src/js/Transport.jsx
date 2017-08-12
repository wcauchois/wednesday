import shortid from 'shortid';

class Transport {
  constructor() {
    const isSecure = window.location.protocol === 'https:';
    const webSocketUrl = `ws${isSecure ? 's' : ''}://${window.location.host}/ws`;
    this.socket = new WebSocket(webSocketUrl);
    this.socket.onmessage = this.onMessage.bind(this);
    this.socket.onerror = this.onError.bind(this);
    window.onbeforeunload = () => this.socket.close();
    this.unresolvedRpcs = {};
  }

  callRpc(methodName, ...args) {
    const callId = shortid.generate();
    const payload = {
      'type': 'rpc',
      'call_id': callId,
      'method': methodName,
      'arguments': args
    };
    return new Promise((resolve, reject) => {
      this.unresolvedRpcs[callId] = (response) => {
        if (response.type === 'rpc_error') {
          reject(new Error(response.message));
        } else {
          resolve(response.return_value);
        }
      };
      this.sendJSON(payload);
    });
  }

  onMessage(event) {
    console.log(`Got message from server: ${event.data}`);
    const payload = JSON.parse(event.data);
    if (/rpc_(error|success)/.test(payload.type)) {
      const callId = payload.call_id;
      if (callId in this.unresolvedRpcs) {
        this.unresolvedRpcs[callId](payload);
      } else {
        console.error(`Warning: Got response for RPC we didn't initiate`, payload);
      }
    }
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
