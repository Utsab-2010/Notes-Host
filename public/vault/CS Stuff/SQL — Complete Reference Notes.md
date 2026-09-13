---
title: "SQL — Complete Reference Notes"
lastmod: 2026-08-12
---



A practical, from-scratch-to-advanced reference. Covers table creation, data types, constraints, the clause execution order, joins, subqueries, aggregation, window functions, indexes, and transactions.

---

## 1. SQL Command Categories

|Category|Full Form|Commands|Purpose|
|---|---|---|---|
|DDL|Data Definition Language|`CREATE`, `ALTER`, `DROP`, `TRUNCATE`|Defines schema/structure|
|DML|Data Manipulation Language|`INSERT`, `UPDATE`, `DELETE`|Modifies data|
|DQL|Data Query Language|`SELECT`|Reads data|
|DCL|Data Control Language|`GRANT`, `REVOKE`|Permissions|
|TCL|Transaction Control Language|`COMMIT`, `ROLLBACK`, `SAVEPOINT`|Transaction management|

---

## 2. Creating Tables

```sql
CREATE TABLE employees (
    emp_id      INT PRIMARY KEY AUTO_INCREMENT,   -- SERIAL in Postgres
    first_name  VARCHAR(50) NOT NULL,
    last_name   VARCHAR(50) NOT NULL,
    email       VARCHAR(100) UNIQUE,
    salary      DECIMAL(10,2) CHECK (salary >= 0),
    dept_id     INT,
    hire_date   DATE DEFAULT CURRENT_DATE,
    manager_id  INT,
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id),
    FOREIGN KEY (manager_id) REFERENCES employees(emp_id)
);
```

### Common Data Types

|Type|Use|
|---|---|
|`INT` / `BIGINT`|Whole numbers|
|`DECIMAL(p,s)` / `NUMERIC(p,s)`|Exact fixed-point (money)|
|`FLOAT` / `DOUBLE`|Approximate floating point|
|`VARCHAR(n)`|Variable-length string|
|`CHAR(n)`|Fixed-length string|
|`TEXT`|Long-form string|
|`DATE`, `TIME`, `DATETIME`/`TIMESTAMP`|Temporal data|
|`BOOLEAN`|True/false|
|`JSON`/`JSONB`|Semi-structured data (Postgres, MySQL)|
|`UUID`|Unique identifiers (Postgres)|

### Constraints

|Constraint|Meaning|
|---|---|
|`PRIMARY KEY`|Unique + not null identifier|
|`FOREIGN KEY`|Links to another table's key|
|`UNIQUE`|No duplicate values|
|`NOT NULL`|Value required|
|`CHECK`|Custom validation rule|
|`DEFAULT`|Fallback value|

### Altering Tables

```sql
ALTER TABLE employees ADD COLUMN phone VARCHAR(15);
ALTER TABLE employees DROP COLUMN phone;
ALTER TABLE employees MODIFY COLUMN salary DECIMAL(12,2);  -- MySQL
ALTER TABLE employees ALTER COLUMN salary TYPE DECIMAL(12,2); -- Postgres
ALTER TABLE employees RENAME COLUMN first_name TO fname;
```

### Dropping / Clearing

```sql
DROP TABLE employees;        -- deletes table + data + structure
TRUNCATE TABLE employees;    -- deletes all rows, keeps structure, resets identity, faster (no per-row logging)
DELETE FROM employees;       -- deletes rows, can use WHERE, logged, triggers fire
```

---

## 3. Inserting, Updating, Deleting Data

```sql
INSERT INTO employees (first_name, last_name, salary, dept_id)
VALUES ('Utsab', 'Roy', 95000.00, 3);

INSERT INTO employees (first_name, last_name, salary, dept_id)
VALUES ('A', 'B', 50000, 1), ('C', 'D', 60000, 2);  -- multi-row insert

UPDATE employees
SET salary = salary * 1.10
WHERE dept_id = 3;

DELETE FROM employees
WHERE hire_date < '2015-01-01';
```

---

## 4. The Golden Rule: Written Order vs Execution Order

This is one of the most important things to internalize in SQL. The order you **write** a query is not the order the engine **executes** it.

### Written (syntax) order

```
SELECT ... 
FROM ... 
JOIN ... 
WHERE ... 
GROUP BY ... 
HAVING ... 
ORDER BY ... 
LIMIT ...
```

### Logical execution order

