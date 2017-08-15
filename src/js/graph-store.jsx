import {Map, List, Set} from 'immutable';

export class Node {
  constructor(id, value, children) {
    this.id = id;
    this.value = value;
    this.children = Map(children || {})
    this.transitiveChildIdSet = Set(this.children.map(c => c.id)).union(
      this.children.map(c => c.transitiveChildIdSet).flatten(true));
  }

  withChildren(newChildren) {
    return new Node(this.id, this.value, newChildren);
  }

  addChild(newChild) {
    return this.withChildren(this.children.set(newChild.id, newChild));
  }

  static deserialize(json, valueDeserializer=(x=>x)) {
    const childMap = {}
    json.children.forEach(child => {
      childMap[child.id] = this.deserialize(child, valueDeserializer)
    });
    return new Node(
      json.id,
      valueDeserializer(json.value),
      childMap
    );
  }

  applyToChildren(opList, valueDeserializer=(x=>x)) {
    const updatedChildren = this.children.map((value, key) => {
      return value.apply(opList, valueDeserializer);
    });
    return this.withChildren(updatedChildren);
  }

  apply(opList, valueDeserializer=(x=>x)) {
    console.log(this);
    return opList.reduce((acc, op) => {
      if (op.type === 'add') {
        if (op.parent_id === acc.id) {
          return acc.addChild(this.constructor.deserialize(op.node));
        } else if (acc.transitiveChildIdSet.has(op.parent_id)) {
          return acc.applyToChildren([op], valueDeserializer);
        } else {
          return acc;
        }
      } else if (op.type === 'remove') {
        if (op.id === acc.id) {
          throw new Error(`Op may have attempted to remove the Root node? ${opList}`);
        } else if (acc.children.has(op.id)) {
          return acc.withChildren(acc.children.delete(op.id));
        } else if (this.transitiveChildIdSet.has(op.id)) {
          return acc.applyToChildren([op]);
        } else {
          return acc;
        }
      }
    }, this);
  }
}

Node.ROOT_ID = -1;

export class GraphStore {
  constructor(rootNode) {
    this.rootNode = rootNode || new Node(Node.ROOT_ID);
  }

  allFlat() {
    const result = [];
    let workingSet = [this.rootNode];
    while (workingSet.length > 0) {
      const node = workingSet.pop();
      result.push(node);
      workingSet = workingSet.concat(node.children.valueSeq().toArray());
    }
    return result.slice(1);
  }

  withRootNode(newRootNode) {
    return new GraphStore(newRootNode);
  }

  apply(opList, valueDeserializer=(x=>x)) {
    console.log(this);
    return this.withRootNode(this.rootNode.apply(opList, valueDeserializer));
  }
}
