import {Map, Set} from 'immutable';

export const PostState = {
  PENDING: 'pending',
  OK: 'ok',
  ERR: 'err',
}

export class Post {
  constructor(values, children = {}) {
    Object.assign(this, values);
    this._values = values;
    this.children = Map(children);
    this.state = PostState.PENDING;
    this.indexTransitiveChildren();
  }

  hasInSubtree(child_id) {
    return (this.id === child_id) || this.transitiveChildren.has(child_id);
  }

  withChildren(newChildren) {
    return new Post(this._values, newChildren);
  }

  addChild(newChild) {
    return this.withChildren(this.children.set(newChild.id, newChild));
  }

  addGrandChild(newChild) {
    if (newChild.parent_id === this.id) {
      return this.addChild(newChild);
    } else {
      let par = this.transitiveChildren.get(newChild.parent_id);
      par = par.addChild(newChild);
      let gpar = this.transitiveChildren.get(par.parent_id);
      while (gpar) {  // traverse up sub tree
        par = gpar.addChild(par);
        gpar = this.transitiveChildren.get(par.parent_id);
      }
      return this.addChild(par);
    }
    
  }

  indexTransitiveChildren() {
    this.transitiveChildren = this.children.merge(
      this.children.map(c => c.transitiveChildren).flatten(true));
  }

  *flatView() {
    yield this;
    for (const [_, child] of this.children) {
      yield* child.flatView();
    }
  }
}

export class PostStore {
  constructor(roots = {}) {
    this.roots = Map(roots);
  }

  addChild(newChild) {
    for (const [id, root] of this.roots) {
      if (root.hasInSubtree(newChild.parent_id)) {
        return new PostStore(this.roots.set(id, root.addGrandChild(newChild)));
      }
    }
  }

  addChildFromValues(newChildValues) {
    return this.addChild(new Post(newChildValues));
  }

  addRoot(newRoot) {
    return new PostStore(this.roots.set(newRoot.id, newRoot));
  }

  addRootFromValues(newRootValues) {
    return this.addRoot(new Post(newRootValues));
  }

  addTree(posts) {
    // NOTE(amstocker): should topologically sort these.  Also maybe do this shallowly
    //                  instead of making new PostStores.
    let tmp_store = this.addRoot(posts[0]);
    for (const child of posts.slice(1)) {
      tmp_store = tmp_store.addChild(child);
    }
    return tmp_store;
  }

  addTreeFromValues(postValues) {
    return this.addTree(postValues.map(p => new Post(p)));
  }
}
