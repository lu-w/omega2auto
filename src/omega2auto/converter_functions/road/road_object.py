from ..utils import *


@monkeypatch(omega_format.RoadObject)
def to_auto(cls, scenery: Scenery, identifier=None, parent_identifier=None):

    # Fetches ontologies
    ph = scenery.ontology(auto.Ontology.Physics)
    l1_core = scenery.ontology(auto.Ontology.L1_Core)
    l1_de = scenery.ontology(auto.Ontology.L1_DE)
    l2_de = scenery.ontology(auto.Ontology.L2_DE)
    l5_de = scenery.ontology(auto.Ontology.L5_DE)

    # Creates road object instance
    road_object = ph.Spatial_Object()
    road_object.identifier = str(parent_identifier) + "_" + str(identifier)

    if cls.type == omega_format.ReferenceTypes.RoadObjectType.STREET_LAMP:
        road_object.is_a.append(l2_de.Street_Light)
    elif cls.type == omega_format.ReferenceTypes.RoadObjectType.TRAFFIC_ISLAND:
        road_object.is_a.append(l1_de.Traffic_Island)
    elif cls.type == omega_format.ReferenceTypes.RoadObjectType.ROUNDABOUT_CENTER:
        road_object.is_a.append(l1_de.Roundabout_Center)
    elif cls.type == omega_format.ReferenceTypes.RoadObjectType.PARKING:
        road_object.is_a.append(l2_de.Parking_Space)
    elif cls.type == omega_format.ReferenceTypes.RoadObjectType.CROSSING_AID:
        road_object.is_a.append(l1_de.Traffic_Island)
    elif cls.type == omega_format.ReferenceTypes.RoadObjectType.SPEED_BUMP:
        road_object.is_a.append(l1_de.Speed_Bump)
    elif cls.type == omega_format.ReferenceTypes.RoadObjectType.POT_HOLE:
        road_object.is_a.append(l1_de.Pothole)
    elif cls.type == omega_format.ReferenceTypes.RoadObjectType.REFLECTOR:
        road_object.is_a.append(l1_de.Reflecting_Guidance_System)
    elif cls.type == omega_format.ReferenceTypes.RoadObjectType.STUD:
        road_object.is_a.append(l1_de.Raised_Pavement_Marker)
    elif cls.type == omega_format.ReferenceTypes.RoadObjectType.BOLLARD:
        road_object.is_a.append(l2_de.Bollard)
    elif cls.type == omega_format.ReferenceTypes.RoadObjectType.CRASH_ABSORBER:
        road_object.is_a.append(l2_de.Impact_Attenuator)
    elif cls.type == omega_format.ReferenceTypes.RoadObjectType.BITUMEN:
        road_object.is_a.append(l1_de.Bitumen_Repair)
    elif cls.type == omega_format.ReferenceTypes.RoadObjectType.MANHOLE_COVER:
        road_object.is_a.append(l1_de.Manhole_Cover)
    elif cls.type == omega_format.ReferenceTypes.RoadObjectType.GRATING:
        road_object.is_a.append(l1_de.Grating)
    elif cls.type == omega_format.ReferenceTypes.RoadObjectType.RUT:
        road_object.is_a.append(l1_de.Rut)
    elif cls.type == omega_format.ReferenceTypes.RoadObjectType.PUDDLE:
        road_object.is_a.append(l5_de.Rain_Puddle)

    if cls.walkable:
        road_object.is_a.append(l1_core.Walkable_Road_Element)
    else:
        road_object.is_a.append(l1_core.Non_Walkable_Road_Element)

    if cls.drivable:
        road_object.is_a.append(l1_core.Driveable_Road_Element)
    else:
        road_object.is_a.append(l1_core.Non_Driveable_Road_Element)

    road_object.has_height = float(cls.height)
    add_geometry_from_polygon(cls, road_object, scenery)

    add_layer_3_information(cls, road_object, scenery)

    return [(cls, [road_object])]
