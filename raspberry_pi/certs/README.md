# TLS Certificates

Place your TLS certificates here:

- ca.crt        # CA certificate (public, can be checked in if you want)
- server.crt    # Server certificate (public, can be checked in if you want)
- ca.key        # CA private key (do NOT commit)
- server.key    # Server private key (do NOT commit)

Optional / temporary files (do NOT commit):

- ca.srl        # OpenSSL metadata
- server.csr    # Certificate signing request

You can generate all certificates locally with:

```bash
./generate_certs.sh
```
Important: Private keys must never be committed to GitHub!