```
1. FROM        -- identify source tables
2. JOIN        -- combine tables
3. WHERE       -- filter individual rows
4. GROUP BY    -- group rows
5. HAVING      -- filter groups
6. SELECT      -- pick/compute columns (aliases created here)
7. DISTINCT    -- remove duplicate rows
8. ORDER BY    -- sort result
9. LIMIT/OFFSET -- restrict row count
```

**Why this matters:**

- You **can't** use a `SELECT` alias in `WHERE` (WHERE runs before SELECT), but you **can** use it in `ORDER BY` (runs after SELECT).
- `WHERE` filters rows _before_ grouping; `HAVING` filters groups _after_ aggregation — so `WHERE` can't reference aggregate functions like `COUNT()`, but `HAVING` can.

```sql
-- Invalid: alias not yet defined when WHERE runs
SELECT salary * 1.1 AS adjusted_salary
FROM employees
WHERE adjusted_salary > 50000;   -- ERROR in most engines

-- Valid: ORDER BY runs after SELECT, alias exists
SELECT salary * 1.1 AS adjusted_salary
FROM employees
ORDER BY adjusted_salary;

-- WHERE vs HAVING
SELECT dept_id, COUNT(*) AS cnt
FROM employees
WHERE salary > 30000        -- filters rows first
GROUP BY dept_id
HAVING COUNT(*) > 5;        -- filters groups after aggregation
```

---

## 5. Filtering & Sorting

```sql
SELECT * FROM employees
WHERE dept_id = 3 AND salary > 50000;

SELECT * FROM employees
WHERE dept_id IN (1, 2, 3);

SELECT * FROM employees
WHERE hire_date BETWEEN '2020-01-01' AND '2023-12-31';

SELECT * FROM employees
WHERE email LIKE '%@iitkgp.ac.in';   -- % = any sequence, _ = single char

SELECT * FROM employees
WHERE manager_id IS NULL;             -- never use `= NULL`

SELECT * FROM employees
ORDER BY salary DESC, last_name ASC;  -- multi-column sort, DESC/ASC per column

SELECT * FROM employees
LIMIT 10 OFFSET 20;                   -- pagination (Postgres/MySQL)
-- SQL Server equivalent: OFFSET 20 ROWS FETCH NEXT 10 ROWS ONLY
```

---

## 6. Joins

Joins combine rows from two or more tables based on a related column.

Setup for examples:

```sql
-- employees: emp_id, name, dept_id
-- departments: dept_id, dept_name
```

|Join|Returns|
|---|---|
|`INNER JOIN`|Only matching rows in both tables|
|`LEFT JOIN`|All rows from left + matches from right (NULL if no match)|
|`RIGHT JOIN`|All rows from right + matches from left (NULL if no match)|
|`FULL OUTER JOIN`|All rows from both, matched where possible|
|`CROSS JOIN`|Cartesian product (every row × every row)|
|`SELF JOIN`|Table joined with itself|

```sql
-- INNER JOIN: only employees that have a valid department
SELECT e.name, d.dept_name
FROM employees e
INNER JOIN departments d ON e.dept_id = d.dept_id;

-- LEFT JOIN: all employees, even if department is missing/null
SELECT e.name, d.dept_name
FROM employees e
LEFT JOIN departments d ON e.dept_id = d.dept_id;

-- RIGHT JOIN: all departments, even if no employees assigned
SELECT e.name, d.dept_name
FROM employees e
RIGHT JOIN departments d ON e.dept_id = d.dept_id;

-- FULL OUTER JOIN: everything from both sides
SELECT e.name, d.dept_name
FROM employees e
FULL OUTER JOIN departments d ON e.dept_id = d.dept_id;
-- MySQL has no FULL OUTER JOIN natively; emulate with:
-- LEFT JOIN UNION RIGHT JOIN

-- CROSS JOIN: every employee paired with every department
SELECT e.name, d.dept_name
FROM employees e
CROSS JOIN departments d;

-- SELF JOIN: employees and their managers
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.emp_id;
```

**Quick visual intuition:**

```
INNER JOIN   →  A ∩ B
LEFT JOIN    →  A ∪ (A ∩ B), keep all A
RIGHT JOIN   →  B ∪ (A ∩ B), keep all B
FULL JOIN    →  A ∪ B
```

---

## 7. Subqueries

