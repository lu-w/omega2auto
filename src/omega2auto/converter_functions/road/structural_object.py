from ..utils import *


@monkeypatch(omega_format.StructuralObject)
def to_auto(cls, scenery, identifier=None, parent_identifier=None):

    # Fetches ontologies
    ph = scenery.ontology(auto.Ontology.Physics)
    l2_core = scenery.ontology(auto.Ontology.L2_Core)
    l2_de = scenery.ontology(auto.Ontology.L2_DE)
    l3_de = scenery.ontology(auto.Ontology.L3_DE)

    # Creates structural object instance
    structural_object = ph.Spatial_Object()
    structural_object.identifier = str(parent_identifier) + "_" + str(identifier)

    if cls.type == omega_format.ReferenceTypes.StructuralObjectType.VEGETATION:
        structural_object.is_a.append(l2_core.Road_Side_Vegetation)
    elif cls.type == omega_format.ReferenceTypes.StructuralObjectType.BUILDING:
        structural_object.is_a.append(l2_de.Building)
    elif cls.type == omega_format.ReferenceTypes.StructuralObjectType.BUS_SHELTER:
        structural_object.is_a.append(l2_de.Bus_Stop)
    elif cls.type == omega_format.ReferenceTypes.StructuralObjectType.TUNNEL:
        structural_object.is_a.append(l2_de.Tunnel)
    elif cls.type == omega_format.ReferenceTypes.StructuralObjectType.BRIDGE:
        structural_object.is_a.append(l2_de.Bridge)
    elif cls.type == omega_format.ReferenceTypes.StructuralObjectType.FENCE:
        structural_object.is_a.append(l2_de.Fence)
    elif cls.type == omega_format.ReferenceTypes.StructuralObjectType.BENCH:
        structural_object.is_a.append(l2_de.Bench)
    elif cls.type == omega_format.ReferenceTypes.StructuralObjectType.ROAD_WORK:
        structural_object.is_a.append(l3_de.Construction_Site)
    elif cls.type == omega_format.ReferenceTypes.StructuralObjectType.BODY_OF_WATER:
        structural_object.is_a.append(l2_core.Water_Body)
    elif cls.type == omega_format.ReferenceTypes.StructuralObjectType.GARAGE:
        structural_object.is_a.append(l2_de.Garage)
    elif cls.type == omega_format.ReferenceTypes.StructuralObjectType.BILLBOARD:
        structural_object.is_a.append(l2_de.Billboard)
    elif cls.type == omega_format.ReferenceTypes.StructuralObjectType.ADVERTISING_PILLAR:
        structural_object.is_a.append(l2_de.Advertising_Pillar)
    elif cls.type == omega_format.ReferenceTypes.StructuralObjectType.PHONE_BOX:
        structural_object.is_a.append(l2_de.Phone_Box)
    elif cls.type == omega_format.ReferenceTypes.StructuralObjectType.POST_BOX:
        structural_object.is_a.append(l2_de.Post_Box)
    elif cls.type == omega_format.ReferenceTypes.StructuralObjectType.OVERHEAD_STRUCTURE:
        structural_object.is_a.append(l2_de.Overhead_Traffic_Structure)

    structural_object.has_height = float(cls.height)

    add_geometry_from_polygon(cls, structural_object, scenery)

    add_layer_3_information(cls, structural_object, scenery)

    return [(cls, [structural_object])]
