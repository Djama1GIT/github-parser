CREATE TABLE IF NOT EXISTS Repositories (
    id SERIAL PRIMARY KEY,
    repo VARCHAR(255) NOT NULL UNIQUE,
    owner VARCHAR(255) NOT NULL,
    position_cur INTEGER NOT NULL,
    position_prev INTEGER NOT NULL,
    stars INTEGER NOT NULL,
    watchers INTEGER NOT NULL,
    forks INTEGER NOT NULL,
    open_issues INTEGER NOT NULL,
    language VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS RepoActivity (
    id SERIAL PRIMARY KEY,
    repo_id INTEGER REFERENCES Repositories(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    commits INTEGER NOT NULL,
    authors JSONB,
    UNIQUE (repo_id, date)
);
