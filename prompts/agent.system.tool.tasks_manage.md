## tasks_manage

Manage Google Tasks. Create new tasks, mark tasks as complete, delete tasks, or update existing task details.

**Arguments:**
- **action** (string, required): The management action to perform. One of `create`, `complete`, `delete`, or `update`.
  - `create` — Create a new task.
  - `complete` — Mark a task as completed.
  - `delete` — Delete a task.
  - `update` — Update an existing task's details.
- **title** (string, optional): Task title. Required when `action` is `create`. Used with `update` to change the title.
- **notes** (string, optional): Task notes or description. Used with `create` or `update`.
- **due** (string, optional): Task due date. Format: `YYYY-MM-DD`. Used with `create` or `update`.
- **task_id** (string, optional): The ID of the task to act on. Required when `action` is `complete`, `delete`, or `update`.
- **task_list_id** (string, optional): The task list containing the task. Defaults to `@default`.
- **status** (string, optional): Task status. One of `needsAction` or `completed`. Used with `update`.

**Examples:**

Create a new task with a due date:
~~~json
{
  "action": "create",
  "title": "Review pull request #42",
  "notes": "Check for security issues and test coverage",
  "due": "2026-03-15",
  "task_list_id": "@default"
}
~~~

Mark a task as completed:
~~~json
{
  "action": "complete",
  "task_id": "dGFzazEyMzQ1Njc4",
  "task_list_id": "@default"
}
~~~

Update a task's title and due date:
~~~json
{
  "action": "update",
  "task_id": "dGFzazEyMzQ1Njc4",
  "title": "Review pull request #42 - URGENT",
  "due": "2026-03-14"
}
~~~

Delete a task:
~~~json
{
  "action": "delete",
  "task_id": "dGFzazEyMzQ1Njc4",
  "task_list_id": "@default"
}
~~~
