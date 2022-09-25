CREATE TABLE IF NOT EXISTS task_database_version(
    version FLOAT
);

INSERT INTO task_database_version(version) VALUES (0.1);

CREATE TABLE IF NOT EXISTS task_status(
    id INTEGER PRIMARY KEY,
    name VARCHAR(20)
);

INSERT INTO task_status VALUES 
    (1, 'open'),
    (2, 'active'),
    (3, 'closed')
; 

CREATE TABLE IF NOT EXISTS project(
    id INTEGER PRIMARY KEY,
    summary VARCHAR(120) NOT NULL UNIQUE,
    description TEXT,
    status_id TINYINT NOT NULL DEFAULT 1,
    due DATE NOT NULL DEFAULT (DATE(current_timestamp, '56 days')),
    FOREIGN KEY(status_id) REFERENCES task_status(id)
);

INSERT INTO project(summary, status_id, due) VALUES ('', 2, DATE(current_timestamp, '1000 years'));

CREATE TABLE IF NOT EXISTS task(
    id INTEGER PRIMARY KEY,
    summary VARCHAR(120),
    description TEXT,
    status_id TINYINT NOT NULL DEFAULT 1,
    due DATETIME NOT NULL DEFAULT (DATETIME(current_timestamp, '14 days')),
    skip_count INTEGER DEFAULT 0,
    project_id INTEGER DEFAULT 1,
    FOREIGN KEY(project_id) REFERENCES project(id)
    FOREIGN KEY(status_id) REFERENCES task_status(id)
);

CREATE TABLE IF NOT EXISTS completed_task(
    task_id INTEGER UNIQUE,
    completed_date DATETIME DEFAULT (DATETIME(current_timestamp)) NOT NULL,
    FOREIGN KEY (task_id) REFERENCES task(id)
);

CREATE TABLE IF NOT EXISTS completed_project(
    project_id INTEGER UNIQUE,
    completed_date DATETIME DEFAULT (DATETIME(current_timestamp)),
    FOREIGN KEY (project_id) REFERENCES project(id)
);