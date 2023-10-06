import os
import random

current_directory = os.getcwd()  # current working directory set at start

def parse_input(case, inp, select):  # read user input given a case to find, input, and split to return as rest of string (note: returns tuple pass/fail + rest of string)
    inp_lower = inp.lower()
    location = inp_lower.find(case)  # solve issue of upper/lower mismatch
    if location >= 0:  # if found
        result = inp.split()[select]
        oup = result.replace(" ", "").replace(";", "")
        return True, oup  # tuple pass, remainder of string
    else:
        return False, 'null'  # tuple fail, null string

def create_database(name):  # if a directory does not exist, creates one
    if not os.path.exists(name):
        os.makedirs(name)
        print("Database", name, "created.")
    else:
        print("!Failed to create database", name, "because it already exists.")

def delete_database(name, parent_path):  # if a directory exists lower than the original program directory, deletes it.
    path = os.path.join(parent_path, name)
    try:
        if os.path.isdir(path):
            if len(os.listdir(path)) == 0:
                os.rmdir(path)
            else:
                for f in os.listdir(path):
                    os.remove(os.path.join(name, f))
            print("Database", name, "deleted.")
        else:
            print("!Failed to delete", name, "because it does not exist.")
    except:
        print("!Failed to delete", name, "because it does not exist.")

def use_database(name, parent_path):  # if a directory exists lower than the original program directory, changes the working directory.
    path = os.path.join(parent_path, name)
    if not os.path.isdir(path):
        print("Database", name, "does not exist.")
    else:
        print("Using database", name, ".")
        os.chdir(path)

def create_table(table_name, inp):  # If a file does not exist, creates it with given parameters
    if os.path.exists(table_name):
        print("!Failed to create table", table_name, "because it already exists.")
    else:
        request = inp[12:]  # remove "create table" 12 characters
        table_data = request.replace(table_name, "")
        table_data = table_data.replace(";", "")
        table_data = table_data.lstrip("(")
        table_data = table_data[:-1]
        table_data = table_data.replace("(", "", 1)
        table_columns = table_data.split(",")
        with open(table_name, 'w+') as f:
            for item in table_columns:
                f.write("%s | " % item)
        print("Table", table_name, "created.")

def delete_table(name):  # If a file exists in the current database, deletes it.
    if os.path.exists(name):
        os.remove(name)
        print("Table", name, "deleted.")
    else:
        print("!Failed to delete", name, "because it does not exist.")

def select_table(name):  # If a file exists in the current database, prints its contents to the prompt.
    parent_path = os.getcwd()
    path = os.path.join(parent_path, name)
    if os.path.exists(name):
        with open(path, 'r') as f:
            print('\n')
            print(f.read())
    else:
        print("!Failed to query table", name, "because it does not exist.")

def alter_table(table_name, inp):  # If a file exists in the current database, modifies the table based on the command
    if os.path.exists(table_name):
        try:
            command = inp.split()[3]
            modifier = inp.split()[4]
            if "add" in command:
                with open(table_name, 'a') as f:
                    to_add = inp.split(command)[1].replace(";", " |").replace('\n', "")
                    f.write(to_add)
            if "delstring" in command:
                with open(table_name, 'r+') as f:
                    lines = f.readlines()
                    f.seek(0)
                    for line in lines:
                        if modifier not in line:
                            f.write(line)
                    f.truncate()
                with open(table_name, 'r+') as f:
                    lines = f.readlines()
                    f.seek(0)
                    for line in lines:
                        if not line.isspace():
                            f.write(line)
            print("Table", table_name, "modified.")
        except:
            print("!Failed to alter table", table_name, "due to improper command or modifiers")
    else:
        print("!Failed to alter table", table_name, "because it does not exist.")

def insert_table(table_name, inp):  # If a file exists in the current database, modifies the table based on the command
    if os.path.exists(table_name):
        try:
            with open(table_name, 'a') as f:
                lengths = 18 + len(table_name)
                request = inp[lengths:]
                table_data = request.replace(table_name, "")
                table_data = table_data.replace(";", "")
                table_data = table_data.replace("'", "").replace("(", "").replace(")", "")
                table_data = table_data[2:]
                table_columns = table_data.split(",")
                f.write('\n')
                for item in table_columns:
                    formatted_item = item.replace(" ", "")
                    f.write("%s | " % formatted_item)
            print("1 new record inserted.")
        except:
            print("!Failed to insert table", table_name, "due to improper command or modifiers")
    else:
        print("!Failed to insert table", table_name, "because it does not exist.")

