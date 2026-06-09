import bpy


class MIRRORTOOL_OT_Mirror_Pose_3977D(bpy.types.Operator):
    bl_idname = "mirrortool.mirror_pose_3977d"
    bl_label = "Mirror Pose"
    bl_description = (
        "Apply changes to matching bone on opposite side of X-axis "
        "(toggle Pose Options mirror settings)"
    )
    bl_options = {"REGISTER", "UNDO"}

    # Properties exposed to the Redo panel
    use_x_axis: bpy.props.BoolProperty(
        name="X-Axis Mirror",
        description="Mirror across X axis",
        default=True,
    )

    relative_mirror: bpy.props.BoolProperty(
        name="Relative Mirror",
        description="Use relative mirroring (if available)",
        default=True,
    )

    affect_only_locations: bpy.props.BoolProperty(
        name="Affect Only: Locations",
        description="Only affect locations when mirroring (if available)",
        default=False,
    )

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (
            obj is not None
            and obj.type == "ARMATURE"
        )

    def execute(self, context):
        obj = context.object
        scene = context.scene

        if not obj or obj.type != "ARMATURE":
            return {"CANCELLED"}

        # Helper: try to set an RNA property by keyword matching
        def try_set_rna_by_keywords(targets, keywords, value):
            for target in targets:
                if target is None or not hasattr(target, "bl_rna"):
                    continue
                for prop in target.bl_rna.properties:
                    if prop.identifier == "rna_type":
                        continue
                    name = (prop.name or "").lower()
                    ident = (prop.identifier or "").lower()
                    desc = (prop.description or "").lower()
                    for kw in keywords:
                        if kw in name or kw in ident or kw in desc:
                            try:
                                setattr(target, prop.identifier, value)
                                return True
                            except Exception:
                                pass
            return False

        targets = [
            getattr(obj, "pose", None),
            getattr(obj, "data", None),
            getattr(scene, "tool_settings", None),
            getattr(context, "tool_settings", None),
            getattr(context, "space_data", None),
            getattr(context.window_manager, "tool_settings", None),
            scene,
            obj,
        ]

        rel_keywords = ["relative", "relative mirror", "use_relative"]
        loc_keywords = ["location", "locations", "affect only", "affect_only"]

        current = getattr(obj.pose, "use_mirror_x", False)

        if not current:
            # Activate mirror
            try:
                obj.pose.use_mirror_x = True
            except Exception:
                pass

            try_set_rna_by_keywords(targets, rel_keywords, bool(self.relative_mirror))
            try_set_rna_by_keywords(targets, loc_keywords, bool(self.affect_only_locations))

            try:
                scene.sna_boolean = True
            except Exception:
                pass
        else:
            # Deactivate mirror
            try:
                obj.pose.use_mirror_x = False
            except Exception:
                pass

            try_set_rna_by_keywords(targets, rel_keywords, False)
            try_set_rna_by_keywords(targets, loc_keywords, False)

            try:
                scene.sna_boolean = False
            except Exception:
                pass

        return {"FINISHED"}


def register():
    bpy.utils.register_class(MIRRORTOOL_OT_Mirror_Pose_3977D)


def unregister():
    bpy.utils.unregister_class(MIRRORTOOL_OT_Mirror_Pose_3977D)
