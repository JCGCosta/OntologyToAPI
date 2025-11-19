async def convert_temperature_c_to_f(data):
    if not data.metadata and data.params["temperature_c"] is None:
        return {"error": "No temperature was provided from Metadata or from the endpoint Parameters."}
    if data.params["temperature_c"] is not None:
        return {
            "original": data.params["temperature_c"],
            "converted": data.params["temperature_c"] * 9 / 5 + 32
        }
    else:
        return {
            "original": [t["temperature_c"] for t in data.metadata["Temperature_C_MD"]],
            "converted": [t["temperature_c"] * 9 / 5 + 32 for t in data.metadata["Temperature_C_MD"]]
        }
