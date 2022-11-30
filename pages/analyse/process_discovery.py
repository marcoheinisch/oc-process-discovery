from ocpa.objects.log.importer.ocel import factory as ocel_import_factory
from ocpa.algo.discovery.ocpn import algorithm as ocpn_discovery_factory
from ocpa.visualization.oc_petri_net import factory as ocpn_vis_factory

import pm4py
from pm4py.util import constants
from pm4py.objects.ocel.constants import OCEL_GLOBAL_EVENT

# datamanagement should be done by Pedro I think
# from datamanagement import ocel

def ocpa_discover():
    # delete those two lines later on (only for testing purposes until a proper ocel extraction and data management interfaces are in place
    filename="data/resources/order_process.jsonocel"
    ocel = ocel_import_factory.apply(file_path=filename)
    ocpn = ocpn_discovery_factory.apply(ocel, parameters={"debug": False})
    ocpn_vis_factory.save(ocpn_vis_factory.apply(ocpn), "data/results/oc_petri_net_ocpa.png")
    dot = ocpn_vis_factory.apply(ocpn).source
    return dot

def pm4py_discover():
    # delete those two lines later on (only for testing purposes until a proper ocel extraction and data management interfaces are in place
    print(1)
    filename = "data/resources/order_process.jsonocel"
    print(2)
    ocel = pm4py.read_ocel(file_path=filename)
    print(3)
    ocpn = pm4py.discover_oc_petri_net(ocel)
    print(4)
    pm4py.save_vis_ocpn(ocpn, "data/results/oc_petri_net_pm4py.png")
    print(5)
    from pm4py.visualization.ocel.ocpn import visualizer as ocpn_visualizer
    print(6)
    gviz = ocpn_visualizer.apply(ocpn)
    print(7)
    dot = gviz.source
    print(8)
    return dot