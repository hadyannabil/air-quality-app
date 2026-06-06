class AirQualityPredictor:

    def debug_input(
        self,
        sensor_co,
        sensor_nmhc,
        sensor_nox,
        sensor_no2,
        sensor_o3,
        temperature,
        rh,
        ah,
        hour,
        month
    ):

        print("\n===== INPUT DITERIMA =====")

        print("Sensor CO      :", sensor_co)
        print("Sensor NMHC    :", sensor_nmhc)
        print("Sensor NOx     :", sensor_nox)
        print("Sensor NO2     :", sensor_no2)
        print("Sensor O3      :", sensor_o3)

        print("Temperatur     :", temperature)
        print("RH             :", rh)
        print("AH             :", ah)

        print("Jam            :", hour)
        print("Bulan          :", month)

        print("==========================\n")

        return "VALID"