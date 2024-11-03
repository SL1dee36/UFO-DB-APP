from typing import Dict, List, Any
import os

class UFORecords:
    def __init__(self):
        self.fields = {}

    def get_field(self, field_name: str) -> str:
        return self.fields.get(field_name, "")

    def add(self, field_name: str, value: str) -> None:
        self.fields[field_name] = value

    def __repr__(self) -> str:
        return str(self.fields)


class UFOTable:
    def __init__(self, table_name: str, columns: List[str]):
        self.name = table_name
        self.columns = columns
        self.records = []
        self.next_id = 1

    def insert_record(self, record_data: Dict[str, str]) -> None:
        new_record = UFORecords()
        for key, value in record_data.items():
            new_record.add(key, value)
        new_record.add("id", str(self.next_id))
        self.next_id += 1
        self.records.append(new_record)

    def select_all(self) -> None:
        self._print_header()
        for record in self.records:
            self._print_record(record)

    def select_where(self, field_name: str, value: str) -> List[UFORecords]:
        return [record for record in self.records if record.get_field(field_name) == value]

    def update_record(self, record_id: int, updates: Dict[str, str]) -> None:
        try:
            record = next(record for record in self.records if record.get_field("id") == str(record_id))
            for field, value in updates.items():
                record.add(field, value)
        except StopIteration:
            raise RuntimeError(f"Record with id {record_id} not found.")

    def delete_record(self, record_id: int) -> bool:
        try:
            index = next(i for i, record in enumerate(self.records) if record.get_field("id") == str(record_id))
            del self.records[index]
            return True
        except StopIteration:
            return False

    def _print_header(self) -> None:
        print(f"| {'id':<10}", end="")
        for col in self.columns:
            print(f" | {col:<10}", end="")
        print(" |")
        print("-" * (13 + len(self.columns) * 13))

    def _print_record(self, record: UFORecords) -> None:
        print(f"| {record.get_field('id'):<10}", end="")
        for col in self.columns:
            print(f" | {record.get_field(col):<10}", end="")
        print(" |")



class Relative_DB: 
    def __init__(self):
        self.tables = {}

    def create_table(self, name: str, columns: List[str]) -> None:
        if name in self.tables:
            raise RuntimeError(f"Table with name {name} already exists.")
        self.tables[name] = UFOTable(name, columns)

    def insert(self, table_name: str, record_data: Dict[str, str]) -> None:
        if table_name not in self.tables:
            raise RuntimeError(f"Table with name {table_name} does not exist.")
        self.tables[table_name].insert_record(record_data)

    def select(self, table_name: str) -> None:
        if table_name not in self.tables:
            raise RuntimeError(f"Table with name {table_name} does not exist.")
        self.tables[table_name].select_all()

    def update(self, table_name: str, record_id: int, updates: Dict[str, str]) -> None:
        if table_name not in self.tables:
            raise RuntimeError(f"Table with name {table_name} does not exist.")
        self.tables[table_name].update_record(record_id, updates)

    def delete_record(self, table_name: str, record_id: int) -> bool:
        if table_name not in self.tables:
            return False
        return self.tables[table_name].delete_record(record_id)

    def save_to_file(self, filename: str) -> bool:
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(str(len(self.tables)) + '\n')
                for table_name, table in self.tables.items():
                    f.write(table_name + '\n')
                    f.write(str(len(table.columns)) + '\n')
                    f.write('\n'.join(table.columns) + '\n')
                    f.write(str(table.next_id) + '\n')
                    f.write(str(len(table.records)) + '\n')
                    for record in table.records:
                        record_data = [record.get_field(col) for col in table.columns]
                        f.write('|'.join(record_data) + '|' + record.get_field("id") + '\n')
            return True
        except (IOError, OSError) as e:
            print(f"Error saving to file: {e}")
            return False


    def load_from_file(self, filename: str) -> bool:
        if not os.path.exists(filename):
            print(f"Error: File '{filename}' not found.")
            return False

        try:
            with open(filename, 'r', encoding='utf-8') as f:
                num_tables = int(f.readline().strip())
                for _ in range(num_tables):
                    table_name = f.readline().strip()
                    num_columns = int(f.readline().strip())
                    columns = [f.readline().strip() for _ in range(num_columns)]
                    table = UFOTable(table_name, columns)
                    table.next_id = int(f.readline().strip())
                    num_records = int(f.readline().strip())
                    for _ in range(num_records):
                        line = f.readline().strip()
                        record_data = line.split('|')
                        record = UFORecords()
                        for i, col in enumerate(table.columns):
                            record.add(col, record_data[i])
                        record.add("id", record_data[-1])
                        table.records.append(record)
                    self.tables[table_name] = table
                return True
        except (IOError, OSError, ValueError, IndexError) as e:
            print(f"Error loading from file: {e}")
            return False