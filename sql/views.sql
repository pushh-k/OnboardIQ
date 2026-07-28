CREATE VIEW IF NOT EXISTS contributor_summary AS
SELECT
    c.login,
    COUNT(pr.id) AS pull_request_count,
    AVG(COALESCE(pr.review_count, 0)) AS avg_review_count
FROM contributors c
LEFT JOIN pull_requests pr ON pr.contributor_id = c.id
GROUP BY c.login;
