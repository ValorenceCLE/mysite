from django.db import models
import uuid


class Raspberry_Pi(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Serial_Number = models.CharField(max_length=30)
    System_Name = models.CharField(max_length=100)


class Router(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Router_ID = models.CharField(max_length=30)
    Model = models.CharField(max_length=40)
    raspberry_pi = models.ForeignKey(Raspberry_Pi, on_delete=models.CASCADE, related_name='router')


class Camera(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Camera_ID = models.CharField(max_length=30)
    Model = models.CharField(max_length=30)
    raspberry_pi = models.ForeignKey(Raspberry_Pi, on_delete=models.CASCADE, related_name='cameras')


class Environmental(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Date_Time = models.DateTimeField()
    SensorID = models.CharField(max_length=45)
    Temperature = models.FloatField()
    Humidity = models.FloatField()
    raspberry_pi = models.ForeignKey(Raspberry_Pi, on_delete=models.CASCADE, related_name='environmental')


class Camera_Power(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Date_Time = models.DateTimeField()
    Volts = models.FloatField()
    Watts = models.FloatField()
    Amps = models.FloatField()
    Sensor_ID = models.CharField(max_length=50)
    Camera_Model = models.CharField(max_length=50, default="Unknown")


class Router_Power(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Date_Time = models.DateTimeField()
    Volts = models.FloatField()
    Watts = models.FloatField()
    Amps = models.FloatField()
    Sensor_ID = models.CharField(max_length=50)
    Router_Model = models.CharField(max_length=50, default="Unknown")


class Cellular_Data(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Date_Time = models.DateTimeField()
    RSSI = models.IntegerField()
    RSRP = models.IntegerField()
    RSRQ = models.IntegerField()
    SINR = models.IntegerField()
    Router_Model = models.CharField(max_length=50, default="Unknown")


class Connection_Speed(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Date_Time = models.DateTimeField()
    Up_Speed = models.FloatField()
    Down_Speed = models.FloatField()
    raspberry_pi = models.ForeignKey(Raspberry_Pi, on_delete=models.CASCADE, related_name='connection_speed')


