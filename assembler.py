import struct
import xml.etree.ElementTree as ET

class Assembler:
    def __init__(self, input_file, output_file, log_file):
        self.input_file = input_file
        self.output_file = output_file
        self.log_file = log_file

    def parse_instruction(self, line):
        """Парсинг строки с инструкцией."""
        parts = line.split()
        if len(parts) < 4:
            raise ValueError(f"Недостаточно аргументов для инструкции: {line}")

        opcode = int(parts[1])  # Первый аргумент — опкод
        operands = list(map(int, parts[2:]))  # Остальные аргументы — операнды
        return opcode, operands

    def assemble_instruction(self, opcode, operands):
        """Преобразование инструкции в бинарный формат."""
        if opcode == 154:  # Загрузка константы
            print(f"Сохраняем: opcode={opcode}, operands={operands}")
            return struct.pack("<BQI", opcode, operands[0], operands[1])
        elif opcode == 216:  # Чтение значения из памяти
            print(f"Сохраняем: opcode={opcode}, operands={operands}")
            return struct.pack("<BQI", opcode, operands[0], operands[1])
        elif opcode == 142:  # Запись значения в память
            print(f"Сохраняем: opcode={opcode}, operands={operands}")
            return struct.pack("<BQQI", opcode, operands[0], operands[1], operands[2])
        elif opcode == 75:  # Побитовый логический сдвиг влево
            print(f"Сохраняем: opcode={opcode}, operands={operands}")
            return struct.pack("<BQII", opcode, operands[0], operands[1], operands[2])
        else:
            raise ValueError(f"Неизвестный опкод: {opcode}")


    def assemble(self):
        """Чтение файла, парсинг инструкций и запись бинарного файла."""
        try:
            with open(self.input_file, "r") as f:
                lines = f.readlines()

            root = ET.Element("Instructions")

            with open(self.output_file, "wb") as binary_file:
                for line in lines:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue

                    opcode, operands = self.parse_instruction(line)
                    binary_instruction = self.assemble_instruction(opcode, operands)
                    binary_file.write(binary_instruction)

                    # Логируем инструкцию
                    instr_element = ET.SubElement(root, "Instruction")
                    ET.SubElement(instr_element, "Command").text = line.split()[0]
                    ET.SubElement(instr_element, "Opcode").text = str(opcode)
                    for operand in operands:
                        ET.SubElement(instr_element, "Operand").text = str(operand)

            tree = ET.ElementTree(root)
            tree.write(self.log_file)
            print(f"Бинарный файл сохранён в {self.output_file}, лог — в {self.log_file}.")
        except Exception as e:
            print(f"Ошибка сборки: {e}")

def main():
    import sys
    if len(sys.argv) != 4:
        print("Ошибка: требуется 3 аргумента: <input_file> <output_file> <log_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    log_file = sys.argv[3]

    assembler = Assembler(input_file, output_file, log_file)
    assembler.assemble()

if __name__ == "__main__":
    main()
