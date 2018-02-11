
class TransportCaller {
  constructor(transport) {
    this.transport = transport;
  }

  addPost(post) {
    this.transport.callRpc('add_post', post);
  }

  getHot({n}) {
    this.transport.callRpc('get_hot', {n: n});
  }

  getTopLevels() {
    this.transport.callRpc('get_toplevels');
  }

  subscribe({id}) {
    this.transport.callRpc('subscribe', {id: id});
  }

  getTree({id}) {
    this.transport.callRpc('get_tree', {id: id});
  }
}