```sql
-- Scalar subquery
SELECT name FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);

-- Subquery with IN
SELECT name FROM employees
WHERE dept_id IN (SELECT dept_id FROM departments WHERE dept_name = 'Engineering');

-- Correlated subquery (runs once per outer row)
SELECT e1.name, e1.salary
FROM employees e1
WHERE salary > (
    SELECT AVG(e2.salary) FROM employees e2 WHERE e2.dept_id = e1.dept_id
);

-- EXISTS (often faster than IN for existence checks)
SELECT d.dept_name
FROM departments d
WHERE EXISTS (SELECT 1 FROM employees e WHERE e.dept_id = d.dept_id);

-- Subquery in FROM (derived table)
SELECT dept_id, avg_sal
FROM (
    SELECT dept_id, AVG(salary) AS avg_sal
    FROM employees
    GROUP BY dept_id
) AS dept_avg
WHERE avg_sal > 60000;
```

---

## 8. Aggregate Functions & GROUP BY

```sql
SELECT COUNT(*), SUM(salary), AVG(salary), MIN(salary), MAX(salary)
FROM employees;

SELECT dept_id, COUNT(*) AS headcount, AVG(salary) AS avg_sal
FROM employees
GROUP BY dept_id
HAVING COUNT(*) > 3
ORDER BY avg_sal DESC;
```

**Rule:** every non-aggregated column in `SELECT` must appear in `GROUP BY`.

---

## 9. Window Functions

Unlike `GROUP BY`, window functions compute a value **per row** while still having access to a set ("window") of related rows — rows are not collapsed.

```sql
SELECT
    name, dept_id, salary,
    RANK()        OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rnk,
    DENSE_RANK()  OVER (PARTITION BY dept_id ORDER BY salary DESC) AS dense_rnk,
    ROW_NUMBER()  OVER (PARTITION BY dept_id ORDER BY salary DESC) AS row_num,
    AVG(salary)   OVER (PARTITION BY dept_id) AS dept_avg_sal,
    LAG(salary)   OVER (PARTITION BY dept_id ORDER BY salary) AS prev_salary,
    LEAD(salary)  OVER (PARTITION BY dept_id ORDER BY salary) AS next_salary,
    SUM(salary)   OVER (ORDER BY emp_id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total
FROM employees;
```

|Function|Behavior|
|---|---|
|`ROW_NUMBER()`|Unique sequential number, no ties|
|`RANK()`|Ties get same rank, next rank skips (1,1,3)|
|`DENSE_RANK()`|Ties get same rank, no skip (1,1,2)|
|`LAG()` / `LEAD()`|Access previous/next row's value|
|`NTILE(n)`|Bucket rows into n groups|
|Aggregate + `OVER()`|Running totals, moving averages|

---

## 10. Set Operations

```sql
SELECT name FROM employees_2023
UNION                              -- removes duplicates
SELECT name FROM employees_2024;

SELECT name FROM employees_2023
UNION ALL                          -- keeps duplicates, faster
SELECT name FROM employees_2024;

SELECT name FROM employees_2023
INTERSECT                          -- common rows
SELECT name FROM employees_2024;

SELECT name FROM employees_2023
EXCEPT                              -- (MINUS in Oracle) rows in first not in second
SELECT name FROM employees_2024;
```

_Requirement:_ same number of columns, compatible data types, across all combined queries.

---

## 11. CASE Expressions

```sql
SELECT name,
    CASE
        WHEN salary >= 100000 THEN 'Senior'
        WHEN salary >= 60000  THEN 'Mid'
        ELSE 'Junior'
    END AS band
FROM employees;
```

---

## 12. Common Table Expressions (CTEs)

Improves readability over nested subqueries; can be recursive.

```sql
WITH dept_avg AS (
    SELECT dept_id, AVG(salary) AS avg_sal
    FROM employees
    GROUP BY dept_id
)
SELECT e.name, e.salary, d.avg_sal
FROM employees e
JOIN dept_avg d ON e.dept_id = d.dept_id
WHERE e.salary > d.avg_sal;

-- Recursive CTE: org hierarchy
WITH RECURSIVE org_chart AS (
    SELECT emp_id, name, manager_id, 1 AS level
    FROM employees
    WHERE manager_id IS NULL         -- anchor: top of hierarchy

    UNION ALL

    SELECT e.emp_id, e.name, e.manager_id, oc.level + 1
    FROM employees e
    JOIN org_chart oc ON e.manager_id = oc.emp_id   -- recursive step
)
SELECT * FROM org_chart ORDER BY level;
```

---

## 13. Indexes

Indexes speed up reads at the cost of slower writes and extra storage.

