import pytest
from .solver import Node

def test_add_node():
    node = Node(0)
    node._add_node(1,0)
    assert ( 1, 0 ) == ( node.nodes[1].id, node.nodes[1].pid )

def test_calc_leafe():
    node = Node(0)
    node._add_node(1,0)
    cnode = node.nodes[1]
    esmins=cnode._calculate_leafesmins(1,1)
    print(esmins)
    assert esmins == ((0, -1), (-2, -1))

def test_discover_children_0():
    node = Node(0)
    node.discover_children({0:1, 1:1},{0:{1:1},1:{0:1}})
    assert node.nodes[1].id==1

def test_discover_children_1():
    node = Node(0)
    node.discover_children({0:1, 1:1, 2:1},{0:{1:1},1:{0:1, 2:1},2:{1:1}})
    assert (node.nodes[1].nodes[2].id, node.nodes[1].nodes[2].pid) == ( 2, 1 )

def test_esmins():
    node = Node(0)
    node.discover_children({0:1, 1:1, 2:1},{0:{1:1},1:{0:1, 2:1},2:{1:1}})
    res=node.calculate_esmins({0:1, 1:1, 2:1},{0:{1:1},1:{0:1, 2:1},2:{1:1}})
    assert res==((-3, -1), (-1, 1))

def test_minE_spin():
    node = Node(0)
    node.discover_children({0:1, 1:1, 2:1},{0:{1:1},1:{0:1, 2:1},2:{1:1}})
    node.calculate_esmins({0:1, 1:1, 2:1},{0:{1:1},1:{0:1, 2:1},2:{1:1}})
    res=dict()
    node.set_minE_spin(res)
    assert res=={2: -1, 1: 1, 0: -1}
