"""Module containing methods and classes for parsing projects."""

import sys
from pypika import Query, Table

from next_task.interface.console_output import Style, TaskTable

from .database import Database

console = Style().console()


class Lookup:
    """Find a project on in the database."""

    def __init__(self, look_up_value):
        """Instansiate the class."""
        self.look_up = self._parse_lookup(look_up_value)
        self.query = self._query_builder()
        self.result = self._search()

    def _parse_lookup(self, look_up):
        try:
            return int(look_up)
        except ValueError:
            return str(look_up)
        except TypeError:
            return ""

    def _query_builder(self):
        project = Table("project")
        query = Query.from_(project).select("id", "summary")

        if isinstance(self.look_up, int):
            return query.where(project.id == self.look_up)

        if isinstance(self.look_up, str):
            return query.where(project.summary.like(f'%{self.look_up}%'))

    def _search(self):
        return Database().read(str(self.query))


class FindProject:
    """Find a project."""

    def __init__(self, look_up):
        """Instansiate the class."""
        self.id = None
        self.summary = None
        self._check_projects()
        self._find_project(look_up)

    def _check_projects(self):
        result = Database().read("SELECT COUNT(*) FROM project;")
        if result[0] == 0:
            console.print("[warning]No open Projects defined.[/warning]")
            sys.exit()

    def _find_project(self, look_up):
        result = Lookup(look_up).result
        while 0 < 1:
            if len(result) == 1:
                self._map_result(result)
                break
            if len(result) > 1:
                result = self._resolve_multiple(result)
                continue
            result = self._resolve_none()

    def _map_result(self, result):
        self.id = result[0]["id"]
        self.summary = result[0]["summary"]

    def _resolve_multiple(self, results):
        console.print("[warning]More than one project found[/warning]")
        TaskTable(results, title="Projects")
        new = console.input("[info]Pick a project id or '--exit': [/info]")
        self._check_exit(new)
        return Lookup(new).result

    def _resolve_none(self):
        console.print("[warning]No Project Found.[/warning]")
        query = "SELECT id, summary FROM project;"
        TaskTable(Database().read(query), title="Projects")
        new = console.input("[info]Search for a project id or summary. "
                            "Type --exit to exit: [/info]")
        self._check_exit(new)
        return Lookup(new).result

    def _check_exit(self, value):
        if value == "--exit":
            sys.exit()
        if value == "0":
            ClearActive()
            sys.exit()


class SetActive:
    """Set a project as active."""

    def __init__(self, project_lookup=""):
        """Instansiate the class."""
        self.project_id = FindProject(project_lookup).id
        Database().write(self._query_builder())
        CheckActiveProject().print()

    def _query_builder(self):
        project_status = Table("project_status")
        query = Query.into(project_status).columns("project_id", "p_status")
        query = query.insert(self.project_id, 'active')
        return str(query)


class CheckActiveProject:
    """Look up active project and return the project id."""

    def __init__(self):
        """Instansiate the class."""
        self.id = None
        self.summary = None
        self._check()

    def _check(self):
        query = """
            WITH _current_p_status AS (
                SELECT
                    ps.project_id AS id,
                    p.summary AS summary,
                    ps.p_status AS p_status,
                    MAX(ps.updated) AS updated
                FROM
                    project_status AS ps
                    LEFT JOIN project AS p
                        ON ps.project_id = p.id
                GROUP BY 1)
            SELECT
                id,
                summary
            FROM
                _current_p_status
            WHERE
                p_status = 'active';
        """
        result = Database().read(query)
        if result == []:
            return
        self.id = result[0]["id"]
        self.summary = result[0]["summary"]

    def print(self):
        """Return the active task to the console."""
        if self.id is None:
            return
        console.print(f"[info][b]Project {self.id}:[/b] {self.summary}"
                      "[/info] is [green]active[/green]", style="default")


class ClearActive:
    """Clear the active project."""

    def __init__(self):
        """Instansiate the class."""
        self.id = CheckActiveProject().id
        if self.id:
            Database().write(self._query())

    def _query(self):
        ps = Table("project_status")
        return str(Query.into(ps).columns(ps.project_id).insert(self.id))


class CreateProject:
    """Create a project."""

    def __init__(self, summary):
        """Instansiate the class."""
        self.summary = summary
        self.id = Database().write(self._query())
        self._print()

    def _query(self):
        p = Table("project")
        return str(Query.into(p).columns(p.summary).insert(self.summary))

    def _print(self):
        console.print(f"Created Project [info]{self.id}: {self.summary}")
