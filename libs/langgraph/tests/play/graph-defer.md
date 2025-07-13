## defer error 1

```mermaid


    graph TD
    a --> b
    a --> c
    a --> d
    b --> d
    c --> d

    style c fill:lightyellow
    style d fill:lightyellow

```

## defer error 2

```mermaid
graph TD
a --> b
a --> c
a --> d
a --> e

b --> f
c --> f

d --> g
e --> g

f --> h
d --> h
g --> h

style f fill:lightyellow
style g fill:lightyellow
style h fill:lightyellow
```