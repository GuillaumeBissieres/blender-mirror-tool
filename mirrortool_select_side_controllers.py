import bpy


class MIRRORTOOL_OT_Select_Side_Controllers(bpy.types.Operator):
    bl_idname = "mirrortool.select_side_controllers"
    bl_label = "Select Side Controllers"
    bl_description = "Select left or right side controllers"
    bl_options = {"REGISTER", "UNDO"}

    select_left: bpy.props.BoolProperty(
        name="Left",
        default=True
    )

    select_right: bpy.props.BoolProperty(
        name="Right",
        default=False
    )

    additive: bpy.props.BoolProperty(
        name="Add to Selection",
        default=False
    )

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (
            obj is not None
            and obj.type == 'ARMATURE'
            and context.mode == 'POSE'
        )

    def execute(self, context):
        obj = context.object

        if not self.additive:
            for pb in obj.pose.bones:
                pb.select = False

        for pb in obj.pose.bones:
            name = pb.name

            is_left = (
                name.endswith(".L")
                or name.endswith("_L")
                or name.endswith(".l")
                or name.startswith("L_")
            )

            is_right = (
                name.endswith(".R")
                or name.endswith("_R")
                or name.endswith(".r")
                or name.startswith("R_")
            )

            if (self.select_left and is_left) or (self.select_right and is_right):
                pb.select = True

        return {"FINISHED"}


def register():
    bpy.utils.register_class(MIRRORTOOL_OT_Select_Side_Controllers)


def unregister():
    bpy.utils.unregister_class(MIRRORTOOL_OT_Select_Side_Controllers)
