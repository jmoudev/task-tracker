A simple command line interface to track tasks.

The list of commands and their usage is given below:

### Adding tasks
```
task-cli add "Buy groceries"

# Output:
{
    "createdAt": 2024-01-01T00:00:00
    "description": "Buy groceries",
    "id": 1,
    "status": "todo",
    "updatedAt": 2024-01-01T00:00:00
}
```

#### Updating tasks
```
# by description
task-cli update 1 "Buy groceries and cook dinner"

# Output:
{
    "createdAt": 2023-01-01T00:00:00
    "description": "Buy groceries and cook dinner",
    "id": 1,
    "status": "todo",
    "updatedAt": 2024-02-01T01:01:01
}

# by status 'in-progress'
task-cli mark-in-progress 1

# Output (subset):
{   
    ...
    "id": 1,
    "status": "in-progress",
    ...
}


# by status 'done'
task-cli mark-done 1

# Output (subset):
{
    ...
    "id": 1,
    "status": "done",
    ...
}
```

### Deleting tasks
```
task-cli delete 1

# Output: Task deleted successfully (ID: 1)
```

### Listing tasks
```
# List all

task-cli list

# Output (subset):
[
    {
        ...
        "id": 1,
        "status": "todo"
        ...
    },
    {
        ...
        "id": 2,
        "status": "in-progress"
        ...
    }
]

# List by status 'in-progress'

task-cli list in-progress

# Output (subset):
[
    {
        ...
        "id": 2
        "status": "in-progress"
        ...
    }
]
```
