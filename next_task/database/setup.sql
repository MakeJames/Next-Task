-- Setup script for Next Task database

CREATE TABLE task_database_version(db_version REAL);

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
    updated DATETIME NOT NULL DEFAULT (DATETIME(current_timestamp)),
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
        WITH _current_status as (
    	    SELECT
    	    	project_id,
    	    	p_status,
    	    	MAX(updated)
    	    FROM
    	    	project_status
    	    GROUP BY
    	    	project_id
    	    )
    	SELECT
            project_id
		FROM
            _current_status
		WHERE
            p_status = 'active'
    ) != NEW.project_id
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

-- Create Views
CREATE VIEW task_list AS
	WITH _current_proect AS (
		SELECT
			project_id,
			p_status,
			MAX(updated)
		FROM
			project_status
		GROUP BY
			project_id
	), _current_status AS (
		SELECT
			task_id,
			t_status,
			MAX(updated)
		FROM
			task_status
		GROUP BY
			task_id
	)
SELECT
	t.id as task_id,
	t.summary,
	COUNT(st.task_id) as skip_count,
	(t.id + t.t_priority * COUNT(st.task_id)) as _rank
FROM
	task AS t
LEFT JOIN task_skips AS st ON
	t.id = st.task_id
LEFT JOIN _current_status AS cs ON
	t.id = cs.task_id
LEFT JOIN project_tasks AS pt ON
	t.id = pt.task_id
WHERE
	cs.t_status != 'closed'
	AND pt.project_id IS (
	SELECT
		project_id
	FROM
		_current_proect
	WHERE
		p_status = 'active')
GROUP BY
	t.id
ORDER BY
	_rank ASC;
