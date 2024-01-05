# About
This is a simple Diffie-Hellman symmetric key exchange algorithm implementation using a client-server protocol through sockets in Python.

## Technical Considerations
This implementation is NOT remotely production-ready. It is solely an exploration of the concepts of Diffie-Hellman through a hands-on project.
The chosen generator g (3) was selected at random and did **not** consider any security limitations or advantages of other values. 
Additionally, the implementation explores DH in its most basic form, not a robust, modern version that handles various security threats like MITM.

That said, this project still offers valuable insight into how sockets in Python work and the mathematical proofs underlying DH. 
