from pyrsistent import pmap, pset
from functools import reduce

class GraphOp(object):
  def serialize(self):
    raise NotImplementedError

class AddChild(GraphOp):
  def __init__(self, parent_id, node):
    self.parent_id = parent_id
    self.node = node

  def serialize(self):
    return {
      'type': 'add',
      'parent_id': self.parent_id,
      'node': self.node.serialize()
    }

  def __repr__(self):
    return 'AddChild(parent_id={}, node={})'.format(self.parent_id, self.node)

class RemoveChild(GraphOp):
  def __init__(self, id):
    self.id = id

  def serialize(self):
    return {
      'type': 'remove',
      'id': self.id
    }

  def __repr__(self):
    return 'RemoveChild(id={})'.format(self.id)

class NodeValue(object):
  """
  Represents a Value that can be stored in a Node. Can provide implementations
  to diff between values, and serialize itself.
  """

  def serialize(self):
    return {}

  def diff(self, other):
    return []

class Node(object):
  """
  Represents an immutable Node in the graph store. A node has an ID, zero or more children,
  and a `value` representing the actual data stored in the Node.
  """

  ROOT_ID = -1

  def __init__(self, id, value=None, children=None):
    self.id = id
    self.parent_id = Node.ROOT_ID
    self.value = value or NodeValue()
    self.children = children or pmap()
    # A transitive set of child IDs helps us mutate efficiently.
    if len(self.children) > 0:
      self.transitive_child_id_set = reduce(lambda x, y: x | y,
        [c.transitive_child_id_set for c in self.children.values()] +
        [pset(self.children.keys())]
      )
    else:
      self.transitive_child_id_set = pset()

  def with_value(self, new_value):
    return Node(self.id, new_value, self.children)

  def with_children(self, new_children):
    return Node(self.id, self.value, new_children)

  def add_child(self, new_child):
    # Kind of lying about immutability here, but this is a convenient way to get the parent ID.
    new_child.parent_id = self.id
    return self.with_children(self.children.set(new_child.id, new_child))

  def mutate(self, target_id, func):
    """
    Mutate the node with the target ID by applying a function to it. target_id may
    be this node's ID, or one of its child IDs. If the target ID is not a part of this
    sub-tree, returns None, otherwise returns a new Node reflecting your modifications.
    """
    if target_id == self.id:
      return func(self)
    elif target_id in self.transitive_child_id_set:
      for child in self.children.values():
        ret = child.mutate(target_id, func)
        if ret is not None:
          return self.with_children(self.children.set(child.id, ret))
    else:
      return None

  def serialize(self):
    return {
      'id': self.id,
      'children': [child.serialize() for child in self.children.values()],
      'value': self.value.serialize()
    }

  def diff(self, other):
    """
    Returns a list of GraphOps representing differences between this Node and the target.
    """
    if self is other:
      # Reference equals means exactly equals, since we are immutable
      return []
    else:
      ops = self.diff_fields(other)
      all_keys = set(self.children.keys()) | set(other.children.keys())
      for key in all_keys:
        if key not in self.children:
          ops.append(AddChild(self.id, other.children[key]))
        elif key not in other.children:
          ops.append(RemoveChild(key))
        else:
          mine = self.children[key]
          theirs = other.children[key]
          ops.extend(mine.diff(theirs))
      return ops

  def __repr__(self):
    return 'Node(ID={}, children=[{}], value={})'.format(
      self.id, len(self.children), self.value)

  def pretty(self, indent=0):
    "Pretty print this Node and its children in a tree-like format."
    print((' ' * indent) + repr(self))
    for child in self.children.values():
      child.pretty(indent + 2)

# This is actually a tree store, but graph store sounds cooler.

# NOTE: Even though this can generate a list of diffs, the serverside graph store
# doesn't support applying those diffs. We don't really need that on the server,
# so shrug.
class GraphStore(object):
  """
  An immutable store of Nodes. Supports operations on these Nodes and diffing
  between graph stores.
  """

  def __init__(self, root_node=None):
    self.root_node = root_node or Node(Node.ROOT_ID)

  @property
  def children(self):
    return self.root_node.children

  def serialize(self):
    return self.root_node.serialize()

  def diff(self, other):
    return self.root_node.diff(other.root_node)

  def mutate(self, target_id, func):
    ret = self.root_node.mutate(target_id, func)
    if ret is not None:
      return GraphStore(ret)
    else:
      return None

  def __repr__(self):
    return 'GraphStore({})'.format(self.root_node)

  def pretty(self):
    self.root_node.pretty()

  def add_node_to_root(self, new_node):
    return self.add_node(Node.ROOT_ID, new_node)

  def add_node(self, parent_id, new_node):
    def add_child_to_node(node):
      return node.add_child(new_node)
    return self.mutate(parent_id, add_child_to_node) or self
