import joblib
import numpy as np
import os

class AirQualityPredictor:

    def __init__(self):
        model_path = os.path.join(
            os.path.dirname(__file__), "..", "models", "model.pkl"
        )
        self.model = joblib.load(model_path)

    def predict(
        self,
        sensor_co,      # PT08.S1(CO)
        nmhc_gt,        # NMHC(GT)
        c6h6_gt,        # C6H6(GT)
        sensor_nmhc,    # PT08.S2(NMHC)
        nox_gt,         # NOx(GT)
        sensor_nox,     # PT08.S3(NOx)
        no2_gt,         # NO2(GT)
        sensor_no2,     # PT08.S4(NO2)
        sensor_o3,      # PT08.S5(O3)
        temperature,    # T
        rh,             # RH
        ah,             # AH
        month,          # Month
        hour,           # Hour
    ):
        # Urutan fitur sesuai dengan training:
        # ['PT08.S1(CO)', 'NMHC(GT)', 'C6H6(GT)', 'PT08.S2(NMHC)',
        #  'NOx(GT)', 'PT08.S3(NOx)', 'NO2(GT)', 'PT08.S4(NO2)',
        #  'PT08.S5(O3)', 'T', 'RH', 'AH', 'Month', 'Hour']
        data = np.array([[
            sensor_co,
            nmhc_gt,
            c6h6_gt,
            sensor_nmhc,
            nox_gt,
            sensor_nox,
            no2_gt,
            sensor_no2,
            sensor_o3,
            temperature,
            rh,
            ah,
            month,
            hour,
        ]])

        hasil = self.model.predict(data)
        return float(hasil[0])
