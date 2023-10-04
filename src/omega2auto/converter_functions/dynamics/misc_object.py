from ..utils import *


@monkeypatch(omega_format.MiscObject)
def to_auto(cls, scene: Scene, scene_number: int, identifier=None):
    s = scene_number - cls.birth
    mo = scene.ontology(auto.Ontology.Physics).Spatial_Object()
    mo.identifier = identifier
    mo.identifier = cls.id
    # Store type and sub_type
    # We ignore 'misc' type and do not set any specific subclass (open world assumption)
    l4_de = scene.ontology(auto.Ontology.L4_DE)
    l4_core = scene.ontology(auto.Ontology.L4_Core)
    if cls.type == omega_format.ReferenceTypes.MiscObjectType.ANIMAL:
        mo.is_a.append(l4_core.Animal)
        if cls.sub_type == omega_format.ReferenceTypes.MiscObjectSubType.DOG:
            mo.is_a.append(l4_de.Dog)
        elif cls.sub_type == omega_format.ReferenceTypes.MiscObjectSubType.CAT:
            mo.is_a.append(l4_de.Cat)
        elif cls.sub_type == omega_format.ReferenceTypes.MiscObjectSubType.BIRD:
            mo.is_a.append(l4_de.Bird)
        elif cls.sub_type == omega_format.ReferenceTypes.MiscObjectSubType.HORSE:
            mo.is_a.append(l4_de.Horse)
        elif cls.sub_type == omega_format.ReferenceTypes.MiscObjectSubType.WILD:
            mo.is_a.append(l4_de.Deer)
    elif cls.type == omega_format.ReferenceTypes.RoadUserType.TRUCK:
        mo.is_a.append(l4_de.Playing_Equipment)
    # Store physical properties
    add_physical_properties(cls, mo, s)
    # Store bounding box
    add_bounding_box(cls, mo)
    # Store geometrical properties
    add_geometry_from_trajectory(cls, mo, s, scene)
    return [(cls, [mo])]
