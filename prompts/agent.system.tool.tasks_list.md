## tasks_list

List Google Tasks task lists or tasks within a specific list. View all task lists to find their IDs, or retrieve tasks with optional filtering for completed items.

**Arguments:**
- **action** (string, required): The list operation to perform. One of `lists` or `tasks`.
  - `lists` — List all task lists.
  - `tasks` — List tasks within a specific task list.
- **task_list_id** (string, optional): The ID of the task list to retrieve tasks from. Required when `action` is `tasks`. Use `@default` for the default task list.
- **show_completed** (boolean, optional): Whether to include completed tasks. Defaults to `false`.
- **limit** (integer, optional): Maximum number of results to return. Defaults to 25.

**Examples:**

List all task lists:
~~~json
{
  "action": "lists"
}
~~~

List tasks in the default task list:
~~~json
{
  "action": "tasks",
  "task_list_id": "@default",
  "limit": 50
}
~~~

List tasks including completed ones:
~~~json
{
  "action": "tasks",
  "task_list_id": "MDExNTIwNzY5OA",
  "show_completed": true
}
~~~
