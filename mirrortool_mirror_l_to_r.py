import bpy
import math
import mathutils


class MIRRORTOOL_OT_Mirror_L_To_R_1F6D6(bpy.types.Operator):
    bl_idname = "mirrortool.mirror_l_to_r_1f6d6"
    bl_label = "Mirror L to R"
    bl_description = "Mirror controllers from left to right side with adjustable strength"
    bl_options = {"REGISTER", "UNDO"}

    axis: bpy.props.EnumProperty(
        name="Axis",
        items=[('X', 'X', ''), ('Y', 'Y', ''), ('Z', 'Z', '')],
        default='X'
    )

    rotation_angle: bpy.props.FloatProperty(
        name="Rotation Angle (deg)",
        description="Extra rotation applied to mirrored bone (degrees)",
        default=0.0
    )

    mirror_strength: bpy.props.FloatProperty(
        name="Mirror Strength",
        description="Blend between original pose and mirrored pose",
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

        def is_leg_bone(name):
            return any(k in name.lower() for k in ["thigh", "calf", "foot", "ankle", "toe"])

        def get_mirror_bone_name(name):
            rules = [
                (".L", ".R"), ("_L", "_R"), (".l", ".r"),
                ("L_", "R_"),
            ]
            for a, b in rules:
                if name.endswith(a):
                    return name[:-len(a)] + b
                if name.startswith(a):
                    return b + name[len(a):]
            return None

        axis_vec_map = {
            'X': (1.0, 0.0, 0.0),
            'Y': (0.0, 1.0, 0.0),
            'Z': (0.0, 0.0, 1.0)
        }

        def invert_translation_by_axis(vec, axis):
            if axis == 'X':
                vec.x *= -1
            elif axis == 'Y':
                vec.y *= -1
            elif axis == 'Z':
                vec.z *= -1

        def invert_euler_by_axis(eul, axis):
            if axis == 'X':
                eul.y = -eul.y
                eul.z = -eul.z
            elif axis == 'Y':
                eul.x = -eul.x
                eul.z = -eul.z
            elif axis == 'Z':
                eul.x = -eul.x
                eul.y = -eul.y

        for bone in bones:
            # Apply only from Left to Right
            if bone.name.endswith(".R") or bone.name.endswith("_R") or bone.name.endswith(".r"):
                continue

            mirror_name = get_mirror_bone_name(bone.name)
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

            # compute 100% mirrored pose
            mat = bone.matrix_basis.copy()
            invert_translation_by_axis(mat.translation, self.axis)
            eul = mat.to_euler()

            if is_auto_rig_pro(bone.name) and is_leg_bone(bone.name):
                if self.axis == 'X':
                    eul.x = -eul.x
                    eul.z = -eul.z
                elif self.axis == 'Y':
                    eul.x = -eul.x
                    eul.z = -eul.z
                elif self.axis == 'Z':
                    eul.x = -eul.x
                    eul.y = -eul.y
            else:
                invert_euler_by_axis(eul, self.axis)

            mirror_mat = eul.to_matrix().to_4x4()
            mirror_mat.translation = mat.translation

            if abs(self.rotation_angle) > 1e-6:
                rot = mathutils.Matrix.Rotation(
                    math.radians(self.rotation_angle), 4, axis_vec_map[self.axis]
                )
                mirror_mat = rot @ mirror_mat

            self._mirrored[mirror_name] = (
                mirror_mat,
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
    bpy.utils.register_class(MIRRORTOOL_OT_Mirror_L_To_R_1F6D6)


def unregister():
    bpy.utils.unregister_class(MIRRORTOOL_OT_Mirror_L_To_R_1F6D6)
