
-- Lab 5 Part F: write your queries for the assistant database here.

-- Q1 requests per intent
SELECT
    intent,
    COUNT(*) AS total_requests
FROM interaction
GROUP BY intent
ORDER BY total_requests DESC;


-- Q2 average latency per intent
SELECT
    intent,
    ROUND(AVG(latency_ms), 1) AS avg_latency_ms
FROM interaction
GROUP BY intent
ORDER BY avg_latency_ms DESC;


-- Q3 topics with the most thumbs-down (JOIN feedback with interaction)
SELECT
    i.topic,
    COUNT(*) AS thumbs_down_count
FROM interaction AS i
JOIN feedback AS f
    ON i.request_id = f.request_id
WHERE f.rating = -1
    AND i.topic IS NOT NULL
GROUP BY i.topic
ORDER BY thumbs_down_count DESC;

-- H2: Which intent has the highest unresolved rate?

SELECT
    intent,
    COUNT(*) AS total_requests,
    SUM(CASE WHEN resolved = 0 THEN 1 ELSE 0 END) AS unresolved_requests,
    ROUND(
        100.0 * SUM(CASE WHEN resolved = 0 THEN 1 ELSE 0 END)
        / COUNT(*),
        1
    ) AS unresolved_rate
FROM interaction
GROUP BY intent
ORDER BY unresolved_rate DESC;