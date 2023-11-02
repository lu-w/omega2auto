from ..utils import *


@monkeypatch(omega_format.Weather)
def to_auto(cls, scene: Scene, scene_number: int):

    # Fetches ontologies
    ph = scene.ontology(auto.Ontology.Physics)
    l1_core = scene.ontology(auto.Ontology.L1_Core)
    l3_de = scene.ontology(auto.Ontology.L3_DE)
    l5_de = scene.ontology(auto.Ontology.L5_DE)
    l5_core = scene.ontology(auto.Ontology.L5_Core)

    environment = l5_core.Environment()

    # precipitation
    # - type
    if scene_number < len(cls.precipitation.type):
        if cls.precipitation.type[scene_number] == omega_format.ReferenceTypes.Precipitation.NO_RAIN:
            environment.is_a.append(l5_de.No_Precipitation_Environment)
        else:
            precipitation = l5_core.Precipitation()
            environment.consists_of.append(precipitation)
            if cls.precipitation.type[scene_number] == omega_format.ReferenceTypes.Precipitation.LIGHT_RAIN:
                precipitation.is_a.append(l5_de.Light_Rain)
            elif cls.precipitation.type[scene_number] == omega_format.ReferenceTypes.Precipitation.MODERATE_RAIN:
                precipitation.is_a.append(l5_de.Moderate_Rain)
            elif cls.precipitation.type[scene_number] == omega_format.ReferenceTypes.Precipitation.HEAVY_RAIN:
                precipitation.is_a.append(l5_de.Heavy_Rain)
            elif cls.precipitation.type[scene_number] == omega_format.ReferenceTypes.Precipitation.EXTREMELY_HEAVY_RAIN:
                precipitation.is_a.append(l5_de.Extremely_Haivy_Rain)
            elif cls.precipitation.type[scene_number] == omega_format.ReferenceTypes.Precipitation.LIGHT_SNOW:
                precipitation.is_a.append(l5_de.Light_Snow)
            elif cls.precipitation.type[scene_number] == omega_format.ReferenceTypes.Precipitation.MODERATE_SNOW:
                precipitation.is_a.append(l5_de.Moderate_Snow)
            elif cls.precipitation.type[scene_number] == omega_format.ReferenceTypes.Precipitation.HEAVY_SNOW:
                precipitation.is_a.append(l5_de.Heavy_Snow)
            # - amount_hourly
            if scene_number < len(cls.precipitation.amount_hourly):
                precipitation.has_precipitation_intensity_hourly = float(cls.precipitation.amount_hourly[scene_number])
            # - amount_minute
            if scene_number < len(cls.precipitation.amount_minute):
                precipitation.has_precipitation_intensity_minutely = float(cls.precipitation.amount_minute[
                                                                               scene_number])
    # - new_snow_depth, snow_depth
    if scene_number < len(cls.precipitation.snow_depth):
        if cls.precipitation.snow_depth[scene_number] > 0:
            snow_cover = l5_de.Snow_Cover()
            environment.consists_of.append(snow_cover)
            snow_cover.has_height = float(cls.precipitation.snow_depth[scene_number])
            if scene_number < len(cls.precipitation.new_snow_depth):
                snow_cover.has_new_snow_height = float(cls.precipitation.new_snow_depth[scene_number])
        else:
            environment.is_a.append(l5_de.No_Snow_Cover_Environment)

    # wind
    if scene_number < max(len(cls.wind.wind_speed), len(cls.wind.wind_direction),
               len(cls.gust_of_wind.wind_speed), len(cls.gust_of_wind.type)):
        wind = l5_core.Wind()
        environment.consists_of.append(wind)
        if scene_number < len(cls.wind.wind_speed):
            wind.has_wind_speed = [float(cls.wind.wind_speed[scene_number])]
        if scene_number < len(cls.wind.wind_direction):
            wind.has_wind_direction = float(cls.wind.wind_direction[scene_number])
        # gust_of_wind
        if scene_number < len(cls.gust_of_wind.type):
            if cls.gust_of_wind.type[scene_number] == omega_format.ReferenceTypes.GustOfWind.NO_GUSTS_OF_WIND:
                wind.is_a.append(l5_de.No_Gust_Wind)
            else:
                gust = l5_de.Gust()
                wind.has_environment_phenomenon(gust)
                environment.consists_of.append(gust)
                if cls.gust_of_wind.type[scene_number] == omega_format.ReferenceTypes.GustOfWind.GUST_OF_WIND:
                    gust.is_a.append(l5_de.Gust_Of_Wind)
                elif cls.gust_of_wind.type[scene_number] == omega_format.ReferenceTypes.GustOfWind.SQUALL:
                    gust.is_a.append(l5_de.Squall)
                elif cls.gust_of_wind.type[scene_number] == omega_format.ReferenceTypes.GustOfWind.HEAVY_SQUALL:
                    gust.is_a.append(l5_de.Heavy_Squall)
                elif cls.gust_of_wind.type[scene_number] == omega_format.ReferenceTypes.GustOfWind.GALE_FORCE_WINDS:
                    gust.is_a.append(l5_de.Gale_Force_Wind)
                elif cls.gust_of_wind.type[scene_number] == omega_format.ReferenceTypes.GustOfWind.VIOLENT_SQUALL:
                    gust.is_a.append(l5_de.Violent_Squall)
                elif (cls.gust_of_wind.type[scene_number] == omega_format.ReferenceTypes.GustOfWind.
                        SEVERE_GALE_FORCE_WINDS):
                    gust.is_a.append(l5_de.Severe_Gale_Force_Wind)
                if scene_number < len(cls.gust_of_wind.wind_speed):
                    wind.has_wind_speed.append(float(cls.gust_of_wind.wind_speed[scene_number]))

    # cloudiness
    if scene_number < len(cls.cloudiness.degree):
        sky = l5_core.Sky()
        environment.consists_of.append(sky)
        sky.has_cloudiness = float(cls.cloudiness.degree[scene_number])

    # temperature
    if scene_number < max(len(cls.temperature.air_temp), len(cls.temperature.air_temp_5cm),
                          len(cls.visibility.visibility), len(cls.air_pressure.air_pressure_nn),
                          len(cls.humidity.humidity)):
        air = l5_core.Air()
        environment.consists_of.append(air)
        if scene_number < len(cls.temperature.air_temp):
            air.has_temperature_2m_height = float(cls.temperature.air_temp[scene_number])
        if scene_number < len(cls.temperature.air_temp_5cm):
            air.has_temperature_5cm_height = float(cls.temperature.air_temp_5cm[scene_number])
        # humidity
        if scene_number < len(cls.humidity.humidity):
            air.has_relative_humidity = float(cls.humidity.humidity[scene_number])
        # air_pressure
        if scene_number < len(cls.air_pressure.air_pressure_nn):
            air.has_atmospheric_pressure = float(cls.air_pressure.air_pressure_nn[scene_number])
        # visibility
        if scene_number < len(cls.visibility.visibility):
            air = l5_core.Air()
            environment.consists_of.append(air)
            air.has_meteorological_visibility = float(cls.visibility.visibility[scene_number])

    # ground
    if scene_number < max(len(cls.temperature.ground_temp), len(cls.road_condition.spray)):
        ground = l5_core.Ground()
        environment.consists_of.append(ground)
        # ground temperature
        if scene_number < len(cls.temperature.ground_temp):
            ground.has_temperature = [float(cls.temperature.ground_temp[scene_number])]
        # spray
        if scene_number < len(cls.road_condition.spray):
            if cls.road_condition.spray[scene_number]:
                spray = l5_de.Spray()
                ground.has_environment_phenomenon.append(spray)
            else:
                ground.is_a.append(l5_de.No_Spray_Ground)

    # solar
    if scene_number < max(len(cls.solar.diff_solar_radiation), len(cls.solar.longwave_down_radiation),
                          len(cls.solar.solar_hours), len(cls.solar.solar_incoming_radiation)):
        sun = l5_core.Sun()
        environment.consists_of.append(sun)
        if scene_number < len(cls.solar.diff_solar_radiation):
            sun.has_diffuse_solar_radiation_10min = float(cls.solar.diff_solar_radiation[scene_number])
        if scene_number < len(cls.solar.solar_incoming_radiation):
            sun.has_solar_incoming_radiation_10min = float(cls.solar.solar_incoming_radiation[scene_number])
        if scene_number < len(cls.solar.solar_hours):
            sun.has_sunshine_duration_10min = float(cls.solar.solar_hours[scene_number])
        if scene_number < len(cls.solar.longwave_down_radiation):
            sun.has_longwave_downward_radiation_10min = float(cls.solar.longwave_down_radiation[scene_number])

    # road_condition
    # surface_condition
    if scene_number < len(cls.road_condition.surface_condition):
        # Wetness is on layer 1
        if (cls.road_condition.surface_condition[scene_number] == omega_format.ReferenceTypes.
                RoadConditionSurfaceCondition.MOIST):
            for r in scene.search(type=l1_core.Road):
                r.is_a.append(ph.Moist_Physical_Object)
        # Actual water bodies are on layer 5
        elif (cls.road_condition.surface_condition[scene_number] == omega_format.ReferenceTypes.
                RoadConditionSurfaceCondition.WET):
            water_layer = l5_de.Water_Layer()
            environment.consists_of.append(water_layer)
            if (cls.road_condition.surface_condition[scene_number] == omega_format.ReferenceTypes.
                    RoadConditionSurfaceCondition.WET_WITH_BODY_OF_WATER):
                water_layer.is_a.append(l5_de.Water_Layer_With_Body_Of_Water)
        elif (cls.road_condition.surface_condition[scene_number] == omega_format.ReferenceTypes.
                RoadConditionSurfaceCondition.SLIPPERINESS):
            ice = l5_de.Ice()
            environment.consists_of.append(ice)
        elif (cls.road_condition.surface_condition[scene_number] == omega_format.ReferenceTypes.
                RoadConditionSurfaceCondition.BLACK_ICE):
            black_ice = l5_de.Black_Ice()
            environment.consists_of.append(black_ice)
        elif (cls.road_condition.surface_condition[scene_number] == omega_format.ReferenceTypes.
                RoadConditionSurfaceCondition.PARTLY_SNOW):
            snow = l5_de.Partial_Snow_Cover()
            environment.consists_of.append(snow)
        elif (cls.road_condition.surface_condition[scene_number] == omega_format.ReferenceTypes.
                RoadConditionSurfaceCondition.SNOW_COVERED):
            snow = l5_de.Closed_Snow_Cover()
            environment.consists_of.append(snow)
        elif (cls.road_condition.surface_condition[scene_number] == omega_format.ReferenceTypes.
                RoadConditionSurfaceCondition.COMPACTED_SNOW):
            snow = l5_de.Compacted_Snow_Cover()
            environment.consists_of.append(snow)
        elif (cls.road_condition.surface_condition[scene_number] == omega_format.ReferenceTypes.
                RoadConditionSurfaceCondition.ICE_COVERED_SNOW):
            snow = l5_de.Snow_Cover()
            ice = l5_de.Ice()
            snow.sfIntersects.append(ice)
            ice.sfIntersects.append(snow)
            environment.consists_of.append(snow)
            environment.consists_of.append(ice)

    # maintenance_status is on layer 3
    for r in scene.search(type=l1_core.Road):
        if cls.road_condition.maintenance_status == omega_format.ReferenceTypes.RoadConditionMaintenanceStatus. \
                UNTREATED:
            r.is_a.append(l3_de.Road_Without_Contamination)
        if cls.road_condition.maintenance_status == omega_format.ReferenceTypes.RoadConditionMaintenanceStatus.DIRTY:
            r.is_a.append(l3_de.Road_With_Dirt)
        if cls.road_condition.maintenance_status == omega_format.ReferenceTypes.RoadConditionMaintenanceStatus.GRIT:
            r.is_a.append(l3_de.Road_With_Grit)
        if cls.road_condition.maintenance_status == omega_format.ReferenceTypes.RoadConditionMaintenanceStatus.SALTED:
            r.is_a.append(l3_de.Road_With_Salt)

    return [(cls, [environment])]