def find_column_to_update(table_name, inp, case):
    result = parse_input(case, inp, 1)
    result2i = parse_input(case, inp, 3)
    word = result2i[1].replace("'", "")
    with open(table_name, 'r') as f:
        data = f.read()
    data = data.replace(" ", "")
    columns = data.split("|")
    sub = result[1]
    column_index = next((i for i, s in enumerate(columns) if sub in s), None)
    column = []
    with open(table_name, 'r') as f:
        for line in f:
            column.append(line.split('|')[column_index])
    return word, column, column_index

def update_table(table_name, user_input, key, lock):
    if os.path.exists(table_name):
        counter = 0
        try:
            col_set = find_column_to_update(table_name, user_input, "set")
            col_where = find_column_to_update(table_name, user_input, "where")
            column_to_change = col_set[1]
            for i in range(len(column_to_change)):
                column_to_change[i] = column_to_change[i].replace("'", "")
                column_to_change[i] = column_to_change[i].replace(" ", "")
            column_to_change = [int(i) for i in column_to_change]
            value = col_set[0]
            if len(value) > 0:
                value = value.replace("'", "")
                value = value.replace(" ", "")
                value = int(value)
            elif len(value) == 0:
                value = column_to_change[0]
            to_insert = value
            primary_key = col_where[0]
            where = col_where[1]
            for i in range(len(where)):
                where[i] = where[i].replace("'", "")
                where[i] = where[i].replace(" ", "")
                where[i] = int(where[i])
            for i in range(len(primary_key)):
                primary_key[i] = primary_key[i].replace("'", "")
                primary_key[i] = primary_key[i].replace(" ", "")
                primary_key[i] = int(primary_key[i])
            primary_key_index = col_where[2]
            column_to_change = [str(i) for i in column_to_change]
            with open(table_name, 'r') as f:
                data = f.read()
            data = data.replace(" ", "")
            rows = data.split("\n")
            rows = [row.split('|') for row in rows]
            for row in rows:
                if row[primary_key_index] in where:
                    row[column_to_change] = to_insert
                    counter += 1
            with open(table_name, 'w') as f:
                for row in rows:
                    row = '|'.join(row)
                    f.write(row)
                    f.write('\n')
            if counter == 0:
                print("!Failed to update table", table_name, "because no rows meet the where condition.")
            else:
                print(counter, "records modified.")
        except:
            print("!Failed to update table", table_name, "due to improper command or modifiers")
    else:
        print("!Failed to update table", table_name, "because it does not exist.")

def main():
    current_directory = os.getcwd()
    while True:
        try:
            user_input = input("Enter command: ")
            case = user_input.split()[0]
            if "create" in case:
                if "database" in user_input:
                    name = user_input.split()[2]
                    create_database(name)
                if "table" in user_input:
                    if os.getcwd() != current_directory:
                        table_name = os.path.join(os.getcwd(), user_input.split()[2])
                    else:
                        table_name = user_input.split()[2]
                    create_table(table_name, user_input)
            if "delete" in case:
                if "database" in user_input:
                    name = user_input.split()[2]
                    delete_database(name, current_directory)
                if "table" in user_input:
                    if os.getcwd() != current_directory:
                        table_name = os.path.join(os.getcwd(), user_input.split()[2])
                    else:
                        table_name = user_input.split()[2]
                    delete_table(table_name)
            if "use" in case:
                name = user_input.split()[1]
                use_database(name, current_directory)
            if "select" in case:
                name = user_input.split()[1]
                select_table(name)
            if "alter" in case:
                if os.getcwd() != current_directory:
                    table_name = os.path.join(os.getcwd(), user_input.split()[2])
                else:
                    table_name = user_input.split()[2]
                alter_table(table_name, user_input)
            if "insert" in case:
                if os.getcwd() != current_directory:
                    table_name = os.path.join(os.getcwd(), user_input.split()[2])
                else:
                    table_name = user_input.split()[2]
                insert_table(table_name, user_input)
            if "update" in case:
                if os.getcwd() != current_directory:
                    table_name = os.path.join(os.getcwd(), user_input.split()[1])
                else:
                    table_name = user_input.split()[1]
                update_table(table_name, user_input, 0, 0)
            if "exit" in case:
                exit()
        except:
            print("!Failed to execute command:", user_input)


if __name__ == "__main__":
    main()
