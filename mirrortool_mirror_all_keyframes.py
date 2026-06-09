import bpy


class MIRRORTOOL_OT_Mirror_All_Keyframes_6C1Cb(bpy.types.Operator):
    bl_idname = "mirrortool.mirror_all_keyframes_6c1cb"
    bl_label = "Mirror All KeyFrames"
    bl_description = (
        "Mirror active controllers on all keyframes on opposite side "
        "of 3D cursor axis"
    )
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (
            obj is not None
            and obj.type == "ARMATURE"
        )

    def execute(self, context):

        def mirror_animation():
            # Save current area type
            prev_area = bpy.context.area.type

            # Switch to Dope Sheet editor to ensure actions can be modified
            for area in bpy.context.screen.areas:
                if area.type == 'DOPESHEET_EDITOR':
                    bpy.context.area.type = 'DOPESHEET_EDITOR'
                    break

            # Select all controllers in Pose Mode
            bpy.ops.pose.select_all(action='SELECT')

            # Optional: set interpolation to constant to avoid curve issues
            bpy.ops.action.interpolation_type(type='CONSTANT')

            # Copy / paste animation with mirror enabled
            bpy.ops.action.select_all(action='SELECT')
            bpy.ops.action.copy()
            bpy.ops.action.paste(flipped=True)

            # Restore previous editor
            bpy.context.area.type = prev_area

        mirror_animation()
        return {"FINISHED"}


def register():
    bpy.utils.register_class(MIRRORTOOL_OT_Mirror_All_Keyframes_6C1Cb)


def unregister():
    bpy.utils.unregister_class(MIRRORTOOL_OT_Mirror_All_Keyframes_6C1Cb)
