import pytest
from datetime import datetime

from app.weather import get_sun

def test_weather():
   a, b = get_sun('Dallas')
   assert isinstance(a, datetime)
   assert isinstance(b, datetime)

