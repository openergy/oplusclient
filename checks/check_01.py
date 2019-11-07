import functools
import sys
import time
import os

dir_path = os.path.realpath(os.path.dirname(__file__))
sys.path.append(os.path.realpath(os.path.join(dir_path, "..")))

from vbpclient import OSSClient, ResourceNotFound

auth_path = os.path.join(dir_path, "..", "rest_api_credentials.json")
url_path = os.path.join(dir_path, "..", "url_path.txt")
wprint = functools.partial(print, end="")

wprint("authenticating to client...")
client = OSSClient(auth_path=auth_path, url_path=url_path)
# client = OSSClient(auth_path=auth_path, url="http://localhost:8000")
print("done")

wprint("finding organization...")
organization = client.get_organization("Openergy")
print("done")

wprint("deleting project if it exists...")
try:
    project = organization.get_project("3zones_cta_project")
except ResourceNotFound:
    print("project does not exist")
else:
    project.destroy()
    print("done")

wprint("creating project...")
project = organization.create_project("3zones_cta_project")
print("done")

wprint("creating geometry...")
geometry = project.create_geometry("3zones_cta", "floorspace")
print("done")

wprint("uploading and importing floorspace...")
geometry.import_geometry("resources/test.flo")
print("done")

wprint("uploading and importing ogw...")
ogw_geom = project.create_geometry("ogw_test", "import")
ogw_geom.import_geometry("/home/zach/Downloads/8e88cf61-5be5-45fa-a948-4034c2a1b9d8.ogw", format="ogw")
print("done")

wprint("listing geometry...")
print(f"{len(project.list_geometry())} found, done.")

wprint("updating geometry site info...")
geometry.update(
    site_latitude=48,
    site_longitude=2,
    site_altitude=46,
    site_country_code="FR",
    site_postal_code="75004",
    site_time_zone_ref="Europe/Paris"
)
print("done")

wprint("creating obat...")
obat = project.create_obat("3zones_cta")
print("done")

wprint("uploading and importing obat excel...")
obat.import_excel("resources/test.xlsx")
print("done")

wprint("uploading and importing generic weather series...")
generic_weather_series = project.create_weather_series("test_weather")
print("done")

wprint("uploading and importing epw weather file...")
generic_weather_series.import_epw("resources/test.epw")
print("done")

wprint("creating mono simulation group...")
mono_simulation_group = project.create_mono_simulation_group("3zones_cta")
print("done")

wprint("updating mono simulation group config...")
mono_simulation_group.update(
    config_geometry=geometry,
    config_start="2012-01-01T00:00:00",
    config_end="2012-12-31T23:00:00",
    config_weather=generic_weather_series,
    config_obat=obat,
)
print("done")

wprint("starting simulation...")
simulation = mono_simulation_group.start_simulation()
print("done")

print("waiting for simulation...")
while True:
    simulation.reload()
    if simulation.status != "running":
        print("\n")
        print("SIMULATION FINISHED RUNNING")
        print(f"status: {simulation.status}")
        print(f"stdout: {simulation.logs}")
        break
    time.sleep(3)

print(simulation.get_out_hourly().shape)  # beware, can be quite big
print(simulation.get_out_zones().shape)
print(simulation.get_out_monthly_consumption().shape)
print(simulation.get_out_envelope().shape)
print(simulation.get_out_monthly_comfort().shape)
print(simulation.get_out_monthly_miscellaneous().shape)
print(simulation.get_out_monthly_thermal_balance().shape)
print(simulation.get_out_monthly_weather().shape)

# cleaning up
wprint("deleting project...")
project.destroy()
print("done")
