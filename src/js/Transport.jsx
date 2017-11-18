import moment from 'moment';
import shortid from 'shortid';
import ReconnectingWebSocket from 'reconnecting-websocket';
import {parseJsonPromise} from 'Utils';
import store from 'config/store';
import * as actions from 'actions';
import EventEmitter from 'event-emitter-es6';

const RPC_TIMEOUT = 5000;

// https://developer.mozilla.org/en-US/docs/Web/API/WebSocket#Ready_state_constants
const ReadyState = {
  CONNECTING: 0,
  OPEN: 1,
  CLOSING: 2,
  CLOSED: 3
};

class QueuedRpc {
  constructor(methodName, args, resolve, reject) {
    this.methodName = methodName;
    this.args = args;
    this.resolve = resolve;
    this.reject = reject;
  }
}

class Transport extends EventEmitter {
  constructor() {
    super();

    window.onbeforeunload = () => this.disconnect();
    this.unresolvedRpcs = {};
    this.connect();
    // RPCs may be queued if the WebSocket isn't yet connected.
    this.queuedRpcs = [];

    // Convenience proxy that lets you say "Transport.call.someRpc(myArguments)"
    this.call = new Proxy({}, {
      get: (target, name) => {
        return (...args) => {
          return this.callRpc(name, ...args);
        }
      }
    });

    // ID from server
    this.client_id = undefined;
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
      this.socket.onopen = null;
      this.socket.close();
      this.socket = null;
    }
  }

  connect() {
    this.socket = new ReconnectingWebSocket(this.getWebSocketUrl());
    this.socket.onmessage = this.onMessage.bind(this);
    this.socket.onerror = this.onError.bind(this);
    this.socket.onopen = this.onOpen.bind(this);
  }

  // Queues up the RPC if we're not connected yet.
  callRpc(methodName, ...args) {
    if (this.socket.readyState !== ReadyState.OPEN) {
      // TODO: We should probably impose a timeout here as well.
      return new Promise((resolve, reject) => {
        this.queuedRpcs.push(new QueuedRpc(methodName, args, resolve, reject));
      });
    } else {
      return this.reallyCallRpc(methodName, ...args);
    }
  }

  reallyCallRpc(methodName, ...args) {
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
          const boldStyle = 'font-weight: bold', unboldStyle = 'font-weight: normal';
          if (response.type === 'rpc_error') {
            console.error(`Got RPC error to %c${methodName}%c (call ID = ${callId})`,
              response.message, boldStyle, unboldStyle);
            reject(new Error(response.message));
          } else {
            parseJsonPromise(response.return_value)
              .then((parsedJson) => {
                console.log(`Got RPC response to %c${methodName}%c (call ID = ${callId})`,
                  boldStyle, unboldStyle, parsedJson);
                return parsedJson;
              })
              .then(resolve, reject);
          }
        }
      };
      this.sendJSON(payload);
    });
  }

  executeQueuedRpcs() {
    this.queuedRpcs.forEach(queuedRpc => {
      this.reallyCallRpc(queuedRpc.methodName, ...queuedRpc.args)
        .then(queuedRpc.resolve, queuedRpc.reject);
    });
    this.queuedRpcs = [];
  }

  onOpen(event) {
    // Handshake with server (in the future this can be an auth process)
    this.call.handshake({client_id: this.client_id}).then((res) => this.client_id = res.client_id);
    this.executeQueuedRpcs();
  }

  onMessage(event) {
    parseJsonPromise(event.data).then((payload) => {
      if (/rpc_(error|success)/.test(payload.type)) {
        const callId = payload.call_id;
        if (callId in this.unresolvedRpcs) {
          this.unresolvedRpcs[callId](payload);
        } else {
          console.error(`Warning: Got response for RPC we didn't initiate`, payload);
        }
      } else {
        console.log('Got non-RPC message from server:', payload);
        this.emit(payload.type, payload);
      }
    }).catch(err => {
      console.error(err);
    });
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
