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
| `api`      | API service.            |
| `auth`     | Authentication service. |
| `book`     | Book update.            |
| `gs`       | (Mini-)Game server.     |
| `misc`     | Miscellaneous topic.    |
| `ui`       | User interface.         |

Types can include :

| Type name  | Description             |
|------------|-------------------------|
| `build`    | Update to build files.  |
| `ci`       | CI/CD related changes.  |
| `docs`     | Added documentation.    |
| `feat`     | Added a feature.        |
| `fix`      | Fixed a bug.            |
| `misc`     | Miscellaneous changes.  |
| `refactor` | Added documentation.    |
| `test`     | Added or updated tests. |

Topics and types may evolve as new modules are added.

Also, commits should be at the present tense, and don't put the "s" at the end
of verbs (put `add`, not `adds`);

Imagine you are describing what the commit does. For example, instead of writing
`docs(misc): added commit format`, write `docs(misc): add commit format`. So
when you read it, you know this commit will add documentation about commit
format.
