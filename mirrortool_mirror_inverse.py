import bpy
import mathutils


class MIRRORTOOL_OT_Mirror_Inverse_A1B7D(bpy.types.Operator):
    bl_idname = "mirrortool.mirror_inverse_a1b7d"
    bl_label = "Mirror Inverse"
    bl_description = "Mirror and inverse selected controller(s) with adjustable strength"
    bl_options = {"REGISTER", "UNDO"}

    mirror_strength: bpy.props.FloatProperty(
        name="Mirror Strength",
        description="Blend between original pose and inverse mirrored pose",
        subtype='PERCENTAGE',
        default=100.0,
        min=0.0,
        max=100.0
    )

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (
            obj is not None and
            obj.type == 'ARMATURE' and
            context.mode == 'POSE'
        )

    # internal storage
    _original = None
    _mirrored = None

    def invoke(self, context, event):
        obj = context.object
        bones = context.selected_pose_bones

        if not bones:
            self.report({'WARNING'}, "No pose bones selected")
            return {'CANCELLED'}

        self._original = {}
        self._mirrored = {}

        def is_auto_rig_pro(name):
            return name.startswith("c_") or name.startswith("c_foot_ik")

        def get_mirror_name(name):
            rules = [
                (".L", ".R"), (".R", ".L"),
                ("_L", "_R"), ("_R", "_L"),
                (".l", ".r"), (".r", ".l"),
                ("L_", "R_"), ("R_", "L_"),
            ]
            for a, b in rules:
                if name.endswith(a):
                    return name[:-len(a)] + b
                if name.startswith(a):
                    return b + name[len(a):]
            return None

        for bone in bones:
            mirror_name = get_mirror_name(bone.name)
            if not mirror_name:
                continue

            mirror_bone = obj.pose.bones.get(mirror_name)
            if not mirror_bone:
                continue

            # store original pose
            self._original[mirror_name] = (
                mirror_bone.matrix_basis.copy(),
                mirror_bone.scale.copy()
            )

            # compute inverse mirror pose (100%)
            mat = bone.matrix_basis.copy()
            name = bone.name

            if "leg" in name.lower() or "foot" in name.lower():
                mat.translation.y *= -1
            else:
                if is_auto_rig_pro(name):
                    mat.translation.y *= -1
                    q = mat.to_quaternion()
                    q.x *= -1
                    q.y *= -1
                    q.z *= -1
                    q.w *= -1
                    mat = q.to_matrix().to_4x4()
                    mat.translation = bone.location
                else:
                    q = mat.to_quaternion()
                    q.w *= -1
                    mat = q.to_matrix().to_4x4()
                    mat.translation = bone.location

            self._mirrored[mirror_name] = (
                mat,
                bone.scale.copy()
            )

        return self.execute(context)

    def execute(self, context):
        if not self._original or not self._mirrored:
            return {'CANCELLED'}

        obj = context.object
        t = self.mirror_strength / 100.0

        for name, (orig_mat, orig_scale) in self._original.items():
            mirror_mat, mirror_scale = self._mirrored.get(name, (None, None))
            if mirror_mat is None:
                continue

            pb = obj.pose.bones.get(name)
            if not pb:
                continue

            loc = orig_mat.translation.lerp(mirror_mat.translation, t)
            rot = orig_mat.to_quaternion().slerp(
                mirror_mat.to_quaternion(), t
            )
            scale = orig_scale.lerp(mirror_scale, t)

            result = rot.to_matrix().to_4x4()
            result.translation = loc

            pb.matrix_basis = result
            pb.scale = scale

        return {'FINISHED'}


def register():
    bpy.utils.register_class(MIRRORTOOL_OT_Mirror_Inverse_A1B7D)


def unregister():
    bpy.utils.unregister_class(MIRRORTOOL_OT_Mirror_Inverse_A1B7D)
