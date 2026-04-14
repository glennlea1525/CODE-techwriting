```mermaid
flowchart LR
subgraph Department A
A[Step 1]
end
subgraph Department B
B[Step 2]
end
subgraph Department C
subgraph Sub-Dept C1
C[Step 3]
end
subgraph Sub-Dept C2
D[Step 4]
end
end
A --> B --> C
D --> B
```
