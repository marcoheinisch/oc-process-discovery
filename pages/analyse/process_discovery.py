from ocpa.objects.log.importer.ocel import factory as ocel_import_factory
from ocpa.algo.discovery.ocpn import algorithm as ocpn_discovery_factory
from ocpa.visualization.oc_petri_net import factory as ocpn_vis_factory

from pm4py.visualization.common.gview import matplotlib_view
import graphviz.rendering

# datamanagement should be done by Pedro I think
# from datamanagement import ocel

def ocpa_discover():
    # delete those two lines later on (only for testing purposes until a proper ocel extraction and data management interfaces are in place
    filename="test/resources/order_process.jsonocel"
    ocel = ocel_import_factory.apply(file_path=filename)
    ocpn = ocpn_discovery_factory.apply(ocel, parameters={"debug": False})
    ocpn_vis_factory.save(ocpn_vis_factory.apply(ocpn), "test/results/oc_petri_net.png")
    dot = ocpn_vis_factory.apply(ocpn).source
    return dot

def pm4py_discover():
    # TODO
    pass