HOST = "158.23.62.92"
PORT = 1883

CENTERS = [
    {
        "name": "A-15",
        "gateway_token": "vnA6AhbUpvWm55EQ7esZ",

        "power_meters": [
            {
                "name": "pm-general",
                "real_energy": 194635227.0,
                "reactive_energy": 14511069.0,
                "apparent_energy": 197810189.0,
            },
            {
                "name": "pm-habitabilidad",
                "real_energy": 21639347.0,
                "reactive_energy": 335969.0,
                "apparent_energy": 22408519.0,
            },
            {
                "name": "pm-fotoperiodo",
                "real_energy": 112435816.0,
                "reactive_energy": 97.0,
                "apparent_energy": 112497081.0,
            },
            {
                "name": "pm-alimentacion",
                "real_energy": 25163321.0,
                "reactive_energy": 9651433.0,
                "apparent_energy": 29185387.0,
            },
            {
                "name": "pm-alimentacion2",
                "real_energy": 11455637.0,
                "reactive_energy": 4352945.0,
                "apparent_energy": 13275347.0,
            },
            {
                "name": "pm-gen-aux",
                "real_energy": 68917773.0,
                "reactive_energy": 7049105.0,
                "apparent_energy": 70230704.0,
            },
            {
                "name": "pm-gen-general",
                "real_energy": 98727530.0,
                "reactive_energy": 5652782.0,
                "apparent_energy": 100004573.0,
            },
        ],

        "dfms": [
            {
                "name": "dfm-general",
                "total_fuel": 32306.625,
                "hours_op": 2470.2094444444447,
            },
            {
                "name": "dfm-aux",
                "total_fuel": 30424.862,
                "hours_op": 1722.661111111111,
            },
        ],
        "tanks": [
            {
                "name": "estanque",
                "level": 3521.73,
                "max_level": 10000.0,
            }
        ]
    }
]
