# Database layout

Here is a preview of the database layout for the database.

## `user_data`

A table where the users are stored.

```admonish info
This is an extendable table, which means that it is easy to add fields if
needed.
```

| Name       | Type      | Unique | Not null | Description                                   | Relation        |
|------------|-----------|--------|----------|-----------------------------------------------|-----------------|
| `user_id`  | `number`  | yes    | yes      | The ID of the user.                           | [`users`](../auth/database.md#users) on `id` |
| `mature`   | `boolean` | no     | yes      | Whether the user wants to see mature content. |                 |
| `birthday` | `date`    | no     | no       | The birthday of the user.                     |                 |

## `friends`

Stores friends relations.

```admonish info
You can deduce whether the friend request is accepted or not by checking if the
date is null or not.
```

```admonish warning
Entries in this table shall be unique. Meaning there should not be twice the
same relation (not even swapped).
```

| Name            | Type     | Unique | Not null | Description                                        | Relation                                     |
|-----------------|----------|--------|----------|----------------------------------------------------|----------------------------------------------|
| `user_a`        | `number` | no     | yes      | The ID of one user.                                | [`users`](../auth/database.md#users) on `id` |
| `user_b`        | `number` | no     | yes      | The ID of the other user.                          | [`users`](../auth/database.md#users) on `id` |
| `date_accepted` | `date`   | no     | no       | The date at which the friend request was accepted. |                                              |

## `history_user`

The game history of the user.

| Name      | Type     | Unique | Not null | Description         | Relation                                     |
|-----------|----------|--------|----------|---------------------|----------------------------------------------|
| `user`    | `number` | no     | yes      | The ID of the user. | [`users`](../auth/database.md#users) on `id` |
| `game_id` | `number` | no     | yes      | The ID of the game. | [`history_game`](#history_game) on `id`      |

## `history_game`

The game history.

| Name    | Type       | Unique | Not null | Description                                  | Relation |
|---------|------------|--------|----------|----------------------------------------------|----------|
| `id`    | `number`   | yes    | yes      | The ID of the game.                          |          |
| `start` | `datetime` | no     | yes      | The date and time at which the game started. |          |
| `end`   | `datetime` | no     | yes      | The date and time at which the game ended.   |          |
| `public`| `boolean`  | no     | yes      | Whether the game was a public one or not.    |          |

## `history_mini_game`

The mini-game history.

| Name      | Type       | Unique | Not null | Description                                       | Relation                                |
|-----------|------------|--------|----------|---------------------------------------------------|-----------------------------------------|
| `id`      | `number`   | yes    | yes      | The ID of the mini-game.                          |                                         |
| `game_id` | `number`   | no     | yes      | The ID of the game.                               | [`history_game`](#history_game) on `id` |
| `start`   | `datetime` | no     | yes      | The date and time at which the mini-game started. |                                         |
| `end`     | `datetime` | no     | yes      | The date and time at which the mini-game ended.   |                                         |
| `config`  | `json`     | no     | yes      | The configuration of the mini-game.               |                                         |

## `history_mini_game_ranking`

```admonish warning
The entries should be unique, meaning that there shall not be two columns with
the same `mini_game_id` and `user_id`.
```

The mini-game raking history.

| Name           | Type     | Unique | Not null | Description            | Relation                                     |
|----------------|----------|--------|----------|------------------------|----------------------------------------------|
| `mini_game_id` | `number` | no     | yes      | The ID of the game.    | [`history_game`](#history_game) on `id`      |
| `user_id`      | `number` | no     | yes      | The ID of the user.    | [`users`](../auth/database.md#users) on `id` |
| `score`        | `number` | no     | yes      | The score of the user. |                                              |

## `mini_games`

Stores mini-games data. This table is to `projects` what `user_data` is to `users`.

| Name          | Type      | Unique | Not null | Description                           | Relation                                           |
|---------------|-----------|--------|----------|---------------------------------------|----------------------------------------------------|
| `project_id`  | `number`  | yes    | yes      | The ID of the project.                | [`projects`](../auth/database.md#projects) on `id` |
| `summary`     | `text`    | no     | yes      | A short description of the project.   |                                                    |
| `description` | `text`    | no     | yes      | A long description of the project.    |                                                    |
| `public`      | `boolean` | no     | yes      | Whether the project is public or not. |                                                    |

