Quickstart
==========


Installation
^^^^^^^^^^^^

oplusclient is easily installed via pip:

.. code-block:: bash

    pip install oplusclient


Client
^^^^^^

Create the client

.. testcode::

    import oplusclient
    import datetime as dt
    client = Client()

Take a seat in an organization so we can make modifications, select an existing project

.. testcode::

    orga = client.get_organization("Test Organization")
    orga.take_seat()
    project = client.get_project("Test Project")

Geometry
^^^^^^^^

Create a new geometry from an idf file (geometries can have "import" or "floorspace" as format, here we should import
because we want to import an idf file), and download it in Openergy's ogw format

.. testcode::

    geom = project.create_geometry("Test Geometry", "import")
    geom.import_file("/path/to/file.idf", import_format="idf")
    geom.download_ogw("/path/to/file.ogw")


Weather
^^^^^^^

Create a new generic weather series from an epw, download it as a csv

.. testcode::

    weather = project.create_weather("Test Weather", "generic")
    weather.import_file("/path/to/file.epw", import_format="epw")
    weather.export("csv", buffer_or_path="/path/to/file.csv")


Thermal Model
^^^^^^^^^^^^^

Thermal Models are referred to as "Obats" in the Client and API.
Here we create an obat using an excel file, and download it in Openergy's obat format

.. testcode::

    obat = project.create_obat("Test Obat")
    obat.import_file("/path/to/file.xlsx", import_format="xlsx")
    obat.export("xlsx", buffer_or_path="/path/to/file.xlsx")


Simulations
^^^^^^^^^^^

Simulations are organized in simulation groups. There are two types of simulation groups: the multi simulation groups
containing several simulations with aggregated results, and the simple mono simulation groups having a single
simulation.
Here, we create a multi simulation group with two simulations and run it

.. testcode::

    simu_group = project.create_multi_simulation_group("My Simulation Group")
    simu_group.add_simulation(
        "first_simu",
        weather,
        geometry,
        obat,
        dt.datetime(2019, 1, 1),
        dt.datetime(2019, 1, 2)
    )
    simu_group.add_simulation(
        "first_simu",
        weather,
        geometry,
        obat,
        dt.datetime(2019, 1, 1),
        dt.datetime(2019, 1, 2),
        variant="some_variant"
    )
    simu_group.run()
    # the next line is optional and waits until the simulation group has finished running, printing the logs received
    #  from the simulator in real time.
    simu_group.wait_for_completion(print_logs=True)

We can then fetch the aggregated results from the simulation group as pandas DataFrames:

.. testcode::

    consumption_ef = simu_group.get_out_monthly_consumption_ep()

Fetch result from a single simulation as pandas DataFrame:

.. testcode::

    first_simu = simu_group.get_simulation_by_name("first_simu")
    thermal_balance = first_simu.get_out_monthly_thermal_balance()
    hourly_outputs = first_simu.get_out_hourly()
