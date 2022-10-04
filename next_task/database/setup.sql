-- Setup script for Next Task database

CREATE TABLE task_database_version(db_version REAL);

INSERT INTO task_database_version(db_version) VALUES (0.4);

-- Create Task Tables
CREATE TABLE task (
    id INTEGER PRIMARY KEY,
    summary TEXT NOT NULL,
    t_priority TINYINT DEFAULT 6
    );

CREATE TABLE task_status (
    task_id NOT NULL,
    t_status TEXT DEFAULT 'open',
    updated DATETIME NOT NULL DEFAULT (DATETIME(current_timestamp)),
    PRIMARY KEY (task_id, updated),
    FOREIGN KEY (task_id) REFERENCES task(id)
    );

CREATE TABLE task_skips (
    task_id NOT NULL,
    skipped DATETIME NOT NULL DEFAULT (DATETIME(current_timestamp)),
    PRIMARY KEY (task_id, skipped)
    );

-- project tables
CREATE TABLE project (
    id INTEGER PRIMARY KEY,
    summary TEXT NOT NULL
    );

CREATE TABLE project_status(
    project_id INT NOT NULL,
    p_status TEXT DEFAULT 'open',
    updated DATETIME NOT NULL DEFAULT (DATE(current_timestamp)),
    PRIMARY KEY (project_id, updated),
    FOREIGN KEY (project_id) REFERENCES project(id)
    );

CREATE TABLE project_tasks(
    project_id INT,
    task_id INT,
    PRIMARY KEY (project_id, task_id),
    FOREIGN KEY (project_id) REFERENCES project(id),
    FOREIGN KEY (task_id) REFERENCES task(id)
    );

-- Create Triggers
-- Inserts task into status table
CREATE TRIGGER _create_task
AFTER INSERT ON
    task
BEGIN
    INSERT INTO
        task_status(task_id)
    VALUES
        (NEW.id)
    ;
END;

-- Inserts project into status table
CREATE TRIGGER _create_project
AFTER INSERT ON
    project
BEGIN
    INSERT INTO
        project_status(project_id)
    VALUES (
        NEW.id
    );
END;

-- Link active project with new task
CREATE TRIGGER _associate_project_task
AFTER INSERT ON
    task
BEGIN
	INSERT INTO
        project_tasks(project_id, task_id)
    VALUES (
        (
            SELECT
                project_id
            FROM
                project_status
        	WHERE
                p_status = 'active'
            ORDER BY
                updated DESC
            LIMIT 1
        ),
        NEW.id
    );
END;

-- Ensure that there is only one active project
CREATE TRIGGER _resolve_concurrent_projects
BEFORE INSERT ON
    project_status
WHEN
    (
    	SELECT COUNT(project_id)
		FROM project_status
		WHERE p_status = 'active'
		ORDER BY updated DESC
    ) IS 1
    AND NEW.p_status = 'active'
BEGIN
    INSERT INTO
        project_status(project_id)
    SELECT
        project_id
    FROM (
        SELECT ps2.project_id
		FROM project_status AS ps2
		WHERE ps2.p_status = 'active'
		ORDER BY ps2.updated DESC
		LIMIT 1
    );
END;
