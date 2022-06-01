# Commit format guidelines

The commit should be formatted as follows :

```
type(topic): a short description

Details if needed... This can span on multiple lines.
```

Look at the first line with caution :

- no uppercase at the topic's name, the type's name or at the beginning of the short description.
- no dot at the end of the sentence.
- everything else is capitalized as normal, and sentences end with a dot.

Topics can include :

| Topic name | Description             |
|------------|-------------------------|
| `auth`     | Authentication service. |
| `api`      | API service.            |
| `gs`       | (Mini-)Game server.     |
| `ci`       | CI/CD related changes.  |
| `book`     | Book update.            |
| `ui`       | User interface.         |
| `misc`     | Miscellaneous topic.    |

Types can include :

| Type name | Description            |
|-----------|------------------------|
| `feat`    | Added a feature.        |
| `docs`    | Added documentation.    |
| `refactor`| Added documentation.    |
| `fix`     | Fixed a bug.            |
| `build`   | Update to build files.  |
| `test`    | Added or updated tests. |
| `misc`    | Miscellaneous changes.  |

Topics and types may evolve as new modules are added.

Also, commits should be at the present tense, and don't put the "s" at the end
of verbs (put `add`, not `adds`);

Imagine you are describing what the commit does. For example, instead of writing
`docs(misc): added commit format`, write `docs(misc): add commit format`. So
when you read it, you know this commit will add documentation about commit
format.
