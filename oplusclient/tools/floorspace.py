import os
import json
import uuid

resources_path = os.path.join(os.path.dirname(__file__), "resources")


class Floorplan:
    """
    Basic Floorplan class.

    For now, just stores the json representation of the floorplan as its json_data attribute.
    """
    def __init__(self, json_data):
        self.json_data = json_data

    def add_window_definition(
            self,
            name,
            window_definition_mode,
            wwr=None,
            window_spacing=None,
            height=None,
            width=None,
            sill_height=None,
            texture="circles-5",
    ):
        """
        Parameters
        ----------
        name: str
        window_definition_mode: str
            windowToWallRatio, or ...
        wwr: float or None
            NOne if window_definition_mode not windowToWallRatio
        window_spacing: float or None
        height: float or None
        width: float or None
        sill_height: float or None
        texture: string
        """
        wd_id = str(uuid.uuid4())
        self.json_data["window_definitions"].append(dict(
            id=wd_id,
            name=name,
            window_definition_mode=window_definition_mode,
            wwr=wwr,
            window_spacing=window_spacing,
            height=height,
            width=width,
            sill_height=sill_height,
            texture=texture
        ))

    def add_window_to_all_exterior_edges(self, window_definition_name, alpha=0.5):
        window_i = 0
        window_definition_id = [w["id"] for w in self.json_data["window_definitions"]
                                if w["name"] == window_definition_name][0]
        for story in self.json_data["stories"]:
            space_faces_ids = set([space["face_id"] for space in story["spaces"]])
            for edge in story["geometry"]["edges"]:
                if (len(edge["face_ids"]) != 1) or (edge["face_ids"][0] not in space_faces_ids):
                    continue
                # TODO: add window to this edge
                story["windows"].append(dict(
                    window_definition_id=window_definition_id,
                    edge_id=edge["id"],
                    alpha=alpha,
                    id=str(uuid.uuid4()),
                    name=f"auto_window_{window_i}"
                ))
                window_i += 1

    def add_story(self, name, height, color="#999933"):
        """
        Create an empty story.

        Parameters
        ----------
        name: str
            story name
        height: str
            story height
        color: str
            color (hexadecimal string)
        """
        self.json_data["stories"].append(dict(
            id=str(uuid.uuid4()),
            handle=None,
            name=name,
            image_visible=True,
            height=height,
            color=color,
            geometry=dict(
                id=str(uuid.uuid4()),
                vertices=[],
                edges=[],
                faces=[]
            ),
            images=[],
            spaces=[],
            shading=[],
            windows=[],
            doors=[]
        ))

    def add_space_to_story(
            self,
            story_name,
            vertices,
            name,
            zone_groups_tag_1_id=None,
            zone_groups_tag_2_id=None,
            pitched_roof_id=None,
            daylighting_controls=None,
            color="#E67E22"
    ):
        """
        Add a space to a story.

        Parameters
        ----------
        story_name: str
            name of the story on which the space should be added
        vertices: list
            ordered list of (x, y) coordinates of the polygon to add
        name: str
        zone_groups_tag_1_id: str or None
        zone_groups_tag_2_id: str or None
        pitched_roof_id: str or None
        daylighting_controls: list or None
        color: str or None
        """
        try:
            story = [s for s in self.json_data["stories"] if s["name"] == story_name][0]
        except IndexError:
            raise ValueError(f"No story with name {story_name} found")

        face_id = str(uuid.uuid4())
        space_id = str(uuid.uuid4())

        story["spaces"].append(dict(
            id=space_id,
            handle=None,
            name=name,
            face_id=face_id,
            zone_groups_tag_1_id=zone_groups_tag_1_id,
            zone_groups_tag_2_id=zone_groups_tag_2_id,
            pitched_roof_id=pitched_roof_id,
            daylighting_controls=daylighting_controls if daylighting_controls is not None else [],
            color=color,
            type="space"
        ))

        # get the dest vertices and add the source ones
        self._add_face_to_story(face_id, vertices, story)

    def add_shading_to_story(
        self,
        story_name,
        vertices,
        name,
        color="#E8E3E5"
    ):
        """
        Add a shading to a story.

        Parameters
        ----------
        story_name: str
            name of the story on which the space should be added
        vertices: list
            ordered list of (x, y) coordinates of the polygon to add
        name: str
            name of the shading
        color: str
        """
        try:
            story = [s for s in self.json_data["stories"] if s["name"] == story_name][0]
        except IndexError:
            raise ValueError(f"No story with name {story_name} found")

        face_id = str(uuid.uuid4())
        shading_id = str(uuid.uuid4())

        story["shading"].append(dict(
            id=shading_id,
            handle=None,
            name=name,
            face_id=face_id,
            color=color,
            type="shading"
        ))

        # get the dest vertices and add the source ones
        self._add_face_to_story(face_id, vertices, story)

    @staticmethod
    def _add_face_to_story(face_id, face_vertices, story):
        face = dict(
            id=face_id,
            edge_ids=[],
            edge_order=[]
        )

        vertices = dict()
        for v in story["geometry"]["vertices"]:
            vertices[(v["x"], v["y"])] = v

        story["geometry"]["faces"].append(face)

        # get the dest edges
        edges = dict()
        for edge in story["geometry"]["edges"]:
            edges[(edge["vertex_ids"][0], edge["vertex_ids"][1])] = edge
        for v0, v1 in zip(face_vertices, face_vertices[1:] + face_vertices[0:1]):
            for v in (v0, v1):
                if v not in vertices:
                    v_id = str(uuid.uuid4())
                    v_d = dict(
                        x=v[0],
                        y=v[1],
                        id=v_id,
                        edge_ids=[]
                    )
                    story["geometry"]["vertices"].append(v_d)
                    vertices[v] = v_d
            tup = (vertices[v0]["id"], vertices[v1]["id"])
            inv = (vertices[v1]["id"], vertices[v0]["id"])
            if tup in edges:
                edge_d = edges[tup]
                face["edge_order"].append(1)
            elif inv in edges:
                edge_d = edges[inv]
                face["edge_order"].append(0)
            else:
                edge_d = dict(
                    id=str(uuid.uuid4()),
                    vertex_ids=list(tup),
                    face_ids=[]
                )
                story["geometry"]["edges"].append(edge_d)
                edges[tup] = edge_d
                face["edge_order"].append(1)
            face["edge_ids"].append(edge_d["id"])
            edge_d["face_ids"].append(face_id)
            vertices[v0]["edge_ids"].append(edge_d["id"])
            vertices[v1]["edge_ids"].append(edge_d["id"])

    def copy_space_to_story(self, space_name, source_story_name, dest_story_name):
        """
        Copy a space to another stories

        Only clones the geometry, windows, etc. are not copied.

        Parameters
        ----------
        space_name: str
            Name of the space to copy
        source_story_name: str
            Story where the space is located
        dest_story_name: str
            Story where the space should be copied
        """
        if source_story_name == dest_story_name:
            raise ValueError("source and destination stories must be different.")
        try:
            src_story = [s for s in self.json_data["stories"] if s["name"] == source_story_name][0]
        except IndexError:
            raise ValueError(f"No story with name {source_story_name} found")
        try:
            src_space = [s for s in src_story["spaces"] if s["name"] == space_name][0]
        except IndexError:
            raise ValueError(f"No space with name {space_name} found")

        src_face = [s for s in src_story["geometry"]["faces"] if s["id"] == src_space["face_id"]][0]

        # get the vertices
        vertices = []
        for e_id, order in zip(src_face["edge_ids"], src_face["edge_order"]):
            edge = [e for e in src_story["geometry"]["edges"] if e["id"] == e_id][0]
            v0 = [v for v in src_story["geometry"]["vertices"] if v["id"] == edge["vertex_ids"][0 if order else 1]][0]
            vertices.append((v0["x"], v0["y"]))

        self.add_space_to_story(
            dest_story_name,
            vertices,
            src_space["name"],
            src_space["zone_groups_tag_1_id"],
            src_space["zone_groups_tag_2_id"],
            src_space["pitched_roof_id"],
            src_space["daylighting_controls"],
            src_space["color"]
        )

    def copy_shading_to_story(self, shading_name, source_story_name, dest_story_name):
        """
        Copy a shading to another stories

        Only clones the geometry, windows, etc. are not copied.

        Parameters
        ----------
        shading_name: str
            Name of the shading to copy
        source_story_name: str
            Story where the shading is located
        dest_story_name: str
            Story where the shading should be copied
        """
        if source_story_name == dest_story_name:
            raise ValueError("source and destination stories must be different.")
        try:
            src_story = [s for s in self.json_data["stories"] if s["name"] == source_story_name][0]
        except IndexError:
            raise ValueError(f"No story with name {source_story_name} found")
        try:
            src_shading = [s for s in src_story["shading"] if s["name"] == shading_name][0]
        except IndexError:
            raise ValueError(f"No shading with name {shading_name} found")

        src_face = [s for s in src_story["geometry"]["faces"] if s["id"] == src_shading["face_id"]][0]

        # get the vertices
        vertices = []
        for e_id, order in zip(src_face["edge_ids"], src_face["edge_order"]):
            edge = [e for e in src_story["geometry"]["edges"] if e["id"] == e_id][0]
            v0 = [v for v in src_story["geometry"]["vertices"] if v["id"] == edge["vertex_ids"][0 if order else 1]][0]
            vertices.append((v0["x"], v0["y"]))

        self.add_shading_to_story(
            dest_story_name,
            vertices,
            src_shading["name"],
            src_shading["color"]
        )

    def save(self, buffer_or_path=None):
        """
        Parameters
        ----------
        buffer_or_path: None, string or buffer
            if None, floorplan will be returned as text
            if string, floorplan will be written into file at given path
            if buffer, floorplan will be written into the buffer


        Returns
        -------
        str or None
        """
        content = json.dumps(self.json_data)

        if buffer_or_path is None:
            return content

        if isinstance(buffer_or_path, str):
            with open(buffer_or_path, "w") as f:
                f.write(content)
            return

        buffer_or_path.write(content)

    @classmethod
    def load(cls, buffer_or_path):
        if isinstance(buffer_or_path, str):
            with open(buffer_or_path, "r") as f:
                json_data = json.load(f)

        else:
            json_data = json.load(buffer_or_path)

        return cls(json_data)

    @classmethod
    def geo_data_frame_to_floorplan(cls, geo_data_frame):
        """
        Parameters
        ----------
        geo_data_frame: geopandas.GeoDataFrame
            GeoDataFrame containing data to transform into a floorplan.
            A 'shading' column may be provided to specify if given a polygon is a shading. If not provided, no polygon
            will be considered as a shading.

        Returns
        -------
        None (if buffer_or_path is not None), else str containing the floorplan
        """
        # todo: recode with the add_zone / add_shading functions coded above
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

        return cls(floorplan)
