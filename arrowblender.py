bl_info = {
    "name": "Arrow Key Car Controller",
    "author": "Herohunter Pictures",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > Car Controller",
    "description": "Control cars using arrow keys",
    "category": "Object",
}

import bpy
from mathutils import Vector


key_states = {
    'UP': False,
    'DOWN': False,
    'LEFT': False,
    'RIGHT': False
}

class CARCONTROLLER_OT_drive_car(bpy.types.Operator):
    """Drive car using arrow keys"""
    bl_idname = "carcontroller.drive_car"
    bl_label = "Drive Car"
    bl_options = {'REGISTER'}

    _timer = None

    def modal(self, context, event):
        arrow_keys = {'UP_ARROW', 'DOWN_ARROW', 'LEFT_ARROW', 'RIGHT_ARROW', 'UP', 'DOWN', 'LEFT', 'RIGHT'}
        
        if event.type in arrow_keys:
            if event.value == 'PRESS':
                if event.type in {'UP_ARROW', 'UP'}:
                    key_states['UP'] = True
                elif event.type in {'DOWN_ARROW', 'DOWN'}:
                    key_states['DOWN'] = True
                elif event.type in {'LEFT_ARROW', 'LEFT'}:
                    key_states['LEFT'] = True
                elif event.type in {'RIGHT_ARROW', 'RIGHT'}:
                    key_states['RIGHT'] = True
                return {'RUNNING_MODAL'}
                
            elif event.value == 'RELEASE':
                if event.type in {'UP_ARROW', 'UP'}:
                    key_states['UP'] = False
                elif event.type in {'DOWN_ARROW', 'DOWN'}:
                    key_states['DOWN'] = False
                elif event.type in {'LEFT_ARROW', 'LEFT'}:
                    key_states['LEFT'] = False
                elif event.type in {'RIGHT_ARROW', 'RIGHT'}:
                    key_states['RIGHT'] = False
                return {'RUNNING_MODAL'}

        if event.type == 'ESC':
            self.cancel(context)
            return {'CANCELLED'}

        car_obj = context.scene.car_controller.car_object
        if car_obj:
            speed = context.scene.car_controller.speed
            rotation_speed = context.scene.car_controller.rotation_speed

            if key_states['UP']:
                car_obj.location += car_obj.matrix_world.to_3x3() @ Vector((0, speed, 0))
            if key_states['DOWN']:
                car_obj.location -= car_obj.matrix_world.to_3x3() @ Vector((0, speed, 0))
            if key_states['LEFT']:
                car_obj.rotation_euler.z += rotation_speed
            if key_states['RIGHT']:
                car_obj.rotation_euler.z -= rotation_speed

        return {'PASS_THROUGH'}

    def execute(self, context):
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.02, window=context.window)  # 50 FPS
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)
        for key in key_states:
            key_states[key] = False


class CarControllerProperties(bpy.types.PropertyGroup):
    car_object: bpy.props.PointerProperty(
        name="Car",
        type=bpy.types.Object,
        description="Select the car object to control"
    )

    speed: bpy.props.FloatProperty(
        name="Speed",
        default=0.1,
        min=0.01,
        max=1.0,
        description="Movement speed of the car"
    )

    rotation_speed: bpy.props.FloatProperty(
        name="Rotation Speed",
        default=0.05,
        min=0.01,
        max=0.5,
        description="Rotation speed of the car"
    )


class CARCONTROLLER_PT_main_panel(bpy.types.Panel):
    """Creates a Panel in the 3D Viewport N Panel"""
    bl_label = "Car Controller"
    bl_idname = "CARCONTROLLER_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Car Controller"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        car_controller = scene.car_controller

        layout.prop(car_controller, "car_object")
        layout.prop(car_controller, "speed")
        layout.prop(car_controller, "rotation_speed")
        layout.operator("carcontroller.drive_car")


def register():
    bpy.utils.register_class(CarControllerProperties)
    bpy.utils.register_class(CARCONTROLLER_OT_drive_car)
    bpy.utils.register_class(CARCONTROLLER_PT_main_panel)

    bpy.types.Scene.car_controller = bpy.props.PointerProperty(type=CarControllerProperties)


def unregister():
    bpy.utils.unregister_class(CarControllerProperties)
    bpy.utils.unregister_class(CARCONTROLLER_OT_drive_car)
    bpy.utils.unregister_class(CARCONTROLLER_PT_main_panel)

    del bpy.types.Scene.car_controller


if __name__ == "__main__":
    register()