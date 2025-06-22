SELECT uid, count(*)
FROM wifi_session
WHERE start_dttm >=  now() - interval '3 month' AND (start_station in (50, 161) OR  stop_station in (161, 50))          -- Учитывал 3 месяца от сегодняшней даты
GROUP BY uid
HAVING count(*) >= 50
;
SELECT*
FROM wifi_session a
  JOIN 
    wifi_session b ON a.uid = b.uid 
                    AND a.start_dttm < b.stop_dttm 
                    AND a.start_dttm > b.start_dttm
ORDER BY a.uid, a.start_dttm
;    
SELECT start_station,
    COUNT(*) AS visit_count
FROM wifi_session
GROUP BY start_station           -- Считал используюму станцию, откуда начинают движение
ORDER BY visit_count DESC
LIMIT 10
;
WITH user_station_counts AS (
    SELECT 
        uid,
        stop_station,
        COUNT(*) AS total_sessions
    FROM 
        wifi_session
    GROUP BY 
        uid, stop_station
),
ranked_stations AS (
    SELECT 
        uid,
        stop_station,
        total_sessions,
        RANK() OVER (PARTITION BY uid ORDER BY total_sessions DESC) AS rnk  -- Учитывая, что таких станций может быть не одна
    FROM 
        user_station_counts
)
SELECT 
    uid,
    stop_station
FROM 
    ranked_stations
WHERE 
    rnk = 1
;

