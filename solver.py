
"""
Ising Model Tree Solver/Node Class

This file contains the functional class for the Ising Model Tree Solver
There are three main methods to use after instantiating a Node.
The first node instantiated will be the root node.

To calculate the minimum energy spin configuration, the following three
methods should be instantiated from the root node in order

a.) Node.discover_children: discover child nodes and create tree
b.) Node.calculate_esmins calculate minimum energies and spins for each sub-tree
c.) Node.set_minE_spin calculate minimum energy and spin,
    walking down from root node

"""
import logging

class Node:
    def __init__(self, id, pid = None):
        self.id = id # my id
        self.pid = pid # my parent's id
        self.nodes = dict() #dict of tuples
        self.esmins = None # tuple of minimum energies for both parent spins
        self.spin = None # This node's spin
        self.emin = None # This node's min E for corresponding sub-tree

    def _add_node(self, cid, pid = None):
        """
        Function to add nodes
        Inputs - cid: ID of child node (node to add)
                 pid: ID of parent node (None for root)
        Outputs - None
        """
        self.nodes[cid] = Node(cid, pid)

    def discover_children(self, hdict, Jdict, pid=None):
        """
        Input - pid: parent node id, None for root
                hdict: dictionary of h referenced by node id
                Jdict: dictionary of J referenced by node id 1, node id 2
        Output - Bool
        NOTE - This function assumes a valid N-ary tree is described by inputs
        TODO -  pass list of pids down tree to make sure is valid N-Ary Tree
        """
        logging.info("Discovering children for {}".format(self.id))
        localedges = Jdict[self.id].copy()
        # TODO fix so catches key error if parent link doesn't exit
        if pid is not None:
            del localedges[pid]
        # TODO if key doesn't exist
        nlocaledges = len(localedges)
        if nlocaledges == 0:
            logging.info("Found leaf at {} with parent {}".format(self.id, pid))
        else:
            for cid in localedges.keys():
                if cid not in [ self.id, self.pid ]:
                    self._add_node(cid, self.id)
                    if len(Jdict[cid]) == 0:
                        logging.info("Found leaf at {} with parent {}".format(cid, self.id))
                    self.nodes[cid].discover_children(hdict, Jdict, pid=self.id)
            logging.info("Created {} branches at {} from parent {}".format(nlocaledges, self.id, pid))
        return True

    def calculate_esmins(self, hdict, Jdict):
        """
        Calculate min energy and minimum energy configuration
        Esmin is ((minE(sigma_n),sigma_c), (minE(sigma_p),sigma_c))
        Inputs - hdict: dictionary of h referenced by node id
                 Jdict: dictionary of J referenced by node id 1, node id 2
        Outputs - esmins: tuple(tuple,tuple) minimum energies and spins for
                          both potential parent spins
        """
        if len(self.nodes) == 0:
            h=hdict[self.id]
            J=Jdict[self.id][self.pid]
            logging.info("Leaf params for Node {} to Parent {} are h={} and J={}".format(self.id, self.pid, h, J))
            self.esmins=self._calculate_leafesmins(h, J)
        else:
            # TODO: Potential Fan out
            cesmins=[]
            logging.info("Calculating min ES on Node {} with {} children".format(self.id, len(self.nodes)))
            for nid, node in self.nodes.items():
                cesmins.append(node.calculate_esmins(hdict, Jdict))
            logging.info("Node {} Children Results {}".format(self.id, cesmins))
            # TODO: Aggregate
            res=(0,0)
            for nesmin, pesmin in cesmins:
                res=(res[0]+nesmin[0], res[1]+pesmin[0])
            logging.info("Node {} Children Sum(-1)={} Sum(1)={}".format(self.id, res[0], res[1]))
            # (if I am S=-1 E_subtree is here, if I am S=1 E_subtree is here)
            # (Add in parent edge energy to calculate two possible minimums)
            if self.pid is None:
                h=hdict[self.id]
                logging.info("Root params for Node {} are h={}".format(self.id, h))
                self.esmins = (res[0] - h, -1),(res[1] + h, +1)
                logging.info("Root Node {} Minimum energies/spins for parent sigma=-1,1 are {}".format(self.id, self.esmins))
            else:
                pJ=Jdict[self.id][self.pid]
                h=hdict[self.id]
                logging.info("Branch Node params for Node {} with parent {} are h={} and J={}".format(self.id, self.pid, h, pJ))
                En = ((res[1] + h - pJ, 1) , (res[0] - h + pJ, -1)) # i=1, sigma=-1; i=-1, sigma=-1
                Ep = ((res[1] + h + pJ, 1), (res[0] - h - pJ, -1)) # i=1, sigma=1; i=-1, sigma=1
                self.esmins = (min(En), min(Ep)) # Tuple of minimum energy, spin tuples for sigma=(-1,1)
                logging.info("Branch Node {} Minimum energies/spins for parent sigma=-1,1 are {}".format(self.id, self.esmins))
        return self.esmins

    def set_minE_spin(self, spindict, pspin=None):
        """
        Set the minimum energy for a sub-tree and this node's spin
        Inputs - spindict: Dictionary to capture spins
                 psin: Parent spin (None for root node)
        Output - minimum energy of subtree
        """
        if self.pid is None:
            self.emin, self.spin = min(self.esmins)
            logging.info("Minimum for Root Node {} E={} S={}".format(self.id,self.emin, self.spin))
        else:
            if pspin == -1:
                self.emin, self.spin = self.esmins[0]
            elif pspin == 1:
                self.emin, self.spin = self.esmins[1]
            else:
                ValueError("Spin not valid")
        logging.info("Minimum for Node {} E={} S={}".format(self.id, self.emin, self.spin))
        for nid, node in self.nodes.items():
            node.set_minE_spin(spindict, pspin=self.spin)
        spindict[self.id]=self.spin
        return self.emin

    def _calculate_leafesmins(self, h, J):
        """
        Calculate the E(v,sigma) and S(v,sigma) for a leaf
        Inputs - h for this leaf, J for this leaf to it's parent
        Outputs - ((Emin(sigma=-1),Smin(sigma=-1)),(Emin(sigma=+1),Smin(sigma=+1)))
        Note: This will prefer the -1 spin in the event of a degenerate minimum
        """
        logging.info("Calculating min ES on Node {} as a Leaf".format(self.id))
        logging.info("Calculating leaf spin energy using {} * i + {} * i * j".format(h,J))
        En = [ (h - J, 1) , (-h + J, -1) ] # i=1, sigma=-1; i=-1, sigma=-1
        Ep = [ (h + J, 1), (-h - J, -1) ] # i=1, sigma=1; i=-1, sigma=1
        logging.debug("En {}".format(En))
        logging.debug("Ep {}".format(Ep))
        logging.info("Results for sigma_j=-1, i={} is {}, i={} is {}".format(En[0][1],En[0][0],En[1][1],En[1][0]))
        logging.info("Results for sigma_j=1, i={} is {}, i={} is {}".format(Ep[0][1],Ep[0][0],Ep[1][1],Ep[1][0]))
        esmins = (min(En), min(Ep)) # Tuple of minimum energy, spin tuples for sigma=(-1,1)
        logging.info("Minimum energies/spins for sigma=-1,1 are {} ".format(esmins))
        return esmins

    def __repr__(self):
        return f"Node({self.id}): {self.nodes}"

class Data:
    """
    Class to hold data about the running Problem
    """
    def __init__(self, name, nnodes, nweights):
        self.name = name
        self.nnodes = nnodes
        self.nweights = nweights
