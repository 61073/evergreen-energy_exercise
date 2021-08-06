from unittest import TestCase
from nose2.tools import params
from src.app.data_calculator import DataCalculator, calculate_heat_loss, calculate_power_heat_loss, get_heat_pump_data

example_house_data = {
    "submissionId": "abc123",
    "designRegion": "Severn Valley (Filton)",
    "floorArea": 150,
    "age": "1967 - 1975",
    "heatingFactor": 100,
    "insulationFactor": 1.1
}

example_heat_pump_5kw = {
    "label": "5kW Package",
    "outputCapacity": 5,
    "costs": [
        {"label": "Design & Supply of your Air Source Heat Pump System Components (5kW)", "cost": 3947},
        {"label": "Installation of your Air Source Heat Pump and Hot Water Cylinder", "cost":  2900},
        {"label": "Supply & Installation of your Homely Smart Thermostat", "cost": 150},
        {"label": "Supply & Installation of a new Consumer Unit", "cost": 300},
        {"label": "MCS System Commissioning & HIES Insurance-backed Warranty", "cost": 1648}
    ]
}

example_heat_pump_12kw = {
    "label": "12kW Package",
    "outputCapacity": 12,
    "costs": [
        {"label": "Design & Supply of your Air Source Heat Pump System Components (12kW)", "cost": 5138},
        {"label": "Installation of your Air Source Heat Pump and Hot Water Cylinder", "cost": 2900},
        {"label": "Supply & Installation of your Homely Smart Thermostat", "cost": 150},
        {"label": "Supply & Installation of a new Consumer Unit", "cost": 300},
        {"label": "MCS System Commissioning & HIES Insurance-backed Warranty", "cost": 1648}
    ]
}

success_example = """"--------------------------------------
abc123
--------------------------------------
Estimated Heat Loss = 16500
Design Region = Severn Valley (Filton)
Power Heat Loss = 8.25
Recommended Heat Pump = 12kW Package
Cost Breakdown:
 Design & Supply of your Air Source Heat Pump System Components (12kW), 5138
 Installation of your Air Source Heat Pump and Hot Water Cylinder, 2900
 Supply & Installation of your Homely Smart Thermostat, 150
 Supply & Installation of a new Consumer Unit, 300
 MCS System Commissioning & HIES Insurance-backed Warranty, 1648
Total Cost, including VAT = 10642.8"""


class TestDataCalculator(TestCase):

    def test_success_init(self):
        calculator_obj = DataCalculator(example_house_data)
        self.assertEqual(101, calculator_obj.heating_factor)
        self.assertEqual(1.3, calculator_obj.insulation_factor)
        self.assertEqual(125, calculator_obj.floor_area)
        self.assertEqual("abc123", calculator_obj.id)
        self.assertEqual("Severn Valley (Filton)", calculator_obj.location)

    def test_process_results(self):
        calculator_obj = DataCalculator(example_house_data)
        actual_results = calculator_obj.process_results()
        self.assertEqual(success_example, actual_results)

    @params((100, 50, 1.5, 7500.0), (80, 75, 1.0, 6000.0))
    def test_calculate_heat_loss(self, floor_area, heating_factor, insulation_factor, expected_heat_loss):
        actual_heat_loss = calculate_heat_loss(floor_area, heating_factor, insulation_factor)
        self.assertEqual(expected_heat_loss, actual_heat_loss)

    @params((20000, 2000, 10.0), (7000, 2500, 2.8))
    def test_calculate_power_heat_loss(self, heat_loss, degree_days, expected_power_heat_loss):
        actual_power_heat_loss = calculate_power_heat_loss(heat_loss, degree_days)
        self.assertEqual(expected_power_heat_loss, actual_power_heat_loss)

    @params((10.0, example_heat_pump_12kw), (2.8, example_heat_pump_5kw))
    def test_get_heat_pump_data(self, power_heat_loss, expected_output):
        actual_output = get_heat_pump_data(power_heat_loss)
        self.assertEqual(expected_output, actual_output)