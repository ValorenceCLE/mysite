from django.shortcuts import render
from django.http import JsonResponse
from .management.commands.uptime import get_uptime
from .management.commands import relay
import json
from threading import Thread
from channels.generic.websocket import AsyncWebsocketConsumer
from .management.commands.ina260 import INA260Sensor
from .management.commands.aht10 import AHT10
from asgiref.sync import sync_to_async
import asyncio
import time

def home(request):
    return render(request, 'home.html')

def system(request):
    return render(request, 'system.html')

def connectivity(request):
    return render(request, 'connectivity.html')

def support(request):
    return render(request, 'support.html')

def thanks(request):
    return render(request, 'thanks.html')

def router_uptime(request):
    return get_uptime(request, "router")


def camera_uptime(request):
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
                'RouterReset': relay.reset_router,
            }

            if action in device_functions:
                if action == 'RouterReset':
                    Thread(target=lambda: asyncio.run(async_reset_router(None))).start()
                    return JsonResponse({'message': 'Restarting Router', 'status': 'Restarting'})
                else:
                    device_functions[action]()
                    return JsonResponse({'message': f'Successfully executed {action} on {device_id}'})
            else:
                return JsonResponse({'error': 'Invalid device ID or action.'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

async def async_reset_router(consumer):
    # This function runs the reset logic asynchronously
    relay.reset_router()
    await asyncio.sleep(10)  # Simulate 10 seconds delay
    if consumer:
        await consumer.send_status()

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
            await self.send_status()
        elif action == 'RouterReset':
            asyncio.create_task(async_reset_router(self))
            await self.send(json.dumps({'router': 'Restarting'}))
        elif action in ('CameraOn', 'CameraOff', 'FanOn', 'FanOff', 'StrobeOn', 'StrobeOff'):
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
                await self.send_status()
        elif action == 'Fan5Min' or action == 'Strobe5Min':
            if action == 'Fan5Min':
                relay.run_fan_for_5_minutes()
            else:
                relay.run_strobe_for_5_minutes()
            await self.send_status()

    async def send_status(self):
        status = {
            'camera': relay.get_camera_state(),
            'fan': relay.get_fan_state(),
            'strobe': relay.get_strobe_state(),
            'router': relay.get_router_state(),
        }
        await self.send(json.dumps(status))

class SensorDataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.aht10_sensor = AHT10()
        self.ina260_sensor = INA260Sensor()
        self.last_temperature = None
        self.last_voltage = None
        asyncio.create_task(self.send_sensor_data_when_changed())

    async def disconnect(self, close_code):
        pass

    async def send_sensor_data_when_changed(self):
        while True:
            temperature = await sync_to_async(self.aht10_sensor.read_temperature)()
            voltage_V = await sync_to_async(self.ina260_sensor.get_voltage_volts)()

            if temperature != self.last_temperature or voltage_V != self.last_voltage:
                self.last_temperature = temperature
                self.last_voltage = voltage_V
                await self.send(json.dumps({
                    'temperature': temperature,
                    'voltage_V': voltage_V,
                }))

            await asyncio.sleep(3)
