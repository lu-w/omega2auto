import math
import os
import tempfile

import numpy as np
import pyauto.visualizer.visualizer
from pyauto import auto
from pyauto.models.scenario import Scenario
from pyauto.models.scene import Scene
from pyauto.models.scenery import Scenery

import omega_format
from omega2auto.converter_functions.utils import *
from omega2auto.converter_functions.dynamics.road_user import *
from omega2auto.converter_functions.dynamics.misc_object import *
from omega2auto.converter_functions.weather.weather import *
from omega2auto.converter_functions.road.road import *
from omega2auto.converter_functions.road.road_object import *
from omega2auto.converter_functions.road.sign import *
from omega2auto.converter_functions.road.state import *
from omega2auto.converter_functions.road.boundary import *
from omega2auto.converter_functions.road.structural_object import *
from omega2auto.converter_functions.road.flat_marking import *
from omega2auto.converter_functions.road.lane import *
from omega2auto.converter_functions.road.lateral_marking import *

# Logging
logger = logging.getLogger(__name__)


def _load_hdf5(omega_file="inD.hdf5"):
    """
    Loads OMEGA HDF5 from the given file location.
    :param omega_file: The path to the OMEGA HDF5 file.
    :return: The ReferenceRecording instance.
    """
    logger.debug("Loading OMEGA file " + str(omega_file))
    rr = omega_format.ReferenceRecording.from_hdf5(filename=omega_file)
    logger.debug("Finished loading OMEGA file")
    return rr


def _add_identity_information(instance_tuples):
    """
    Adds the identity relation that tracks same objects over multiple scenes based on the information returned by the
    `to_auto` functions.
    :param instance_tuples: A list of tuples with the first entry being a OMEGA object, the second one begin a list of
    corresponding OWL individuals representing the first entry. Each time iteration, the same list sorting of the second
    entry is expected.
    """
    for rr_inst, owl_inst in instance_tuples:
        for i, inst in enumerate(owl_inst):
            try:
                inst.identical_to = [rr_inst.last_owl_instance[i]]
            except AttributeError:
                pass
        setattr(rr_inst, "last_owl_instance", owl_inst)


def _get_speed_limit(rr: omega_format.ReferenceRecording) -> int or None:
    """
    Returns the speed limit in the given reference recording or None if the speed limit can not be determined.
    Determination works via a simple lookup of known locations and speed limits.
    :param rr: The reference recording
    """
    if math.isclose(rr.meta_data.reference_point_lat, 50.78563844942432) and \
            math.isclose(rr.meta_data.reference_point_lon, 6.128973907195158):
        # Charlottenburger Allee - Neuköllner Str. (Location 4)
        return 50
    elif math.isclose(rr.meta_data.reference_point_lat, 50.779082542457765) and \
            math.isclose(rr.meta_data.reference_point_lon, 6.164784245039574):
        # Von-Coels-Str. - Heckstr. (Location 3)
        return 50
    elif math.isclose(rr.meta_data.reference_point_lat, 50.768629564172194) and \
            math.isclose(rr.meta_data.reference_point_lon, 6.101500261218432):
        # Bismarckstr. - Schlossstr. (Location 2)
        return 30
    elif math.isclose(rr.meta_data.reference_point_lat, 50.78232943792871) and \
            math.isclose(rr.meta_data.reference_point_lon, 6.070376552691796):
        # Süsterfeldstr. - Kühlwetterstr. (Location 1)
        return 50
    return None


