# blender-mirror-tool

An add-on to mirror selected controller in Blender

<img width="1200" height="600" alt="Mirror Tool" src="https://github.com/user-attachments/assets/b823c1b5-eec2-4540-9988-993b6e457795" />

#

Mirror Tool is an animation and rigging utility that allows users to mirror transformations across rig controllers. It supports standard custom rigs as well as generated rigs from Auto Rig Pro and Rigify. The tool copies position, rotation, and scale data from one side of a rig to the other while maintaining orientation consistency to avoid distortion.

The interface provides controls for instantaneous mirroring, including specific left-to-right or right-to-left operations. Users can blend between the original and mirrored pose in real time using an adjustable strength slider. Additional features include one-click selection isolation for specific rig sides, bulk keyframe mirroring for active controls, and inverse target operations.

# Installation
Download the ZIP file.

Open Blender and go to **Edit** > **Preferences** > **Add-ons**.

Click **Install**, select the ZIP file, and click **Install Add-on**.

Enable the add-on by checking the corresponding box.

Access **Mirror Tool** in the **N menu** (sidebar) under the **Fill Mesh tab**.

# How to Use Mirror Tool
1. **Select a controller** : Choose the control bone whose transformations you want to mirror.

2. **Execute and choose the mirroring option** :

	• **Mirror Selection** : Mirror selected controler.

	• **Mirror Inverse** : Flip the transformation to the opposite side of the selected controller.

	• **Mirror Pose** : Enable or Disable the Mirror Pose option already in Blender. Apply changes to matching bone on opposite side of x-axis.

	• **Mirror R to L & Mirror L to R** : Quickly flip selected poses or animations across the character's symmetry axis.

	• **Mirror All KeyFrames** : Flip entire animation and all keyframes across the character's symmetry axis.

3. **Adjust if needed** : Fine-tune position or rotation manually if necessary.

# Advanced Options
**Automatic Detection** – Identifies and mirrors controllers based on naming conventions (e.g., .L ↔ .R, _L ↔ _R).

**Supports Multiple Rigs** – Works with Auto Rig Pro, Blender’s default rigs, and custom controllers.

**Preserves Natural Motion** – Ensures proper orientation without flipping unwanted axes.

**Works for Rotation, Location & Scale** – Handles all transformation properties seamlessly.

  • **Mirror IK & FK Controllers** – Ensures proper mirroring for both inverse and forward kinematics setups.
  
  • **Axis Compensation** – Prevents unwanted flipping by intelligently adjusting Euler rotations.

  • **Manual Selection Override** – Allows users to manually define the mirrored bone for custom setups.
  
