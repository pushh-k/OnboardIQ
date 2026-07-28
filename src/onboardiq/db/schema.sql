CREATE TABLE IF NOT EXISTS repositories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS contributors (
    id SERIAL PRIMARY KEY,
    login VARCHAR(255) NOT NULL UNIQUE,
    type VARCHAR(50),
    created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS pull_requests (
    id SERIAL PRIMARY KEY,
    repository_id INTEGER REFERENCES repositories(id),
    contributor_id INTEGER REFERENCES contributors(id),
    number INTEGER NOT NULL,
    title VARCHAR(500),
    state VARCHAR(50),
    created_at TIMESTAMP,
    merged_at TIMESTAMP,
    review_count INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS reviews (
    id SERIAL PRIMARY KEY,
    pull_request_id INTEGER REFERENCES pull_requests(id),
    reviewer_login VARCHAR(255),
    state VARCHAR(50),
    submitted_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS review_comments (
    id SERIAL PRIMARY KEY,
    review_id INTEGER REFERENCES reviews(id),
    body TEXT,
    created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS issues (
    id SERIAL PRIMARY KEY,
    repository_id INTEGER REFERENCES repositories(id),
    number INTEGER NOT NULL,
    title VARCHAR(500),
    state VARCHAR(50),
    created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS analytics (
    id SERIAL PRIMARY KEY,
    repository_id INTEGER REFERENCES repositories(id),
    metric_name VARCHAR(255) NOT NULL,
    metric_value DOUBLE PRECISION,
    computed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_pull_requests_repository_id ON pull_requests(repository_id);
CREATE INDEX IF NOT EXISTS idx_pull_requests_contributor_id ON pull_requests(contributor_id);
CREATE INDEX IF NOT EXISTS idx_reviews_pull_request_id ON reviews(pull_request_id);
