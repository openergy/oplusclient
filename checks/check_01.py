import functools
import sys
import os

dir_path = os.path.realpath(os.path.dirname(__file__))
sys.path.append(os.path.realpath(os.path.join(dir_path, "..")))

from vbpclient import OSSClient, ResourceNotFound

auth_path = os.path.join(dir_path, "..", "rest_api_credentials.json")
url_path = os.path.join(dir_path, "..", "url_path.txt")
wprint = functools.partial(print, end="")

wprint("authenticating to client...")
client = OSSClient(auth_path=auth_path, url="https://test-ossplatform.openergy.fr")
# client = OSSClient(auth_path=auth_path, url="http://localhost:8000")
print("done")

wprint("finding organization...")
organization = client.get_organization("Template Organization")
print("done")

project = organization.get_project("openergy_historical_weather_series")
weather = project.create_weather("Niort", format="historical")
weather.update(
    location_latitude=46.3273551,
    location_longitude=-0.5313457,
    location_altitude=12,
    location_time_zone_ref="Europe/Paris",
    sizing=dict(method="rt2012", data=dict(department="79", is_coast=False)),
    site_conditions=dict(method="monthly_triplets", data={
        "heated_ground_temperatures": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        "undisturbed_ground_temperatures": [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        "water_temperatures": [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
    })
)

weather.import_file("resources/test.epw", import_format="epw")

# wprint("deleting project if it exists...")
# try:
#     project = organization.get_project("3zones_cta_project")
# except ResourceNotFound:
#     print("project does not exist")
# else:
#     project.destroy()
#     print("done")
#
# wprint("creating project...")
# project = organization.create_project("3zones_cta_project")
# print("done")
#
# wprint("creating geometry...")
# geometry = project.create_geometry("3zones_cta", "floorspace")
# print("done")
#
# wprint("uploading and importing floorspace...")
# geometry.import_file("resources/test.flo")
# print("done")
#
# wprint("uploading and importing ogw...")
# ogw_geom = project.create_geometry("ogw_test", "import")
# ogw_geom.import_file("/home/zach/Downloads/8e88cf61-5be5-45fa-a948-4034c2a1b9d8.ogw")
# print("done")
#
# wprint("listing geometry...")
# print(f"{len(project.list_geometry())} found, done.")
#
# wprint("creating obat...")
# obat = project.create_obat("3zones_cta")
# print("done")
#
# wprint("uploading and importing obat excel...")
# obat.import_file("resources/test.xlsx", import_format="xlsx")
# print("done")
#
# wprint("uploading and importing generic weather series...")
# weather = project.create_weather("test_weather", format="generic")
# print("done")
#
# wprint("updating site information...")
# weather.update(
#     location_latitude=0,
#     location_longitude=0,
#     location_altitude=0,
#     location_time_zone_ref="Europe/Paris",
#     sizing=dict(method="rt2012", data=dict(department="75", is_coast=False)),
#     site_conditions=dict(method="monthly_triplets", data={
#         "heated_ground_temperatures": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#         "undisturbed_ground_temperatures": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#         "water_temperatures": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
#     })
# )
# print("done")
#
# wprint("uploading and importing epw weather file...")
# weather.import_file("resources/test.epw", import_format="epw")
# print("done")
#
# wprint("creating mono simulation group...")
# mono_simulation_group = project.create_mono_simulation_group("3zones_cta")
# print("done")
#
# wprint("updating mono simulation group config...")
# mono_simulation_group.update(
#     config_geometry=geometry,
#     config_start="2012-01-01T00:00:00",
#     config_end="2012-12-31T23:00:00",
#     config_weather=weather,
#     config_obat=obat,
# )
# print("done")
#
# wprint("starting simulation...")
# simulation = mono_simulation_group.run_simulation()
# print("done")
#
# print("waiting for simulation...")
# simulation.wait_for_completion(print_logs=True)
#
# print(simulation.get_out_hourly().shape)  # beware, can be quite big
# print(simulation.get_out_zones().shape)
# print(simulation.get_out_monthly_consumption().shape)
# print(simulation.get_out_envelope().shape)
# print(simulation.get_out_monthly_comfort().shape)
# print(simulation.get_out_monthly_miscellaneous().shape)
# print(simulation.get_out_monthly_thermal_balance().shape)
# print(simulation.get_out_monthly_weather().shape)
#
# # cleaning up
# wprint("deleting project...")
# project.destroy()
# print("done")
