import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from main import adjusted_index, classify, heat_index_c  # noqa: E402

HERE = os.path.dirname(__file__)


def test_mild_weather_is_low():
    assert classify(heat_index_c(25, 40)) == "Low"


def test_hot_humid_is_dangerous():
    hi = heat_index_c(35, 70)
    assert hi > 45
    assert classify(hi) in ("Danger", "Extreme")


def test_heavy_work_raises_risk():
    assert adjusted_index(30, "construction") == 33
    assert adjusted_index(30, "office") == 30


def test_sample_data():
    with open(os.path.join(HERE, "sample_data.json")) as f:
        cases = json.load(f)
    for c in cases:
        hi = heat_index_c(c["temp_c"], c["humidity"])
        assert classify(adjusted_index(hi, c["job"])) == c["expected"]
