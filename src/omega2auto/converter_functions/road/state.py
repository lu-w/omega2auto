from ..utils import *


@monkeypatch(omega_format.State)
def to_auto(cls, scene: Scene, scene_number: int):

    # Fetches ontologies
    l6_core = scene.ontology(auto.Ontology.L6_Core)
    l6_de = scene.ontology(auto.Ontology.L6_DE)

    owl_instance = cls.sign.last_owl_instance[0]

    if scene_number < len(cls.value):
        state = l6_core.Traffic_Light_State()
        owl_instance.delivers_signal.append(state)
        sign_value = int(cls.value[scene_number])
        if sign_value == omega_format.ReferenceTypes.StateValue.GREEN:
            state.is_a.append(l6_de.Green_Light)
        elif sign_value == omega_format.ReferenceTypes.StateValue.AMBER:
            state.is_a.append(l6_de.Amber_Light)
        elif sign_value == omega_format.ReferenceTypes.StateValue.RED:
            state.is_a.append(l6_de.Red_Light)
        elif sign_value == omega_format.ReferenceTypes.StateValue.RED_AMBER:
            state.is_a.append(l6_de.Red_Amber_Light)
        elif sign_value == omega_format.ReferenceTypes.StateValue.FLASHING_AMBER:
            state.is_a.append(l6_de.Flashing_Light)
            state.is_a.append(l6_de.Amber_Light)
        elif sign_value == omega_format.ReferenceTypes.StateValue.FLASHING_RED:
            state.is_a.append(l6_de.Flashing_Light)
            state.is_a.append(l6_de.Red_Light)
        elif sign_value == omega_format.ReferenceTypes.StateValue.GREEN_ARROW:
            state.is_a.append(l6_de.Green_Arrow_Light)
        elif sign_value == omega_format.ReferenceTypes.StateValue.RED_CROSS:
            state.is_a.append(l6_de.Red_Cross_Light)
        elif sign_value == omega_format.ReferenceTypes.StateValue.AMBER_DIAGONAL_ARROW_RIGHT:
            state.is_a.append(l6_de.Amber_Diagonal_Arrow_Right)
        elif sign_value == omega_format.ReferenceTypes.StateValue.AMBER_DIAGONAL_ARROW_LEFT:
            state.is_a.append(l6_de.Amber_Diagonal_Arrow_Left)
        elif sign_value == omega_format.ReferenceTypes.StateValue.ACTIVE:
            state.is_a.append(l6_de.Active_Signal)
        elif sign_value == omega_format.ReferenceTypes.StateValue.INACTIVE:
            state.is_a.append(l6_de.Inactive_Signal)
        elif sign_value == omega_format.ReferenceTypes.StateValue.BUS_STOP:
            state.is_a.append(l6_de.Bus_Stop_Light)
        elif sign_value == omega_format.ReferenceTypes.StateValue.BUS_STRAIGHT:
            state.is_a.append(l6_de.Bus_Straight_Light)
        elif sign_value == omega_format.ReferenceTypes.StateValue.BUS_RIGHT:
            state.is_a.append(l6_de.Bus_Right_Light)
        elif sign_value == omega_format.ReferenceTypes.StateValue.BUS_LEFT:
            state.is_a.append(l6_de.Bus_Left_Light)
        elif sign_value == omega_format.ReferenceTypes.StateValue.BUS_STOP_EXPECTED:
            state.is_a.append(l6_de.Bus_Stop_Expected_Light)
        elif sign_value == omega_format.ReferenceTypes.StateValue.BUS_YIELD:
            state.is_a.append(l6_de.Bus_Yield_Light)
        elif sign_value == omega_format.ReferenceTypes.StateValue.BUS_WILL_SWITCH:
            state.is_a.append(l6_de.Bus_Switch_Light)
        return [(cls, [state])]
    else:
        return [(cls, [])]
