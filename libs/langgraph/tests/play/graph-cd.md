## conditional edge error 1

```mermaid
graph TD
a --> b
a --> c
a --> d
a --> e

b -.true.-> f
c -.true.-> f

d -.true.-> g
e -.true.-> g

f --> h
d -.true.-> h
g --> h

```