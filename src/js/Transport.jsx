import shortid from 'shortid';
import ReconnectingWebSocket from 'reconnecting-websocket';

const RPC_TIMEOUT = 5000;

class Transport {
  constructor() {
    window.onbeforeunload = () => this.disconnect();
    this.unresolvedRpcs = {};
    this.connect();

    // Convenience proxy that lets you say "Transport.call.someRpc(myArguments)"
    this.call = new Proxy({}, {
      get: (target, name) => {
        return (...args) => {
          return this.callRpc(name, ...args);
        }
      }
    });
  }

  getWebSocketUrl() {
    const isSecure = window.location.protocol === 'https:';
    return `ws${isSecure ? 's' : ''}://${window.location.host}/ws`;
  }

  disconnect() {
    if (this.socket) {
      // Clear event handlers
      this.socket.onmessage = null;
      this.socket.onerror = null;
      this.socket.close();
      this.socket = null;
    }
  }

  connect() {
    this.socket = new ReconnectingWebSocket(this.getWebSocketUrl());
    this.socket.onmessage = this.onMessage.bind(this);
    this.socket.onerror = this.onError.bind(this);
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
      const timeout = setTimeout(() => {
        const err = new Error(`RPC '${methodName}' timed out after ${RPC_TIMEOUT} milliseconds`);
        this.unresolvedRpcs[callId] && this.unresolvedRpcs[callId](null, err);
      }, RPC_TIMEOUT);
      this.unresolvedRpcs[callId] = (response, err) => {
        delete this.unresolvedRpcs[callId];
        clearTimeout(timeout);
        if (err) {
          reject(err);
        } else {
          if (response.type === 'rpc_error') {
            reject(new Error(response.message));
          } else {
            resolve(response.return_value);
          }
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
