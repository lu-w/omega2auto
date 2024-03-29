from ..utils import *


@monkeypatch(omega_format.Road)
def to_auto(cls, scenery: Scenery, identifier=None):

    # Fetches ontologies
    geo = scenery.ontology(auto.Ontology.GeoSPARQL)
    l1_core = scenery.ontology(auto.Ontology.L1_Core)
    l1_de = scenery.ontology(auto.Ontology.L1_DE)

    # Creates road instance
    road = l1_core.Road()
    road.identifier = identifier
    parent_id = "road" + str(identifier)

    # Stores road type
    if cls.location == omega_format.ReferenceTypes.RoadLocation.URBAN:
        road.is_a.append(l1_de.Urban_Road)
    elif cls.location == omega_format.ReferenceTypes.RoadLocation.NON_URBAN:
        road.is_a.append(l1_de.Rural_Road)
    elif cls.location == omega_format.ReferenceTypes.RoadLocation.HIGHWAY:
        road.is_a.append(l1_de.Highway_Road)

    instances = []
    # Creates lane instances
    road_geom = None
    if len(cls.lanes.values()) > 0:
        wkt_string = "MULTIPOLYGON ("
        lane_instances = []
        for i, lane in enumerate(cls.lanes.values()):
            lane_insts = lane.to_auto(scenery, i, parent_id + "_0")
            instances += lane_insts
            lane_inst = lane_insts[0][1][0]
            lane_instances.append((lane, [lane_inst]))
            road.has_lane.append(lane_inst)
            lane_inst.has_road = road
            wkt_string += lane_inst.hasGeometry[0].asWKT[0].replace("POLYGON ", "") + ", "
            road.has_road_material += lane_inst.has_lane_material

        # Stores geometry of road as conjunction of lane polygons
        wkt_string = wkt_string[:-2] + "))"
        road_geom = wkt.loads(wkt_string)
        # Fix invalid roads (multipolygon may intersect itself due to taking the union of all lanes)
        if not road_geom.is_valid:
            road_geom = road_geom.buffer(0)
        road_geometry = geo.Geometry()
        road_geometry.asWKT = [str(road_geom)]
        road.hasGeometry = [road_geometry]
    else:
        logger.warning("Found a road with no lane instances")

    # Add lateral markers
    for i, marker in enumerate(cls.lateral_markings.data.values()):
        marker_inst = marker.to_auto(scenery, i, parent_id + "_1", road_geom)
        marker_inst[0][1][0].applies_to.append(road)
        instances += marker_inst

    # Add structural objects
    for i, structural_object in enumerate(cls.structural_objects.data.values()):
        struct_inst = structural_object.to_auto(scenery, i, parent_id + "_2")
        instances += struct_inst

    # Add road objects
    for i, road_object in enumerate(cls.road_objects.data.values()):
        obj_inst = road_object.to_auto(scenery, i, parent_id + "_3")
        instances += obj_inst

    # Add signs
    for i, sign in enumerate(cls.signs.data.values()):
        sign_inst = sign.to_auto(scenery, i, parent_id + "_4")
        instances += sign_inst

    instances.append((cls, [road]))
    return instances
