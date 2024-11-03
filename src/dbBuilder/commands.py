# commands.py
import re

def execute_command(command, table):
    # Измененное регулярное выражение для обработки нескольких операндов
    match = re.match(r"=(\s*\{.+?\}\w+\s*)(\s*[+\-*/]\s*\{.+?\}\w+\s*)*", command)
    if not match:
        raise ValueError("Invalid command format. Use format ={...}col [+|-|*|/]{...}col")

    operands = []
    operators = []
    parts = re.split(r'\s*([+\-*/])\s*', match.group(0)[1:]) # Разделим на операнды и операторы

    for i, part in enumerate(parts):
        if i % 2 == 0: # Операнд
            operands.append(evaluate_cell_reference(part, table))
        else: # Оператор
            operators.append(part)


    result = operands[0]
    for i in range(len(operators)):
        operator = operators[i]
        operand = operands[i+1]
        if operator == '+':
            result += operand
        elif operator == '-':
            result -= operand
        elif operator == '*':
            result *= operand
        elif operator == '/':
            if operand == 0:
                raise ZeroDivisionError("Division by zero")
            result /= operand

    return result


def evaluate_cell_reference(cell_ref, table):
    match = re.match(r"{(\d+)}(\w+)", cell_ref)
    if not match:
        raise ValueError("Invalid cell reference format.")

    row_index = int(match.group(1))
    col_name = match.group(2).lower()  # Case-insensitive column names

    try:
        if col_name.isdigit(): # Check if column reference is numeric (id or index)

            col_index = int(col_name)
            if 0 <= col_index < len(table.columns + ["id"]):
                value = table.records[row_index].fields.get( (table.columns + ["id"])[col_index] )
            else:
                raise IndexError("Column index out of range.")

        elif col_name == "id": #Handle special "id" column
            value = table.records[row_index].fields["id"]


        else: # Column reference is a name
            if col_name in table.columns:
                value = table.records[row_index].fields[col_name]
            else:
                raise ValueError(f"Column '{col_name}' not found.")



        try:
            return int(value)  # Attempt converting to integer
        except (ValueError, TypeError):
            try:
                return float(value) # If not int, try float
            except (ValueError, TypeError):
                 return value # Return as string if not a number



    except IndexError:
        raise IndexError("Row index out of range.")
    except KeyError:
        raise ValueError("Invalid column name or ID.") # More informative error message