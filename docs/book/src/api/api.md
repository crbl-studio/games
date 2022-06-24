# Introduction

Since this and the authentication service are very similar, so is the
documentation. Please read the [introduction of the authentication
service](../auth/api.md#introduction) to better understand how this
documentation is laid out.

# Routes

## POST to `/account`

Updates personal information.

### Input

#### Headers

- `Authorization: Bearer <token>`

#### Data

```admonish info
Only not `undefined` values are updated, the rest stays the same.
```

```typescript
interface Body {
    /* This represents [this](../database.md#user_data). */
    mature: boolean | undefined;
}
```

### Output

#### Error codes

```admonish warning
TBD stands for "to be determined" and means we need to determine a minimum age for which not to display mature content.
```

- `1` : mature is set to true and the age of the client is lower than TBD or undefined.

#### HTTP codes

- `400` : if the input is malformed (missing fields, unknown fields, etc.).
- `401` : if no authorization token was provided or if the authorization token is invalid.

## POST to `/friend/{name}`

Send a friend request.

### Input

#### Headers

- `Authorization: Bearer <token>`

#### Data

```typescript
interface Url {
    name: string; /* The name of the friend to add. */
}
```

### Output

#### Error codes

- `1` : the name does not belong to any user.

#### HTTP codes

- `400` : if the input is malformed (missing fields, unknown fields, etc.).
- `401` : if no authorization token was provided or if the authorization token is invalid.

## PUT to `/friend`

Accept a friend request.

When a user sends a friend request, the API server generates a token, which
contains the ID's of both users. It then encrypts it with it's private key. Upon
acceptance of the request, the server decrypts the token, and if the users match
the ones in the token, they become friends. Some might say that `name` in
the accept request is not needed, but in fact, it is. Let me explain by giving
you an example. Let's say I'm Alex, and I want to be friends with Bogdan, but
Bogdan doesn't want to because I am unbearable, but Bogdan would be ok with
being friends with Claire. Alex asks Claire to send Bogdan a friend request with
his own token, so that when Bogdan accepts, Alex and Bogdan become friends. By
sending the name along, we ensure that this trick did not happened.

We also send an expiration date in order to avoid very old friend requests (+1
months) to be accepted.

```admonish info
The public key is available to anyone. This way, the token can also be read by
the browser.
```

### Input

#### Headers

- `Authorization: Bearer <token>`

#### Data

```typescript
interface Body {
    friendRequestToken: string;
    expirationDate: number;
}

interface Url {
    name: string;
}
```

### Output

#### Error codes

- `1` : the users in the token does not match the users in the request.
- `2` : expiration date has been reached.

#### HTTP codes

- `400` : if the input is malformed (missing fields, unknown fields, etc.).
- `401` : if no authorization token was provided or if the authorization token is invalid.

## `DELETE` to `/friend/{name}`

Removes a friend from the friend list.

### Input

#### Headers

- `Authorization: Bearer <token>`

#### Data

```typescript
interface Url {
    name: string;
}
```

### Output

#### Error codes

- `1` : no user with this name was found.

#### HTTP codes

- `400` : if the input is malformed (missing fields, unknown fields, etc.).
- `401` : if no authorization token was provided or if the authorization token is invalid.

## `POST` to `/user/block/{name}`

Block another user.

### Input

#### Headers

- `Authorization: Bearer <token>`

#### Data

```typescript
interface Url {
    name: string;
}
```

### Output

#### Error codes

- `1` : no user with this name was found.
- `2` : user already blocked.

#### HTTP codes

- `400` : if the input is malformed (missing fields, unknown fields, etc.).
- `401` : if no authorization token was provided or if the authorization token is invalid.

## `DELETE` to `/user/block/{name}`

Unblock a blocked user.

### Input

#### Headers

- `Authorization: Bearer <token>`

#### Data

```typescript
interface Url {
    name: string;
}
```

### Output

#### Error codes

- `1` : no user with this name was found.
- `1` : user not blocked.

#### HTTP codes

- `400` : if the input is malformed (missing fields, unknown fields, etc.).
- `401` : if no authorization token was provided or if the authorization token is invalid.

## `GET` to `/user/{name}`

Get the profile of a user.

```admonish warning "Privacy"
Do not allow people to get the profile if :

- the requested user has blocked the requesting user.
- the requested user has a private profile.
```

### Input

#### Headers

- `Authorization: Bearer <token>`

#### Data

```typescript
interface Url {
    name: string;
}
```

### Output

#### Data

```admonish warning "Subject to change"
This data is subject to a lot of changes, as there may be more data that needs to be added.
```

```typescript
interface Output {
    name: string;      /* The user's name. */
    friends: string[]; /* The user's friends names, only if his friend list 
                        * is public or friends only and the requesting user
                        * is friends with the requested user. */
}
```

#### Error codes

- `1` : no user with this name was found or the requested user blocked the requesting user.

#### HTTP codes

- `400` : if the input is malformed (missing fields, unknown fields, etc.).
- `401` : if no authorization token was provided or if the authorization token is invalid.

## `GET` to `/user/find/{name}`

Search for users by name.

```admonish info
Just like before, do not display users who blocked the requesting user.
```

### Input

#### Headers

- `Authorization: Bearer <token>`

#### Data

```typescript
interface Url {
    name: string;
}
```

## `GET` to `/key`

Get the public key that is used throughout the API.

### Output

#### Data

```typescript
interface Output {
    key: string;
}
```
