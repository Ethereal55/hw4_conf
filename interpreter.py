import struct
import xml.etree.ElementTree as ET


class VMInterpreter:
    def __init__(self, binary_file, result_file, memory_range):
        self.binary_file = binary_file
        self.result_file = result_file
        self.memory_range = memory_range
        self.memory = {}  # Используем словарь для хранения данных памяти
        self.instruction_pointer = 0  # Указатель инструкций
        self.binary_data = b""  # Содержимое бинарного файла

    def load_binary(self):
        """Загружает бинарный файл в память."""
        with open(self.binary_file, "rb") as f:
            self.binary_data = f.read()
        print(f"Бинарный файл загружен: {len(self.binary_data)} байт")

    def execute_instruction(self):
        """Выполняет одну инструкцию на основе текущего указателя."""
        if self.instruction_pointer >= len(self.binary_data):
            raise ValueError("Указатель инструкций выходит за пределы памяти")

        opcode = self.binary_data[self.instruction_pointer]
        if opcode == 154:  # LOAD_CONST
            addr, const = struct.unpack_from("<QI", self.binary_data, self.instruction_pointer + 1)
            self.memory[addr] = const
            self.instruction_pointer += 10
        elif opcode == 216:  # READ_MEM
            dest, src = struct.unpack_from("<QQ", self.binary_data, self.instruction_pointer + 1)
            self.memory[dest] = self.memory.get(src, 0)
            self.instruction_pointer += 17
        elif opcode == 142:  # WRITE_MEM
            base, offset, src = struct.unpack_from("<QHI", self.binary_data, self.instruction_pointer + 1)
            target_addr = base + offset
            self.memory[target_addr] = self.memory.get(src, 0)
            self.instruction_pointer += 13
        elif opcode == 75:  # SHIFT_LEFT
            dest, src1, src2 = struct.unpack_from("<QII", self.binary_data, self.instruction_pointer + 1)
            val1 = self.memory.get(src1, 0)
            val2 = self.memory.get(src2, 0)
            self.memory[dest] = val1 << val2
            self.instruction_pointer += 13
        else:
            raise ValueError(f"Неизвестный опкод: {opcode}")

    def save_to_xml(self):
        """Сохраняет диапазон памяти в XML."""
        root = ET.Element("memory")
        for addr in range(self.memory_range[0], self.memory_range[1] + 1):
            value = self.memory.get(addr, 0)
            ET.SubElement(root, "cell", address=str(addr)).text = str(value)

        tree = ET.ElementTree(root)
        with open(self.result_file, "wb") as f:
            tree.write(f, encoding="utf-8", xml_declaration=True)
        print(f"Диапазон памяти сохранён в файл {self.result_file}")

    def interpret(self):
        """Основной процесс интерпретации."""
        self.load_binary()
        while self.instruction_pointer < len(self.binary_data):
            self.execute_instruction()
        self.save_to_xml()


def main():
    import sys
    if len(sys.argv) != 5:
        print("Использование: <binary_file> <result_file> <range_start> <range_end>")
        sys.exit(1)

    binary_file = sys.argv[1]
    result_file = sys.argv[2]
    try:
        range_start = int(sys.argv[3])
        range_end = int(sys.argv[4])
    except ValueError:
        print("Ошибка: диапазон должен быть целыми числами.")
        sys.exit(1)

    interpreter = VMInterpreter(binary_file, result_file, (range_start, range_end))
    interpreter.interpret()


if __name__ == "__main__":
    main()
