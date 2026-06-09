import bpy
import math
import mathutils


class MIRRORTOOL_OT_Mirror_Selection_06D5A(bpy.types.Operator):
    bl_idname = "mirrortool.mirror_selection_06d5a"
    bl_label = "Mirror Selection"
    bl_description = "Mirror selected controller(s) with adjustable strength"
    bl_options = {"REGISTER", "UNDO"}

    axis: bpy.props.EnumProperty(
        name="Axis",
        items=[('X', 'X', ''), ('Y', 'Y', ''), ('Z', 'Z', '')],
        default='X'
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
            obj is not None
            and obj.type == 'ARMATURE'
            and context.mode == 'POSE'
        )

    # -------------------------------------------------
    # INTERNAL STORAGE (per operator instance)
    # -------------------------------------------------
    _original_matrices = None
    _mirror_matrices = None

    def invoke(self, context, event):
        """Store original and mirrored poses once."""
        obj = context.object
        selected_bones = context.selected_pose_bones

        if not selected_bones:
            self.report({'WARNING'}, "No pose bones selected")
            return {'CANCELLED'}

        self._original_matrices = {}
        self._mirror_matrices = {}

        for bone in selected_bones:
            mirror_name = self._get_mirror_name(bone.name)
            if not mirror_name:
                continue

            mirror_bone = obj.pose.bones.get(mirror_name)
            if not mirror_bone:
                continue

            # Store original pose of mirror bone
            self._original_matrices[mirror_name] = (
                mirror_bone.matrix_basis.copy(),
                mirror_bone.scale.copy()
            )

            # Compute 100% mirror pose
            mat = bone.matrix_basis.copy()
            self._invert_translation_by_axis(mat.translation, self.axis)

            eul = mat.to_euler()
            self._invert_euler_by_axis(eul, self.axis)

            mirror_mat = eul.to_matrix().to_4x4()
            mirror_mat.translation = mat.translation

            self._mirror_matrices[mirror_name] = (
                mirror_mat,
                bone.scale.copy()
            )

        return self.execute(context)

    def execute(self, context):
        if not self._original_matrices or not self._mirror_matrices:
            return {'CANCELLED'}

        strength = self.mirror_strength / 100.0
        obj = context.object

        for name, (orig_mat, orig_scale) in self._original_matrices.items():
            mirror_mat, mirror_scale = self._mirror_matrices.get(name, (None, None))
            if mirror_mat is None:
                continue

            pb = obj.pose.bones.get(name)
            if not pb:
                continue

            # Blend transforms
            loc = orig_mat.translation.lerp(mirror_mat.translation, strength)
            rot = orig_mat.to_quaternion().slerp(
                mirror_mat.to_quaternion(), strength
            )
            scale = orig_scale.lerp(mirror_scale, strength)

            result = rot.to_matrix().to_4x4()
            result.translation = loc

            pb.matrix_basis = result
            pb.scale = scale

        return {'FINISHED'}

    # -------------------------------------------------
    # UTILS
    # -------------------------------------------------
    def _invert_translation_by_axis(self, vec, axis):
        if axis == 'X':
            vec.x *= -1
        elif axis == 'Y':
            vec.y *= -1
        elif axis == 'Z':
            vec.z *= -1

    def _invert_euler_by_axis(self, eul, axis):
        if axis == 'X':
            eul.y = -eul.y
            eul.z = -eul.z
        elif axis == 'Y':
            eul.x = -eul.x
            eul.z = -eul.z
        elif axis == 'Z':
            eul.x = -eul.x
            eul.y = -eul.y

    def _get_mirror_name(self, name):
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


def register():
    bpy.utils.register_class(MIRRORTOOL_OT_Mirror_Selection_06D5A)


def unregister():
    bpy.utils.unregister_class(MIRRORTOOL_OT_Mirror_Selection_06D5A)