```sql
CREATE INDEX idx_employees_dept ON employees(dept_id);
CREATE UNIQUE INDEX idx_employees_email ON employees(email);
DROP INDEX idx_employees_dept;
```

- Use on columns frequently in `WHERE`, `JOIN`, `ORDER BY`.
- Composite indexes: order of columns matters — leftmost prefix is used first.
- Over-indexing slows down `INSERT`/`UPDATE`/`DELETE`.

---

## 14. Transactions (TCL)

```sql
BEGIN;                     -- or START TRANSACTION;

UPDATE accounts SET balance = balance - 500 WHERE acc_id = 1;
UPDATE accounts SET balance = balance + 500 WHERE acc_id = 2;

-- if everything looks right:
COMMIT;
-- if something went wrong:
ROLLBACK;

-- Partial rollback:
BEGIN;
UPDATE accounts SET balance = balance - 500 WHERE acc_id = 1;
SAVEPOINT sp1;
UPDATE accounts SET balance = balance + 500 WHERE acc_id = 2;
ROLLBACK TO sp1;    -- undoes only the second update
COMMIT;
```

**ACID properties:** Atomicity, Consistency, Isolation, Durability.

**Isolation levels** (weakest to strongest): `READ UNCOMMITTED` → `READ COMMITTED` → `REPEATABLE READ` → `SERIALIZABLE`. Higher isolation = fewer anomalies (dirty reads, non-repeatable reads, phantom reads) but more locking/lower concurrency.

---

## 15. Views

```sql
CREATE VIEW high_earners AS
SELECT name, salary, dept_id
FROM employees
WHERE salary > 100000;

SELECT * FROM high_earners;   -- query it like a table

DROP VIEW high_earners;
```

A view is a stored query, not stored data (unless it's a _materialized_ view, which caches results and must be manually/periodically refreshed: `REFRESH MATERIALIZED VIEW ...`).

---

## 16. Normalization (Quick Reference)

|Form|Rule|
|---|---|
|1NF|Atomic values, no repeating groups|
|2NF|1NF + no partial dependency on composite key|
|3NF|2NF + no transitive dependency (non-key depends only on key)|
|BCNF|Every determinant is a candidate key|

Normalization reduces redundancy/anomalies; denormalization trades some redundancy for read performance (common in analytics/OLAP).

---

## 17. Keys Summary

|Key|Meaning|
|---|---|
|Primary Key|Uniquely identifies a row, not null|
|Foreign Key|References primary key of another table|
|Candidate Key|Any column(s) that could be primary key|
|Composite Key|Primary key made of multiple columns|
|Surrogate Key|Artificial key (e.g. auto-increment ID) with no business meaning|

---

## 18. Query Optimization Quick Tips

- Filter early: push `WHERE` conditions to reduce rows before joins/aggregation where possible.
- Index columns used in `JOIN`, `WHERE`, `ORDER BY`.
- Avoid `SELECT *` in production code — fetch only needed columns.
- Prefer `EXISTS` over `IN` for large subqueries; prefer `JOIN` over correlated subqueries when possible.
- Use `EXPLAIN` / `EXPLAIN ANALYZE` to inspect the query plan and spot full table scans.
- Beware of implicit type conversions in `WHERE` clauses — they can silently disable index usage.

```sql
EXPLAIN ANALYZE
SELECT * FROM employees WHERE dept_id = 3;
```

---

## 19. NULL Handling

```sql
SELECT COALESCE(phone, 'N/A') AS phone FROM employees;   -- first non-null value
SELECT NULLIF(salary, 0) FROM employees;                  -- returns NULL if equal
SELECT * FROM employees WHERE phone IS NULL;
SELECT * FROM employees WHERE phone IS NOT NULL;
```

Remember: `NULL = NULL` evaluates to `NULL` (not `TRUE`), and any arithmetic/comparison involving `NULL` yields `NULL`, not `FALSE`.

---

## 20. Cheat-Sheet Summary

```
Written order:    SELECT → FROM → JOIN → WHERE → GROUP BY → HAVING → ORDER BY → LIMIT
Execution order:  FROM → JOIN → WHERE → GROUP BY → HAVING → SELECT → DISTINCT → ORDER BY → LIMIT

WHERE   → filters rows (before grouping, no aggregates allowed)
HAVING  → filters groups (after aggregation, aggregates allowed)

JOIN types → INNER, LEFT, RIGHT, FULL OUTER, CROSS, SELF
Set ops    → UNION, UNION ALL, INTERSECT, EXCEPT
```