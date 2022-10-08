
-- Create Tasks
INSERT INTO
	task(summary)
VALUES
    ("A task");

INSERT INTO
	task(summary)
VALUES
    ("Make a cup of tea");

INSERT INTO
	task(summary)
VALUES
    ("Trash the econonmy");

INSERT INTO
	task(summary)
VALUES
    ("Read that article about postmodern politics");

INSERT INTO
	task(summary)
VALUES
    ("This is a new_task");

INSERT INTO
	task(summary)
VALUES
    ("Is this really another task");

INSERT INTO
	task(summary)
VALUES
    ("Make tea");

INSERT INTO
	task(summary)
VALUES
    ("Another task");

INSERT INTO
	task(summary, t_priority)
VALUES
    ("A task", 3);

INSERT INTO
	task(summary)
VALUES
    ("Make a cup of tea");

INSERT INTO
	task(summary)
VALUES
    ("Trash the econonmy");

INSERT INTO
	task(summary, t_priority)
VALUES
    ("Read that article about postmodern politics", 3);

INSERT INTO
	task(summary)
VALUES
    ("This is a new_task");

INSERT INTO
	task(summary)
VALUES
    ("Is this really another task");

INSERT INTO
	task(summary, t_priority)
VALUES
    ("Make tea", 10);

INSERT INTO
	task(summary)
VALUES
    ("Another task");

INSERT INTO
	task(summary)
VALUES
    ("Improve the speed of a parsec");

INSERT INTO
	task(summary)
VALUES
    ("Defeat the 2nd law of thermodynamics");

INSERT INTO
	task(summary)
VALUES
    ("Stare out of a window for several hours");

INSERT INTO
	task(summary)
VALUES
    ("State the obvious");

INSERT INTO
	task(summary)
VALUES
    ("42");

-- Create Projects

INSERT INTO
	project(summary)
VALUES
    ("Calculate the meaning of Life");

INSERT INTO
	project(summary)
VALUES
    ("Create a task Management Solution");


-- Update status_tables

UPDATE task_status
SET updated = "2022-01-01 09:32:11";

UPDATE project_status
SET updated = "2022-01-01 09:32:11";