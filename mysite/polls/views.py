from django.shortcuts import render
from django.http import JsonResponse
from .management.commands.uptime import get_uptime
from .management.commands import relay
import json
from threading import Thread
from channels.generic.websocket import AsyncWebsocketConsumer


def home(request):
    return render(request, 'home.html')


def pwr(request):
    return render(request, 'pwr.html')


def storage(request):
    return render(request, 'storage.html')


def connectivity(request):
    return render(request, 'connectivity.html')


def support(request):
    return render(request, 'support.html')


def thanks(request):
    return render(request, 'thanks.html')


def router_uptime(request):
    # Call get_uptime and pass "router" as the device identifier
    return get_uptime(request, "router")


def camera_uptime(request):
    # Call get_uptime and pass "camera" as the device identifier
    return get_uptime(request, "camera")


def control_device(request, device_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            action = data.get('action')

            device_functions = {
                'CameraOn': relay.turn_on_camera,
                'CameraOff': relay.turn_off_camera,
                'FanOn': relay.turn_on_fan,
                'FanOff': relay.turn_off_fan,
                'Fan5Min': relay.run_fan_for_5_minutes,
                'StrobeOn': relay.turn_on_strobe,
                'StrobeOff': relay.turn_off_strobe,
                'Strobe5Min': relay.run_strobe_for_5_minutes,
                # 'RouterReset': relay.reset_router,  # We will handle RouterReset separately.
            }

            # Special handling for RouterReset action
            if action == 'RouterReset':
                def async_reset_router():
                    relay.reset_router()
                    # No additional actions needed after reset in this thread.

                # Start the reset operation in a background thread.
                Thread(target=async_reset_router).start()

                # Immediately respond with "Resetting" status.
                return JsonResponse({'message': 'Resetting Router', 'status': 'Resetting'})

            # Handling other device actions.
            elif action in device_functions:
                device_functions[action]()
                return JsonResponse({'message': f'Successfully executed {action} on {device_id}'})

            else:
                return JsonResponse({'error': 'Invalid device ID or action.'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)


def gpio_status(request):
    status = {
        'camera': relay.get_camera_state(),
        'fan': relay.get_fan_state(),
        'strobe': relay.get_strobe_state(),
        'router': relay.get_router_state(),
    }
    return JsonResponse(status)


class GPIOStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'get_status':
            status = {
                'camera': relay.get_camera_state(),
                'fan': relay.get_fan_state(),
                'strobe': relay.get_strobe_state(),
                'router': relay.get_router_state(),
            }
            await self.send(text_data=json.dumps(status))
        elif action == 'RouterReset':
            Thread(target=self.router_reset_logic).start()
            await self.send(text_data=json.dumps({'router': 'Resetting'}))
        elif action in ('CameraOn', 'CameraOff', 'FanOn', 'FanOff', 'StrobeOn', 'StrobeOff'):
            # Handle the other GPIO control actions here
            # Call the corresponding functions from the relay module
            relay_functions = {
                'CameraOn': relay.turn_on_camera,
                'CameraOff': relay.turn_off_camera,
                'FanOn': relay.turn_on_fan,
                'FanOff': relay.turn_off_fan,
                'StrobeOn': relay.turn_on_strobe,
                'StrobeOff': relay.turn_off_strobe,
            }
            if action in relay_functions:
                relay_functions[action]()
                # Optionally, send a response to confirm the action if needed
                await self.send(text_data=json.dumps({'message': f'Successfully executed {action}'}))
        if action == 'Fan5Min':
            relay.run_fan_for_5_minutes()
            await self.send(text_data=json.dumps({'message': 'Fan running for 5 minutes'}))
        elif action == 'Strobe5Min':
            relay.run_strobe_for_5_minutes()
            await self.send(text_data=json.dumps({'message': 'Strobe running for 5 minutes'}))
    def router_reset_logic(self):
        # This method runs the reset logic in a separate thread
        relay.reset_router()
