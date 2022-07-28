# Database layout

Here is a preview of the database layout for the database.

## `users`

A table where the users are stored.

| Name            | Type     | Unique | Not null | Description                      | Relation |
|-----------------|----------|--------|----------|----------------------------------|----------|
| `id`            | `number` | yes    | yes      | The ID of the user.              |          |
| `name`          | `string` | yes    | yes      | The unique name of the user.     |          |
| `email`         | `string` | yes    | yes      | The unique email of the user.    |          |
| `password_hash` | `string` | no     | yes      | The hash of the user's password. |          |

## `user_blacklist`

A table where the blacklisted tokens are stored.

Entries must be removed after the expiration date has been reached.

| Name         | Type     | Unique | Not null | Description                                         | Relation        |
|--------------|----------|--------|----------|-----------------------------------------------------|-----------------|
| `token`      | `string` | yes    | yes      | The token to blacklist.                             |                 |
| `type`       | `enum`   | no     | yes      | The type of token (`refresh` or `jwt`).             |                 |
| `expiration` | `date`   | no     | yes      | The date when the token expires.                    |                 |


## `projects`

A table storing projects (mini-games).

| Name      | Type     | Unique | Not null | Description                            | Relation        |
|-----------|----------|--------|----------|----------------------------------------|-----------------|
| `id`      | `number` | yes    | yes      | The ID of the project.                 |                 |
| `name`    | `string` | no     | yes      | The name of the project.               |                 |
| `api_key` | `string` | yes    | yes      | A key to authenticate the project.     |                 |
| `user_id` | `number` | no     | yes      | The ID of the user owning the project. | `users` on `id` |

## `temp_users`

A table where the just created accounts are stored until their email is
verified. On email verification, users must get transferred from this table to
the `users` table.

```admonish note
When an email is updated, there is no temporary account created. When an email
is changed, the user gets an email with a token that contains an encoded
message that is signed by this server. To update the email, the user clicks on
a link which sends a request to this server and updates the email directly in
the `users` table.
```

| Name            | Type     | Unique | Not null | Description                      | Relation |
|-----------------|----------|--------|----------|----------------------------------|----------|
| `id`            | `number` | yes    | yes      | The ID of the user.              |          |
| `name`          | `string` | yes    | yes      | The unique name of the user.     |          |
| `email`         | `string` | yes    | yes      | The unique email of the user.    |          |
| `password_hash` | `string` | no     | yes      | The hash of the user's password. |          |
