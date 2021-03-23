import os
import random
import json
import uuid
import warnings


FLOORSPACE_COLORS = [
    "#aa4499",
    "#88ccee",
    "#332288",
    "#117733",
    "#999933",
    "#ddcc77",
    "#cc6677",
    "#882255",
    "#44aa99",
    "#6699cc",
    "#661100",
    "#aa4466",
]

resources_path = os.path.join(os.path.dirname(__file__), "resources")


def geo_data_frame_to_floorplan(geo_data_frame, buffer_or_path=None):
    warnings.warn(DeprecationWarning, "this function is deprecated, use Floorplan.geo_data_frame_to_floorplan")
    plan = Floorplan.geo_data_frame_to_floorplan(geo_data_frame)
    return plan.save(buffer_or_path)


class ObjectNotFoundError(Exception):
    pass


class Floorplan:
    """
    Basic Floorplan class.

    For now, just stores the json representation of the floorplan as its json_data attribute.
    """
    def __init__(self, json_data):
        self.json_data = json_data
        self._color_index = random.randint(0, len(FLOORSPACE_COLORS) - 1)

    def get_next_color(self):
        color = FLOORSPACE_COLORS[self._color_index]
        self._color_index = (self._color_index + 1) % len(FLOORSPACE_COLORS)
        return color

    def add_zone_group_tag_1(self, name, color=None):
        """
        Create a empty zone_group_tag_1.

        Parameters
        ----------
        name: str
            story name
        color: str
            color (hexadecimal string)
        """
        self.json_data["zone_groups_tags_1"].append(dict(
            id=str(uuid.uuid4()),
            handle=None,
            name=name,
            color=color or self.get_next_color(),
            type="zone_groups_tags_1"
        ))
    
    def add_zone_group_tag_2(self, name, color=None):
        """
        Create a empty zone_group_tag_2.

        Parameters
        ----------
        name: str
            story name
        color: str
            color (hexadecimal string)
        """
        self.json_data["zone_groups_tags_2"].append(dict(
            id=str(uuid.uuid4()),
            handle=None,
            name=name,
            color=color or self.get_next_color(),
            type="zone_groups_tags_2"
        ))

    def add_zone_group_tag_3(self, name, color=None):
        """
        Create a empty zone_group_tag_3.

        Parameters
        ----------
        name: str
            story name
        color: str
            color (hexadecimal string)
        """
        self.json_data["zone_groups_tags_3"].append(dict(
            id=str(uuid.uuid4()),
            handle=None,
            name=name,
            color=color or self.get_next_color(),
            type="zone_groups_tags_3"
        ))
    
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
                story["windows"].append(dict(
                    window_definition_id=window_definition_id,
                    edge_id=edge["id"],
                    alpha=alpha,
                    id=str(uuid.uuid4()),
                    name=f"auto_window_{window_i}"
                ))
                window_i += 1

    def add_story(self, name, height, color=None):
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
            color=color or self.get_next_color(),
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
            zone_groups_tag_3_id=None,
            pitched_roof_id=None,
            daylighting_controls=None,
            color=None
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
        zone_groups_tag_3_id: str or None
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
            zone_groups_tag_3_id=zone_groups_tag_3_id,
            pitched_roof_id=pitched_roof_id,
            daylighting_controls=daylighting_controls if daylighting_controls is not None else [],
            color=color or self.get_next_color(),
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
        color: str or None
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
            color=color or self.get_next_color(),
            type="shading"
        ))

        # get the dest vertices and add the source ones
        self._add_face_to_story(face_id, vertices, story)

    def remove_space_from_story(
            self,
            story_name,
            name
    ):
        """
        Remove a space from a story.

        Parameters
        ----------
        story_name: str
            name of the story on which the space should be added
        name: str
        """
        try:
            story = [s for s in self.json_data["stories"] if s["name"] == story_name][0]
        except IndexError:
            raise ValueError(f"No story with name {story_name} found")

        space_ix, space = [(i, s) for i, s in enumerate(story["spaces"]) if s["name"] == name][0]
        del story["spaces"][space_ix]

        self._remove_face_from_story(space["face_id"], story)

    def remove_shading_from_story(
            self,
            story_name,
            name
    ):
        """
        Remove a shading from a story.

        Parameters
        ----------
        story_name: str
            name of the story on which the space should be added
        name: str
        """
        try:
            story = [s for s in self.json_data["stories"] if s["name"] == story_name][0]
        except IndexError:
            raise ValueError(f"No story with name {story_name} found")

        shading_ix, shading = [(i, s) for i, s in enumerate(story["shadings"]) if s["name"] == name][0]
        del story["shadings"][shading_ix]

        self._remove_face_from_story(shading["face_id"], story)

    def _remove_face_from_story(self, face_id, story):
        face_ix, face = [(i, f) for i, f in enumerate(story["geometry"]["faces"]) if f["id"] == face_id][0]
        del story["geometry"]["faces"][face_ix]
        deleted_edges = set()
        for edge in story["geometry"]["edges"]:
            edge["face_ids"] = [fid for fid in edge["face_ids"] if fid != face_id]
            if len(edge["face_ids"]) == 0:
                deleted_edges.add(edge["id"])
        # remove edges with no face
        story["geometry"]["edges"] = [e for e in story["geometry"]["edges"] if len(e["face_ids"]) != 0]

        for vertex in story["geometry"]["vertices"]:
            vertex["edge_ids"] = [eid for eid in vertex["edge_ids"] if eid not in deleted_edges]
        # remove vertices with no edge
        story["geometry"]["vertices"] = [v for v in story["geometry"]["vertices"] if len(v["edge_ids"]) != 0]

    def _add_face_to_story(self, face_id, face_vertices, story):
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

    def display_faces(self, face_ids):
        # debug function used to display faces
        import numpy as np
        from matplotlib.patches import Polygon
        from matplotlib.collections import PatchCollection
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        if isinstance(face_ids, str):
            face_ids = [face_ids]
        vertices = [np.array(self.get_face_vertices(f)) for f in face_ids]
        patches = [Polygon(v) for v in vertices]
        colors = np.arange(len(face_ids))
        p = PatchCollection(patches)
        p.set_array(np.array(colors))
        ax.set_xlim(xmin=min([np.min(v[:, 0]) for v in vertices]), xmax=max([np.max(v[:, 0]) for v in vertices]))
        ax.set_ylim(ymin=min([np.min(v[:, 1]) for v in vertices]), ymax=max([np.max(v[:, 1]) for v in vertices]))
        ax.add_collection(p)
        fig.colorbar(p, ax=ax)
        plt.show()

    @staticmethod
    def _get_by_id(l, id):
        try:
            return [o for o in l if o["id"] == id][0]
        except IndexError:
            raise ObjectNotFoundError(f"Could not find an object with id {id}.")

    def get_face_vertices(self, face_id):
        vertices = []
        for s in self.json_data["stories"]:
            try:
                face = self._get_by_id(s["geometry"]["faces"], face_id)
            except ObjectNotFoundError:
                continue
            else:
                geometry = s["geometry"]
                break
        else:
            raise ValueError(f"Could not find a face with id {face_id}.")
        for e_id, e_order in zip(face["edge_ids"], face["edge_order"]):
            edge = self._get_by_id(geometry["edges"], e_id)
            if e_order:
                v = self._get_by_id(geometry["vertices"], edge["vertex_ids"][0])
            else:
                v = self._get_by_id(geometry["vertices"], edge["vertex_ids"][1])
            vertices.append((v["x"], v["y"]))
        return vertices

    def copy_space_to_story(self, space_name, source_story_name, dest_story_name):
        """
        Copy a space to another story

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

        src_face = self._get_by_id(src_story["geometry"]["faces"], src_space["face_id"])

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
            src_space["zone_groups_tag_3_id"],
            src_space["pitched_roof_id"],
            src_space["daylighting_controls"],
            src_space["color"]
        )

    def copy_shading_to_story(self, shading_name, source_story_name, dest_story_name):
        """
        Copy a shading to another story

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

        src_face = self._get_by_id(src_story["geometry"]["faces"], src_shading["face_id"])

        # get the vertices
        vertices = []
        for e_id, order in zip(src_face["edge_ids"], src_face["edge_order"]):
            edge = self._get_by_id(src_story["geometry"]["edges"], e_id)
            v0 = self._get_by_id(src_story["geometry"]["vertices"], edge["vertex_ids"][0 if order else 1])
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
    def geo_data_frame_to_floorplan(
        cls,
        geo_data_frame,
        story_name="story_0",
        story_height=3,
        centroid=None,
        rotation_angle=0,
        snap_to_grid=False,
        decimal_precision=1
    ):
        """
        Parameters
        ----------
        geo_data_frame: geopandas.GeoDataFrame
            GeoDataFrame containing data to transform into a floorplan.
            A 'shading' column may be provided to specify if given a polygon is a shading. If not provided, no polygon
            will be considered as a shading.
        story_name: str, default story_0
            name that will be given to the unique story
        story_height: float, default 3
            height of the unique story
        rotation_angle: float, default 0
            rotation angle of polygons
        snap_to_grid: boolean, default False
            indicates if polygons should be snapped to grid in order to facilitate further edition
        decimal_precision: int, default 1
            decimal precision of the grid

        Returns
        -------
        None (if buffer_or_path is not None), else floorplan

        Notes
        -----
        The created floorplan will contain one story. This story will contain one space per non shading polygon. The
        name of the spaces corresponds to the index of the geo_data_frame.
        """
        # todo: explain the characteristics of geo_data_frame (shadings columns ? multiple zones ?)
        # import dependencies
        import shapely

        # projection
        # todo: manage multiple projections
        gdf = geo_data_frame.to_crs(epsg=2154)
        # remove empty and duplicate geometries
        gdf = gdf[~gdf.is_empty]
        gdf = gdf.sort_values(["shading"])
        if len(gdf) > 1:
            gdf = gdf[~gdf.geometry.duplicated(keep="first")]

        # find centroid and translate
        if centroid is None:
            centroid = gdf.geometry.iloc[0].centroid
        gdf.geometry = gdf.geometry.translate(xoff=-centroid.x, yoff=-centroid.y)

        # transform to polygons
        polygons = list()
        for _, row in gdf.iterrows():
            if isinstance(row.geometry, shapely.geometry.MultiPolygon):
                if len(row.geometry) > 1:
                    raise NotImplemented
                polygon = shapely.geometry.Polygon(row.geometry[0].exterior).simplify(0, preserve_topology=False)
            elif isinstance(row.geometry, shapely.geometry.Polygon):
                polygon = shapely.geometry.Polygon(row.geometry.exterior).simplify(0, preserve_topology=False)
            else:
                raise NotImplemented
            if rotation_angle:
                polygon = shapely.affinity.rotate(polygon, angle=rotation_angle, origin=[0, 0])
            if snap_to_grid:
                polygon = shapely.wkt.loads(shapely.wkt.dumps(polygon, rounding_precision=decimal_precision))
            polygons.append(dict(
                polygon=polygon,
                is_shading=row.shading,
                name=str(row.name)
            ))

        # load empty floorplan
        with open(os.path.join(resources_path, "empty_floorplan.flo")) as f:
            floorplan = cls(json.load(f))
        
        # Set floorplan project parameters
        fp = floorplan.json_data["project"]
        fp["north_axis"] = rotation_angle
        fp["grid"]["spacing"] = 10 ** (- decimal_precision)
        
        # fill it with prepared data
        fs = floorplan.json_data["stories"][0]
        fs["name"] = story_name
        fs["height"] = story_height

        for p in polygons:
            if p["is_shading"]:
                floorplan.add_shading_to_story(
                    story_name,
                    list(p["polygon"].exterior.coords[:-1]),
                    p["name"]
                )
            else:
                floorplan.add_space_to_story(
                    story_name,
                    list(p["polygon"].exterior.coords[:-1]),
                    p["name"]
                )

        return floorplan
