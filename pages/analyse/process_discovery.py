import warnings
import dms.dms
from utils.constants import UPLOAD_DIRECTORY
import os

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from ocpa.objects.log.importer.ocel import factory as ocel_import_factory
    from ocpa.algo.discovery.ocpn import algorithm as ocpn_discovery_factory
    from ocpa.visualization.oc_petri_net import factory as ocpn_vis_factory
    from pm4py.visualization.ocel.ocpn import visualizer as ocpn_visualizer
    from pm4py.visualization.ocel.ocdfg import visualizer as ocdfg_visualizer

import pm4py
from pm4py.util import constants
from pm4py.objects.ocel.constants import OCEL_GLOBAL_EVENT

from app import log_management

def ocpa_discover():
    ocel = log_management.get_ocel()
    singleton_instance = dms.dms.SingletonClass()
    key = singleton_instance.selected
    filename = os.path.join(UPLOAD_DIRECTORY, key.rpartition('.jsonocel')[0] + '_temporary.jsonocel')
    pm4py.write_ocel(ocel, filename)
    ocel = ocel_import_factory.apply(filename)
    ocpn = ocpn_discovery_factory.apply(ocel, parameters={"debug": False})
    ocpn_vis_factory.save(ocpn_vis_factory.apply(ocpn), "data/results/oc_petri_net_ocpa.png")
    dot = ocpn_vis_factory.apply(ocpn).source
    return dot

def pm4py_discover():
    ocel = log_management.get_ocel()
    ocpn = pm4py.discover_oc_petri_net(ocel)
    pm4py.save_vis_ocpn(ocpn, "data/results/oc_petri_net_pm4py.png")
    from pm4py.visualization.ocel.ocpn import visualizer as ocpn_visualizer
    gviz = ocpn_visualizer.apply(ocpn)
    dot = gviz.source
    return dot

def dfg_discover():
    ocel = log_management.get_ocel()
    ocpn = pm4py.discover_ocdfg(ocel)
    pm4py.save_vis_ocdfg(ocpn, "data/results/oc_dfg_pm4py.png")
    from pm4py.visualization.ocel.ocdfg import visualizer as ocdfg_visualizer
    gviz = ocdfg_visualizer.apply(ocpn)
    dot = gviz.source
    return dot