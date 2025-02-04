<?php
// URL de la API de Open-Meteo
$url = "https://api.open-meteo.com/v1/forecast?latitude=40.2842&longitude=-3.7942&daily=temperature_2m_max,temperature_2m_min&timezone=Europe/Madrid&forecast_days=3";

// Realizar la solicitud GET a la API
$response = file_get_contents($url);

// Decodificar la respuesta JSON
$data = json_decode($response, true);

// Mostrar las temperaturas máximas y mínimas para los próximos 3 días
for ($i = 0; $i < 3; $i++) {
    echo "Día " . ($i + 1) . ":\n";
    echo "  Máxima: " . $data['daily']['temperature_2m_max'][$i] . "°C\n";
    echo "  Mínima: " . $data['daily']['temperature_2m_min'][$i] . "°C\n";
}
?>