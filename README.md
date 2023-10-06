# Linux-Based-SQL-Database-System
RUNNING INSTRUCTIONS:
1.	Extract the files from rbothne_pa4.zip
2.	Navigate into the directory holding rbothne_PA4.py from the terminal
3.	Execute the program manually using the format found in the test file
   
The database system utilizes the file directory system of the machine.
A table is simply a file.
A database is simply a directory.
A table in a database is simply a file in a directory.
If “using” a database, we simply navigate to the directory specified if it exists.
If creating a database we check its existence, if it does not exist, we create a directory.
If creating a table we check its existence, if it does not exist, we create a table.
If altering a table we check its existence, if it does exist, we change file values.
If selecting a table we check its existence, if it exists, we change print its values to the console.
If inserting new data in a table, we simply append the new information to the file.
If deleting a value in a table, we find satisfying rows and remove their contents before sliding them back into a list of all the rows and reprint the file.
If updating a value in a table we find satisfying rows, split them into columns and change the specified contents before sliding them back into a list of all the rows, and reprint the file.
If querying a value in a table we find satisfying rows, split them into columns and print the desired to be printed columns.

Join Operations:
Preparation:
Store the name and symbol of both tables in separate tuples.
Determine the type of join (e.g., inner join, outer join).
 
Column Selection:
Take user input to specify which columns to compare during the join operation.

Inner Join:
Find the index of the specified column in both tables.
Compare values at that index for each row.
Include only matching rows from both tables in the result.

Outer Join:
Follow the same process as with inner join.
If a row is not found in the newly joined table:
Append any value from the left table that wasn't included in the first pass to the result.

Key Generation:
When a user initiates a transaction using "begin transaction," a random float value is generated as the "key."

Lock Creation:
The generated key is used to create a lock file with a specific name, such as "Flightslock."

Key Storage:
The generated key value is stored within the newly created lock file.

Committing Updates:
When a user attempts to "commit" an update to a file, the lock file is consulted.
The key value in the lock file is compared to the generated key value.
If the key values match, the update is allowed to commit.
If the key values differ, the transaction is aborted.
