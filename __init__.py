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

from distutils.sysconfig import customize_compiler
import bpy
from bpy.types import Operator, AddonPreferences
from bpy.props import FloatProperty, StringProperty
from mathutils import Matrix, Vector

bl_info = {
    "name" : "TP Tools",
    "author" : "Tiago Patricio",
    "description" : "A collection of tools to help with the Environment Art workflow",
    "blender" : (4, 1, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "View 3D"
}

# UI
class VIEW3D_PT_TP_Tools(bpy.types.Panel):
    bl_label = "TP Tools"
    bl_idname = "VIEW3D_PT_TP_Tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'TP Tools'

    def draw(self, context):
        layout = self.layout

        # Create a subfolder for Cube Creation
        box = layout.box()
        box.label(text="Blockout Tools")

        # Button to create cube
        box.operator("view3d.create_cube", text="Create 1x1 Cube")

        # Button to Add Cube
        box.operator("view3d.add_cube_interactively", text="Draw Cube")
        
        # Create a subfolder for Grid Scale settings
        box = layout.box()
        box.label(text="Grid Scale")

        # Add the rows inside the subfolder
        box_row = box.row()
        box_row.label(text="Grid Value:")

        # Display current grid scale
        box_row.prop(context.space_data.overlay, "grid_scale", text="")

        # Add a row for the multiplier slider
        box_row = box.row()
        box_row.prop(context.scene, "grid_scale_multiplier", text="Multiplier")

        # Add a row for buttons
        box_row = box.row()

        # Button to increase grid scale
        box_row.operator("view3d.grid_scale_operation", text="+").operation = 'INCREASE'

        # Button to decrease grid scale
        box_row.operator("view3d.grid_scale_operation", text="-").operation = 'DECREASE'

        box.label(text="Shortcuts: + and -")


class VIEW3D_OT_CreateCube(bpy.types.Operator):
    bl_label = "Create 1x1 Cube"
    bl_idname = "view3d.create_cube"
    bl_description = "Creates a 1x1 meter cube with its origin at the bottom face"

    def execute(self, context):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
        bpy.context.active_object.data.transform(Matrix.Translation((0.5, 0.5, 0.5)))
        return {'FINISHED'}
    
class VIEW3D_OT_AddCubeInteractively(bpy.types.Operator):
    bl_label = "Add Cube Interactively"
    bl_idname = "view3d.add_cube_interactively"
    bl_description = "Draws a cube interactively. For grid snapping, change 'Snap to:' from 'Geometry' to 'Default'"

    def execute(self, context):
        bpy.ops.wm.tool_set_by_id(name="builtin.primitive_cube_add")
        return {'FINISHED'}

# Grid Increase/Decrease behaviour
class VIEW3D_OT_GridScaleOperation(bpy.types.Operator):
    bl_label = "Grid Scale Operation"
    bl_idname = "view3d.grid_scale_operation"
    bl_description = "Increase / Decrease grid size"

    operation: bpy.props.StringProperty()

    def execute(self, context):
        multiplier = context.scene.grid_scale_multiplier
        overlay = context.space_data.overlay

        if self.operation == 'INCREASE':
            context.space_data.overlay.grid_scale *= multiplier
            self.report({'INFO'}, f"Grid: {overlay.grid_scale}")
        elif self.operation == 'DECREASE':
            context.space_data.overlay.grid_scale /= multiplier
            self.report({'INFO'}, f"Grid: {overlay.grid_scale}")
        return {'FINISHED'}


def register():
    bpy.types.Scene.grid_scale_multiplier = bpy.props.FloatProperty(name="Multiplier", default=2.0, min=0.01)
    bpy.utils.register_class(VIEW3D_PT_TP_Tools)
    bpy.utils.register_class(VIEW3D_OT_CreateCube)
    bpy.utils.register_class(VIEW3D_OT_AddCubeInteractively)
    bpy.utils.register_class(VIEW3D_OT_GridScaleOperation)


    # Define keymap entries

    # Object mode
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
    kmi = km.keymap_items.new("view3d.grid_scale_operation", 'EQUAL', 'PRESS')
    kmi.properties.operation = 'INCREASE'
    kmi = km.keymap_items.new("view3d.grid_scale_operation", 'MINUS', 'PRESS')
    kmi.properties.operation = 'DECREASE'
    # Numpad keys
    kmi = km.keymap_items.new("view3d.grid_scale_operation", 'NUMPAD_PLUS', 'PRESS')
    kmi.properties.operation = 'INCREASE'
    kmi = km.keymap_items.new("view3d.grid_scale_operation", 'NUMPAD_MINUS', 'PRESS')
    kmi.properties.operation = 'DECREASE'

    # Edit mode
    om = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
    kmi = om.keymap_items.new("view3d.grid_scale_operation", 'EQUAL', 'PRESS')
    kmi.properties.operation = 'INCREASE'
    kmi = om.keymap_items.new("view3d.grid_scale_operation", 'MINUS', 'PRESS')
    kmi.properties.operation = 'DECREASE'
    # Numpad keys
    kmi = om.keymap_items.new("view3d.grid_scale_operation", 'NUMPAD_PLUS', 'PRESS')
    kmi.properties.operation = 'INCREASE'
    kmi = om.keymap_items.new("view3d.grid_scale_operation", 'NUMPAD_MINUS', 'PRESS')
    kmi.properties.operation = 'DECREASE'



def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_TP_Tools)
    bpy.utils.unregister_class(VIEW3D_OT_CreateCube)
    bpy.utils.unregister_class(VIEW3D_OT_AddCubeInteractively)
    bpy.utils.unregister_class(VIEW3D_OT_GridScaleOperation)
    del bpy.types.Scene.grid_scale_multiplier

    # Remove keymap entries
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.get('Object Mode')
    if km:
        for kmi in km.keymap_items:
            if kmi.idname == 'view3d.grid_scale_operation':
                km.keymap_items.remove(kmi)

    om = wm.keyconfigs.addon.keymaps.get('3D View')
    if om:
        for omi in om.keymap_items:
            if omi.idname == 'view3d.grid_scale_operation':
                om.keymap_items.remove(omi)


if __name__ == "__main__":
    register()