import json
from os import error
from pprint import pprint


import dace
from dace.codegen.instrumentation.papi import MapEntry
from dace.codegen.instrumentation.provider import SDFG
from dace.sdfg.nodes import AccessNode, EntryNode
from dace.transformation.passes.symbol_propagation import SDFGState
from dace.sdfg.nodes import Node


type StateAlloc = dict[AccessNode,list[SDFGState]]
type NodeAlloc = dict[AccessNode, list[Node]]



def create_allocation_report(to : dict[SDFG | SDFGState | EntryNode, list[tuple[SDFG, SDFGState | None,AccessNode | None, bool, bool, bool]]]):

    #state_alloc: dict[AccessNode,list[SDFGState]] = {}
    #node_alloc: dict[AccessNode, list[Node]] = {}

    state_alloc: dict[str, list[str]] = {}
    node_alloc: dict[str, list[str]] = {}

    all_alloc: dict[str, list[str]] = {}

    report: dict[SDFG, dict[str, list[str]]] = {}

    pprint(to)
    for scope in to:
        print(scope)
        for alloc_info in to[scope]:

            sdfg: SDFG = alloc_info[0]
            print(sdfg.build_folder)
            state : SDFGState | None = alloc_info[1]
            access_node =alloc_info[2]

            nodes_allocated: list[Node] = []
            states_allocated: list[SDFGState] = []

            if issubclass(type(scope),SDFG):
                #TODO: find example where SDFG is the scope and implement
                pass
            elif issubclass(type(scope),SDFGState):
                #highlight all nodes and the state itself
                nodes_allocated = list(scope.nodes()) if isinstance(scope, SDFGState) else []
                states_allocated = [scope] if isinstance(scope, SDFGState) else []
            elif issubclass(type(scope),EntryNode):
                print("entry")
                #highlight only map entry + exit nodes and the contained nodes
                if isinstance(scope, MapEntry):
                    #list all nodes inside Map + entry and exit nodes
                    nodes_allocated = []
                    scope_dict = state.scope_dict() if state != None else {}
                    for node in state.nodes() if state != None else []:
                        if scope_dict[node] == scope or node == scope:
                            nodes_allocated.append(node)

                    #if state containing map should also be highlighted
                    #states_allocated = [state]
                    print("\n\n")

            if access_node != None:
                state_alloc[access_node.guid] = [state.guid for state in states_allocated]
                node_alloc[access_node.guid] = [node.guid for node in nodes_allocated]
                all_alloc[access_node.guid] = state_alloc[access_node.guid] + node_alloc[access_node.guid]
                if sdfg in report.keys():
                    report[sdfg].update(all_alloc)
                else:
                    report[sdfg] = all_alloc

    pprint(state_alloc)
    pprint(node_alloc)
    pprint(report)

    for sdfg in report:
        with open(f"{sdfg.build_folder}/perf/allocation-report-{str(hash(str(report[sdfg])))}.json", "x") as f:
            json.dump(report[sdfg],f)





    return