def _to_auto(rr: omega_format.ReferenceRecording, hertz: int = None, start_offset=0, end_offset=0,
             folder="pyauto/auto", cp=False) -> Scenario:
    """
    Main converter function - converts all instances within the reference recording to A.U.T.O. instances. Uses the
    monkey-patched converter functions.
    :param rr: The reference recording to convert from.
    :param hertz: An optional sampling rate (so that recordings can be down sampled when loading into A.U.T.O.)
        Note: The recording's sampling rate *has* to be a multiple of this sampling rate, if given.
    :param start_offset: The offset to start sampling the scenarios from (in s).
    :param end_offset: The offset to end sampling the scenarios from (in s).
    :param folder: The path to the folder in which A.U.T.O. is located.
    :param cp: Whether to also load the two criticality phenomena ontologies (needed for criticality inference).
    """
    snippet_start = rr.timestamps.val[0] + start_offset
    snippet_end = rr.timestamps.val[-1] - end_offset
    if snippet_start >= snippet_end:
        logger.warning("Invalid snippet start / end offsets. Defaulting to 0.")
        snippet_start = rr.timestamps.val[0]
        snippet_end = rr.timestamps.val[-1]
    rr_hz = int(1 / (rr.timestamps.val[1] - rr.timestamps.val[0]))
    if not hertz:
        hertz = rr_hz

    logger.debug("Loading scenario from " + str(str(snippet_start)) + "s - " + str(str(snippet_end)) + "s")

    speed_limit = _get_speed_limit(rr)

    # Convert static infrastructure
    logger.debug("Converting " + str(len(rr.roads.values())) + " roads")
    scenery = Scenery(load_cp=cp, folder=folder)
    for i, road in enumerate(rr.roads.values()):
        road.to_auto(scenery, i)

    scenes = []
    for scene_number in np.arange(snippet_start * rr_hz, snippet_end * rr_hz, round(rr_hz / hertz)):
        scene_number = int(scene_number)
        t = scene_number / rr_hz

        logger.debug("Scene " + str(scene_number + 1) + " (" + str(t) + "s) / " + str(len(rr.timestamps.val)))

        # Note: already passing scenery here. If we do it later, we might create clashes with individual names.
        scene = Scene(timestamp=float(t), folder=folder, load_cp=cp, scenery=scenery)
        scenes.append(scene)
        scene.has_speed_limit = speed_limit

        converted_rr_entities = []

        # Convert road users and ego vehicle
        road_users_s = [x for x in {k: v for k, v in rr.road_users.items()}.items() if
                        x[1].birth <= scene_number <= x[1].end]
        if rr.ego_vehicle.birth <= scene_number <= rr.ego_vehicle.end:
            road_users_s.append((rr.ego_vehicle.id, rr.ego_vehicle))
        logger.debug("Converting " + str(len(road_users_s)) + " road users")
        for i, road_user in road_users_s:
            user_instances = road_user.to_auto(scene, scene_number, i)
            converted_rr_entities += user_instances
            road_user.owl_entity = user_instances
            _add_identity_information(user_instances)

        # Convert misc objects
        misc_objects_s = [x for x in {k: v for k, v in rr.misc_objects.items()}.items() if
                          x[1].birth <= scene_number <= x[1].end]
        logger.debug("Converting " + str(len(misc_objects_s)) + " misc entities")
        for i, misc in misc_objects_s:
            misc_instances = misc.to_auto(scene, scene_number, i)
            converted_rr_entities += misc_instances
            _add_identity_information(misc_instances)

        # Convert traffic sign states
        logger.debug("Converting " + str(len(rr.states.values())) + " traffic sign states")
        for traffic_sign_state in rr.states.values():
            state_s = traffic_sign_state.values[scene_number]
            state_instances = state_s.to_auto(scene, scene_number)
            converted_rr_entities += state_instances
            _add_identity_information(state_instances)

        # Convert weather
        if rr.weather is not None:
            logger.debug("Converting weather")
            weather_instances = rr.weather.to_auto(scene, scene_number)
            converted_rr_entities += weather_instances
            _add_identity_information(weather_instances)
        else:
            logger.debug("No weather information present in recording")

        # Set correct relations between created entities in case those were not settable during time of creation
        for i, entity in converted_rr_entities:
            if hasattr(entity[0], "owl_relations"):
                for rel in entity[0].owl_relations:
                    if rel[1] == "connected_to":
                        rel[0].connected_to = entity.last_owl_instance
                entity.owl_relations = []

    # Extra iteration over all scenes for sign states as they can only be created after road infrastructure
    for scene_number, scene in enumerate(scenes):
        for sign_state in rr.states.values():
            sign_state.to_auto(scene, scene_number)

    # Final step: Set references to relations correctly
    for rr_inst in list(rr.road_users.values()) + list(rr.misc_objects.values()) + list(rr.roads.values()) + \
                   list(rr.states.values()) + list(rr.states.values()) + [l for ll in rr.roads.values() for l in ll]:
        instantiate_relations(rr_inst)

    logger.debug("Finished converting OMEGA to OWL")
    return Scenario(scenes=scenes, scenery=scenery, folder=folder, load_cp=cp)


def convert(omega_file="inD.hdf5", folder="pyauto/auto", cp=False, scenarios=None, hertz=None, start_offset=0,
            end_offset=0, max_scenario_duration=None) -> list:
    """
    Main entry function for OMEGA to A.U.T.O. conversion.
    :param omega_file: the HDF5 file to load the OMEGA data from.
    :param folder: The path to the folder in which A.U.T.O. is located.
    :param cp: Whether to also load the two criticality phenomena ontologies (needed for criticality inference).
    :param scenarios: An optional list of scenario IDs (as integers) which shall be selected. The rest is then ignored.
    :param hertz: The sampling rate (in Hertz) to which scenarios are reduced. Default is using the fully sampling rate
        of the recording.
    :param start_offset: The offset to start sampling the scenarios from (in s).
    :param end_offset: The offset to end sampling the scenarios from (in s).
    :param max_scenario_duration: The maximum duration (in s) of a scenario - longer scenarios are ignored
    :return: The scenarios as extracted by the OMEGA library from the HDF5 file as a list of owlready2 worlds.
    """
    if start_offset is None:
        start_offset = 0
    if end_offset is None:
        end_offset = 0
    loaded_scenarios = []
    omega_data = _load_hdf5(omega_file)
    logger.debug("Extracting snippets from OMEGA file")
    # TODO revert once omega_format master has been updated
    try:
        omega_snippets = omega_data.extract_snippets(ids=scenarios)
        if max_scenario_duration is not None:
            omega_snippets = list(filter(
                lambda x: (x.timestamps.val[-1] - x.timestamps.val[0]) <= max_scenario_duration, omega_snippets))
    except AssertionError:
        omega_snippets = [omega_data]
    snippets_len = len(omega_snippets)
    for i, rr in enumerate(omega_snippets):
        logger.debug("Creating OWL worlds for snippet " + str(i) + "/" + str(snippets_len))
        snippet_scenario = _to_auto(rr, hertz=hertz, start_offset=start_offset, end_offset=end_offset, folder=folder,
                                    cp=cp)
        loaded_scenarios.append(snippet_scenario)
    return loaded_scenarios
