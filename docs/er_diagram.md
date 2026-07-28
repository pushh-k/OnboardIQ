# ER Diagram

```mermaid
eerDiagram
    REPOSITORIES ||--o{ PULL_REQUESTS : contains
    CONTRIBUTORS ||--o{ PULL_REQUESTS : authors
    PULL_REQUESTS ||--o{ REVIEWS : has
    REVIEWS ||--o{ REVIEW_COMMENTS : contains
    REPOSITORIES ||--o{ ISSUES : owns
```
