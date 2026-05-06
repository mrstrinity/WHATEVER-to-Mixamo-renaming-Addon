bl_info = {
          "name": "Whatever to Mixamo!",
          "author": "mrstrinity",
          "version": (1, 0),
          "blender": (3, 6, 15),
          "location": "View3D > Sidebar > WHATEVER!",
          "category": "Rigging",
          "description": "Rename bones to the Mixamo Counterpart."
}

# You need this, or it just won't work
import bpy
from bl_operators.presets import AddPresetBase
from bpy.types import Menu

#Mixamo bonelist
MIXAMO_BONES = [
          "mixamorig:Hips",
          "mixamorig:Spine",
          "mixamorig:Spine1",
          "mixamorig:Spine2",
          "mixamorig:Neck",
          "mixamorig:Head",
          
          "mixamorig:LeftUpLeg",
          "mixamorig:RightUpLeg",
          "mixamorig:LeftLeg",
          "mixamorig:RightLeg",
          "mixamorig:LeftFoot",
          "mixamorig:RightFoot",
          "mixamorig:LeftToeBase",
          "mixamorig:RightToeBase", 
          
          "mixamorig:LeftShoulder",
          "mixamorig:RightShoulder",
          "mixamorig:LeftForeArm",
          "mixamorig:RightForeArm",
          "mixamorig:LeftArm",
          "mixamorig:RightArm",
          "mixamorig:LeftHand",
          "mixamorig:RightHand",
          
          "mixamorig:LeftHandThumb1",
          "mixamorig:RightHandThumb1",
          "mixamorig:LeftHandThumb2",
          "mixamorig:RightHandThumb2",
          "mixamorig:LeftHandThumb3",
          "mixamorig:RightHandThumb3",
          
          "mixamorig:LeftHandIndex1",
          "mixamorig:RightHandIndex1",
          "mixamorig:LeftHandIndex2",
          "mixamorig:RightHandIndex2",
          "mixamorig:LeftHandIndex3",
          "mixamorig:RightHandIndex3",
          
          "mixamorig:LeftHandMiddle1",
          "mixamorig:RightHandMiddle1",
          "mixamorig:LeftHandMiddle2",
          "mixamorig:RightHandMiddle2",
          "mixamorig:LeftHandMiddle3",
          "mixamorig:RightHandMiddle3",
          
          "mixamorig:LeftHandRing1",
          "mixamorig:RightHandRing1",
          "mixamorig:LeftHandRing2",
          "mixamorig:RightHandRing2",
          "mixamorig:LeftHandRing3",
          "mixamorig:RightHandRing3",
          
          "mixamorig:LeftHandPinky1",
          "mixamorig:RightHandPinky1",
          "mixamorig:LeftHandPinky2",
          "mixamorig:RightHandPinky2",
          "mixamorig:LeftHandPinky3",
          "mixamorig:RightHandPinky3",
          
          "Eye.L",
          "Eye.R",
          
          "Bust1.L",
          "Bust1.R",
          "Bust2.L",
          "Bust2.R",
          ]

class MIXAMO_Props(bpy.types.PropertyGroup):
          pass

for bone in MIXAMO_BONES:
          
          prop_name = bone.lower().replace(":", "_").replace(".", "_")
          
          if not hasattr(MIXAMO_Props, "__annotations__"):
                    MIXAMO_Props.__annotations__ = {}
                    
          MIXAMO_Props.__annotations__[prop_name] = bpy.props.StringProperty(
                                                                              name=bone
                                                                      )
          
class MIXAMO_OT_rename(bpy.types.Operator):
          bl_idname = "mixamo.rename_bones"
          bl_label = "Rename Bones to Mixamo"
          
          def execute(self, context):
                    obj = context.object
                    
                    if not obj or obj.type != 'ARMATURE':
                              self.report({'ERROR'}, "Select an Armature")
                              return {'CANCELLED'}
                              
                    props = context.scene.mixamo_props
                    
                    for bone in MIXAMO_BONES:
                              prop_name = bone.lower().replace(":", "_").replace(".", "_")
                              selected_bone = getattr(props, prop_name)
                              
                              if selected_bone and selected_bone in obj.data.bones:
                                        obj.data.bones[selected_bone].name = bone
                              
                    self.report({'INFO'}, "Renamed!")                              
                    return {'FINISHED'}

# Add and save renaming presets.
class MIXAMO_OT_add_preset(AddPresetBase, bpy.types.Operator):
          bl_idname = "mixamo.add_preset"
          bl_label = "Save Template"
          preset_menu = "MIXAMO_MT_presets"
          
          # Where presets are saved.
          preset_subdir = "renaming_templates"
          preset_operator = "script.execute_preset"
          
          # What gets saved?
          preset_values = [
                    f"scene.mixamo_props.{bone.lower().replace(':','_').replace('.','_')}"
                    for bone in MIXAMO_BONES
          ]
          
          preset_defines = [
                    "scene = bpy.context.scene"
          ]
          
class MIXAMO_MT_presets(bpy.types.Menu):
          bl_label = "Templates"
          bl_idname = "MIXAMO_MT_presets"
          preset_subdir = "renaming_templates"
          preset_operator = "script.execute_preset"
          
          draw = Menu.draw_preset
          
# The UI                              
class WHATEVER_PT_panel(bpy.types.Panel):
          bl_label = "Mixamo Bone Renamer"
          bl_idname = "WHATEVER_PT_panel"
          bl_space_type = "VIEW_3D"
          bl_region_type = "UI"
          bl_category = "WHATEVER!"
          
          def draw(self, context):
                    layout = self.layout
                    props = context.scene.mixamo_props
                    
                    obj = context.object
                    
                    # Is the armature selected?
                    if not obj or obj.type != 'ARMATURE':
                              layout.label(text="You might need to select an Armature first, bud.")
                              return
                    
                    layout.label(text="Fill in the blanks.", icon="GREASEPENCIL")
                    
                    # Preset UI
                    row = layout.row()
                    
                    row.menu("MIXAMO_MT_presets", text="Select Preset...")
                    row.operator("mixamo.add_preset", text="", icon='ADD')
                    row.operator("mixamo.add_preset", text="", icon='REMOVE').remove_active = True
                    
                    # Renaming UI
                    col = layout.column()
                    
                    for bone in MIXAMO_BONES:
                              prop_name = bone.lower().replace(":", "_").replace(".", "_")
                              
                              col.prop_search(
                                              props,
                                              prop_name,
                                              obj.data,
                                              "bones"
                                        )
                    
                              
                    layout.separator()
                    
                    layout.label(text="I'd save a preset for later, if I were you.", icon="INFO")
                    
                    # References what class is going to function by bl_idname. This is the button.
                    layout.operator("mixamo.rename_bones", icon="SMALL_CAPS")
                    
                    
                    

classes = (
           MIXAMO_Props,
           MIXAMO_OT_rename,
           MIXAMO_OT_add_preset,
           WHATEVER_PT_panel,
           MIXAMO_MT_presets,
           )

def register():
          for c in classes:
                    bpy.utils.register_class(c)
                    
          bpy.types.Scene.mixamo_props = bpy.props.PointerProperty(type=MIXAMO_Props)
          
def unregister():
          for c in reversed(classes):
                    bpy.utils.unregister_class(c)
                    
          del bpy.types.Scene.mixamo_props
          
if __name__ == "__main__":
          register()