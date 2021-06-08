#!/bin/bash
curl -XPOST http://127.0.0.1:8080/secrets/aaa
curl -XGET http://127.0.0.1:8080/secrets/aaa
curl -XPOST http://127.0.0.1:8080/secrets/aaa
curl -XGET http://127.0.0.1:8080/secrets/aaa
curl -XGET http://127.0.0.1:8080/secrets/aaa
curl -XDELETE http://127.0.0.1:8080/secrets/aaa
curl -XDELETE http://127.0.0.1:8080/secrets/aaa
curl -XGET http://127.0.0.1:8080/secrets/aaa