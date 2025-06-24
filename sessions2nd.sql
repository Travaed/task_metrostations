WITH prev_date AS (
    SELECT uid, start_dttm, stop_dttm, LAG(stop_dttm) OVER(PARTITION BY uid ORDER BY start_dttm) AS prevstopt
    FROM wifi_session
)
SELECT *
FROM prev_date
WHERE start_dttm < prevstopt
ORDER BY uid;

WITH last_sessions AS (
    SELECT 
        uid,
        DATE(stop_dttm) AS session_date,
        stop_station,
        ROW_NUMBER() OVER (PARTITION BY uid, DATE(stop_dttm) ORDER BY stop_dttm DESC) AS rn
    FROM 
        wifi_session
),
count_stations AS (
    SELECT 
        uid,
        stop_station,
        COUNT(*) AS station_count
    FROM 
        last_sessions
    WHERE 
        rn = 1 
    GROUP BY 
        uid, stop_station
),
ranked_stations AS (
    SELECT 
        uid,
        stop_station,
        station_count,
        RANK() OVER (PARTITION BY uid ORDER BY station_count DESC) AS rn
    FROM 
        count_stations
)
SELECT 
    uid,
    stop_station
FROM 
    ranked_stations
WHERE 
    rn = 1;