# Introduction

Foremost, each response is structured as follows :

```typescript
interface Dto<T> {
    data: T | null;
    error?: Error | null;
}

interface Error {
    code: number;
    message: string;
}
```

Either `data` or `error` must be null, and the other one must contain
something. In the rest of this page, we will only declare the interface that
represents `T`, and list error codes that can be returned by each route.

Errors are only returned if the data is well sent by the client. If data is
malformed, fields are missing, authorization is required, etc., then the HTTP
response code should be between 400 and 499 and the return body should be
empty.

Error codes are route dependent. This means that error code `1` on `POST` to
`/user` does not mean the same thing as error code `1` on `GET` to
`/server/login`.

For input data, the `Body` interface is considered to be a JSON body, and
the `Url` interface are the parameters passed in the URL. They should match
the braces in the title of the route. For example, if a route is `/user/{id}`,
then the `Url` object should contain one item, named `id`.

Error code `0` always means unknown error.

A JWT should contain the following information :

- an expiration date
- a unique identifier to the authenticated entity
- an entity type (`'User' | 'MiniGameServer'`)

# Routes

## `POST` to `/user`

Creates a new user.

### Input

#### Data

```typescript
interface Body {
    name: string; /* The user's display name, must be unique. */
    email: string; /* The user's email, must be unique. */
    password: string; /* The user's password. */
    mature: boolean; /* Whether to display mature content to the user or not */
}
```

### Output

#### Data

```typescript
interface Output {
    jwt: string;
    refreshToken: string;
}
```

#### Error codes

- `1` : name is already used.
- `2` : email is already used.
- `3` : password is considered insecure.

#### HTTP codes

- `400` : if the input is malformed (missing fields, unknown fields, etc.).

---

## `PUT` to `/user/name`

Edits a user's name.

No email change happens here. Email change is accomplished by [another
route](please put link here).

### Input

#### Data

```typescript
interface Body {
    name: string;
}
```

#### Headers

- `Authorization: Bearer <token>`

### Output

#### Data

```typescript
interface Output {
    name: string;
}
```

#### Error codes

- `1` : name is already used.

#### HTTP codes

- `400` : if the input is malformed (missing fields, unknown fields, etc.).
- `401` : if no authorization token was provided or if the authorization token is invalid.

---

## `PUT` to `/user/email`

Edits a user's email.

No name change happens here. Name change is accomplished by [another
route](please put link here).

This should not instantly change the user's email, but wait for the user to
verify his new email before changing it.

### Input

#### Data

```typescript
interface Body {
    email: string;
}
```

#### Headers

- `Authorization: Bearer <token>`

### Output

#### Data

```typescript
interface Output {
    email: string;
}
```

#### Error codes

- `1` : email is already used.

#### HTTP codes

- `400` : if the input is malformed (missing fields, unknown fields, etc.).
- `401` : if no authorization token was provided or if the authorization token is invalid.

---

## `POST` to `/user/login`

Logs in a user with his name or email, and password.

### Input

#### Data

```typescript
interface Body {
    email: string | null;
    name: string | null;
    password: string;
}
```

### Output

#### Data

```typescript
interface Output {
    jwt: string;
    refreshToken: string;
}
```

#### Error codes

- `1` : both email and name are null.
- `2` : both email and name are provided.
- `3` : no user found with this combination.

---

## `POST` to `/user/logout`

Logs out a user.

Should invalidate the tokens.

### Input

#### Headers

- `Authorization: Bearer <token>`
- `X-Refresh-Token: <token>`

### Output

None.

---

## `DELETE` to `/user`

Deletes a user.

### Input

#### Headers

- `Authorization: Bearer <token>`

### Output

None.

---

## `POST` to `/mini-game`

Creates a new mini-game project for the logged-in user.

### Input

#### Data

```typescript
interface Body {
    name: string;
}
```

#### Headers

- `Authorization: Bearer <token>`

### Output

#### Data

```typescript
interface Output {
    name: string;
    apiKey: string; /* Only delivered once as it is stored as a hash in the database, watch out ! */
    id: string; /* Unique mini-game identifier. */
}
```

#### Error codes

- `1` : the name is already used.
- `2` : the user has reached the maximum number of mini-games allowed per user.

#### HTTP codes

- `400` : if the input is malformed (missing fields, unknown fields, etc.).
- `401` : if no authorization token was provided or if the authorization token is invalid.

---

## `DELETE` to `/mini-game/{id}`

Deletes the specified mini-game.

### Input

#### Headers

- `Authorization: Bearer <token>`

### Output

#### HTTP codes

- `401` : if no authorization token was provided or if the authorization token is invalid.
- `404` : if no such mini-game was found or if the mini-game does not belong to the user.

---

## `POST` to `/mini-game/login`

Generates an authentication token for a mini-game.

### Input

#### Headers

- `X-Api-Key: <api-key>`

### Output

#### Data

```typescript
interface Output {
    jwt: string;
    refreshToken: string;
}
```

#### HTTP codes

- `401` : if no authorization token was provided or if the authorization token is invalid.

---

## `POST` to `/mini-game/logout`

Generates an authentication token for a mini-game.

### Input

#### Headers

- `Authorization: Bearer <token>`
- `X-Refresh-Token: <token>`

### Output

None.

---

## `POST` to `/decode`

Decodes information encoded into a JWT and verifies its authenticity.

```admonish warning "Authorization"
Only authorized services should be able to decode and verify a JWT.
```

```admonish note
This information can be cached, in order to not verify the JWT on each request.
For example, when the API server wants to know if the JWT is valid, it will
make a request to the authentication server, which will respond with the
necessary information, which is then cached by the API server. This way, the
API server won't have to make another request to the authentication server
whenever the entity makes another request with the same JWT.
```

```admonish note
Data could be decoded locally using a public key, but that implementation would
make it difficult to invalidate tokens. This is why the service wanting to
verify the token asks the authentication service if the token is valid or not.
```

### Input

#### Data

```typescript
interface Body {
    jwt: string;
}
```

#### Headers

- `Authorization: Bearer <token>`

### Output

#### Data

```typescript
interface Output {
    type: 'User' | 'MiniGameServer';
    exp: number; /* The date the JWT expires on. */
    id: string; /* Unique identifier to the entity. */
}
```

#### Error codes

- `1` : the server was not able to decode the JWT.
- `2` : the JWT is expired.

#### HTTP codes

- `400` : if the input is malformed (missing fields, unknown fields, etc.).
- `401` : if no authorization token was provided or if the authorization token is invalid.

---
