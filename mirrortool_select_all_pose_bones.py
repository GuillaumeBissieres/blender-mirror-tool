import bpy


class MIRRORTOOL_OT_Select_All_Pose_Bones(bpy.types.Operator):
    bl_idname = "mirrortool.select_all_pose_bones"
    bl_label = "Select All Pose Bones"
    bl_description = "Select all bones in Pose Mode"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (
            obj is not None
            and obj.type == 'ARMATURE'
            and context.mode == 'POSE'
        )

    def execute(self, context):
        bpy.ops.pose.select_all(action='SELECT')
        return {'FINISHED'}


def register():
    bpy.utils.register_class(MIRRORTOOL_OT_Select_All_Pose_Bones)


def unregister():
    bpy.utils.unregister_class(MIRRORTOOL_OT_Select_All_Pose_Bones)
