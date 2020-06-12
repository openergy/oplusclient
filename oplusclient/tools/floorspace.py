import os
import json
import uuid

resources_path = os.path.join(os.path.dirname(__file__), "resources")


def geo_data_frame_to_floorplan(geo_data_frame, buffer_or_path=None):
    """
    Parameters
    ----------
    geo_data_frame: geopandas.GeoDataFrame
        GeoDataFrame containing data to transform into a floorplan.
        A 'shading' column may be provided to specify if given a polygon is a shading. If not provided, no polygon
        will be considered as a shading.
    buffer_or_path: None, string or buffer
        if None, floorplan will be returned as text
        if string, floorplan will be written into file at given path
        if buffer, floorplan will be written into the buffer

    Returns
    -------
    None (if buffer_or_path is not None), else str containing the floorplan
    """
    # todo: explain the characteristics of geo_data_frame (shadings columns ? multiple zones ?)
    # import dependencies
    import numpy as np
    import shapely

    # projection
    # todo: manage multiple projections
    gdf = geo_data_frame.to_crs(epsg=2154)  # todo: what is epsg ?

    # find centroid and translate
    centroid = gdf.geometry[~gdf.shading].iloc[0].centroid
    gdf.geometry = gdf.geometry.translate(xoff=-centroid.x, yoff=-centroid.y)

    # transform to polygons
    polygons = list()
    for _, row in gdf.iterrows():
        if len(row.geometry) > 1:
            raise NotImplemented
        polygons.append(dict(
            polygon=shapely.affinity.rotate(
                shapely.geometry.Polygon(row.geometry[0].exterior),
                angle=-4,
                origin=[0, 0]),
            is_shading=row.shading,
            name=str(row.name)
        ))

    # set decimals
    decimals = 1  # todo: is this an option ?
    for p in polygons:
        p["polygon"] = shapely.wkt.loads(shapely.wkt.dumps(p["polygon"], rounding_precision=decimals))

    # prepare points
    points = np.array([])
    points.shape = (0, 2)
    for p in polygons:
        points = np.append(points, np.array(p["polygon"].exterior.coords[:-1]), axis=0)
    points = np.unique(points, axis=0)

    # prepare edges and faces
    edges = dict()
    faces = []
    for p in polygons:
        face = dict(edges=[], edges_order=[], is_shading=p["is_shading"], name=p["name"], id=str(uuid.uuid4()))
        for _a, _b in zip(p["polygon"].exterior.coords[:-1], p["polygon"].exterior.coords[1:]):
            a = np.where(np.all(points == np.array(_a), axis=1))[0][0]
            b = np.where(np.all(points == np.array(_b), axis=1))[0][0]
            if (a, b) in edges:
                edge_id = edges[(a, b)]
                order = 1
            elif (b, a) in edges:
                edge_id = edges[(b, a)]
                order = 0
            else:
                edge_id = str(uuid.uuid4())
                edges[(a, b)] = edge_id
                order = 1
            face["edges"].append(edge_id)
            face["edges_order"].append(order)
        faces.append(face)

    # load empty floorplan
    with open(os.path.join(resources_path, "empty_floorplan.flo")) as f:
        floorplan = json.load(f)

    # fill it with prepared data
    fs = floorplan["stories"][0]
    for i, p in enumerate(points):
        fs["geometry"]["vertices"].append(dict(
            x=p[0],
            y=p[1],
            id=str(uuid.UUID(int=i)),
            edge_ids=[]
        ))
    for vertices, e_id in edges.items():
        fs["geometry"]["edges"].append(dict(
            id=e_id,
            vertex_ids=[str(uuid.UUID(int=vertices[0])), str(uuid.UUID(int=vertices[1]))],
            face_ids=[]
        ))
        fs["geometry"]["vertices"][vertices[0]]["edge_ids"].append(e_id)
        fs["geometry"]["vertices"][vertices[1]]["edge_ids"].append(e_id)
    for face in faces:
        fs["geometry"]["faces"].append(dict(
            id=face["id"],
            edge_ids=face["edges"],
            edge_order=face["edges_order"]
        ))
        for edge in [e for e in fs["geometry"]["edges"] if e["id"] in face["edges"]]:
            edge["face_ids"].append(face["id"])
        if face["is_shading"]:
            fs["shading"].append(dict(
                id=str(uuid.uuid4()),
                handle=None,
                name=face["name"],
                face_id=face["id"],
                color="#E8E3E5",
                type="shading"
            ))
        else:
            fs["spaces"].append(dict(
                id=str(uuid.uuid4()),
                handle=None,
                name=face["name"],
                face_id=face["id"],
                zone_groups_tag_1_id=None,
                zone_groups_tag_2_id=None,
                pitched_roof_id=None,
                daylighting_controls=[],
                color="#E67E22",
                type="space"
            ))

    content = json.dumps(floorplan)

    if buffer_or_path is None:
        return content

    if isinstance(buffer_or_path, str):
        with open(buffer_or_path, "w") as f:
            f.write(content)
        return

    buffer_or_path.write(content)
