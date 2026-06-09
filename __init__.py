# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name": "Mirror Tool",
    "author": "Bissieres Guillaume",
    "description": "An add-on to mirror selected controller in Blender",
    "blender": (3, 0, 0),
    "version": (1, 0, 5),
    "location": "View3D > Sidebar > Mirror Tool",
    "doc_url": "https://bissieres.gumroad.com/l/MirrorTool",
    "tracker_url": "https://github.com/GuillaumeBissieres/blender-mirror-tool",
    "category": "3D View",
}

import bpy
import bpy.utils.previews

# --------------------------------------------------
# IMPORT MODULES (ALL BUTTONS)
# --------------------------------------------------
from . import mirrortool_select_all_pose_bones
from . import mirrortool_select_side_controllers

from . import mirrortool_mirror_selection
from . import mirrortool_mirror_inverse
from . import mirrortool_mirror_pose
from . import mirrortool_mirror_r_to_l
from . import mirrortool_mirror_l_to_r
from . import mirrortool_mirror_all_keyframes

addon_keymaps = {}
_icons = None


# --------------------------------------------------
# PANEL (DESIGN UNCHANGED + 2 NEW BUTTONS)
# --------------------------------------------------
class MIRRORTOOL_PT_MIRROR_TOOL_3061E(bpy.types.Panel):
    bl_label = 'Mirror Tool'
    bl_idname = 'MIRRORTOOL_PT_MIRROR_TOOL_3061E'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Mirror Tool'

    def draw(self, context):
        layout = self.layout

        # --- NEW BUTTONS (ADDED) ---
        layout.operator(
            "mirrortool.select_all_pose_bones",
            text="Select All Pose Bones",
        )
        layout.operator(
            "mirrortool.select_side_controllers",
            text="Select Side Controllers",
        )

        layout.separator()

        # --- ORIGINAL DESIGN (UNCHANGED) ---
        layout.operator('mirrortool.mirror_selection_06d5a', text='Mirror Selection')
        layout.operator('mirrortool.mirror_inverse_a1b7d', text='Mirror Inverse')
        layout.operator(
            'mirrortool.mirror_pose_3977d',
            text='Mirror Pose',
            depress=context.scene.sna_boolean
        )

        row = layout.row(align=True)
        row.operator('mirrortool.mirror_r_to_l_80709', text='Mirror R to L')
        row.operator('mirrortool.mirror_l_to_r_1f6d6', text='Mirror L to R')

        layout.operator(
            'mirrortool.mirror_all_keyframes_6c1cb',
            text='Mirror All KeyFrames'
        )


# --------------------------------------------------
# REGISTER / UNREGISTER
# --------------------------------------------------
def register():
    global _icons
    _icons = bpy.utils.previews.new()

    bpy.types.Scene.sna_boolean = bpy.props.BoolProperty(default=False)

    bpy.utils.register_class(MIRRORTOOL_PT_MIRROR_TOOL_3061E)

    mirrortool_select_all_pose_bones.register()
    mirrortool_select_side_controllers.register()

    mirrortool_mirror_selection.register()
    mirrortool_mirror_inverse.register()
    mirrortool_mirror_pose.register()
    mirrortool_mirror_r_to_l.register()
    mirrortool_mirror_l_to_r.register()
    mirrortool_mirror_all_keyframes.register()


def unregister():
    mirrortool_mirror_all_keyframes.unregister()
    mirrortool_mirror_l_to_r.unregister()
    mirrortool_mirror_r_to_l.unregister()
    mirrortool_mirror_pose.unregister()
    mirrortool_mirror_inverse.unregister()
    mirrortool_mirror_selection.unregister()

    mirrortool_select_side_controllers.unregister()
    mirrortool_select_all_pose_bones.unregister()

    bpy.utils.unregister_class(MIRRORTOOL_PT_MIRROR_TOOL_3061E)

    del bpy.types.Scene.sna_boolean

    bpy.utils.previews.remove(_icons)
