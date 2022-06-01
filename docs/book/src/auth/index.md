# Authentication service

The authentication service (or auth service) is a core component which handles
authentication in the entire project. It's a REST API which means there is an
[API subchapter](./auth/api.md) which documents all the API endpoints.

This API handles user authentication, first-party components authentication as
well as mini-game servers authentication. Each type of client will get a
different type of authentication proof, which will allow them to identify
themselves to other services. The other services **do not** need to call the
auth service to check if the proof is valid. On authentication, the client will
receive a public key which allows them to verify all authentication proof. This
implementation has its ups and downs. The main advantage is that the auth
service usage is reduced (because the proofs do not have to be checked every
time by a request to the auth service). The main disadvantage is that
invalidating a proof might be tricky, and some elegant solution is yet to be
determined.
