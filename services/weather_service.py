from tools import weather as openweather


def get_weather(city):

    result = openweather.get_weather(city)

    # ✅ éxito directo
    if result["status"] == "success":
        return result

    # ⚠️ fallback aún no implementado
    if result.get("error", {}).get("retryable"):
        print("[INFO] retryable error detected (fallback not implemented yet)")

    return result