import unittest
import os
from assembler import Assembler

class TestAssembler(unittest.TestCase):
    def setUp(self):
        """Создание тестовых файлов перед каждым тестом."""
        self.input_file = "test_input.txt"
        self.output_file = "test_output.bin"
        self.log_file = "test_log.xml"
        
        with open(self.input_file, "w") as f:
            f.write("LOAD_CONST 154 10 20\n")
            f.write("READ_MEM 216 30 40\n")
            f.write("WRITE_MEM 142 50 60 70\n")
            f.write("SHIFT_LEFT 75 80 90 100\n")
    
    def tearDown(self):
        """Удаление тестовых файлов после каждого теста."""
        if os.path.exists(self.input_file):
            os.remove(self.input_file)
        if os.path.exists(self.output_file):
            os.remove(self.output_file)
        if os.path.exists(self.log_file):
            os.remove(self.log_file)

    def test_assemble(self):
        """Тест на успешную сборку бинарного файла."""
        assembler = Assembler(self.input_file, self.output_file, self.log_file)
        assembler.assemble()
        
        # Проверяем, что выходные файлы созданы
        self.assertTrue(os.path.exists(self.output_file))
        self.assertTrue(os.path.exists(self.log_file))
        
        # Проверяем размер бинарного файла
        with open(self.output_file, "rb") as f:
            binary_data = f.read()
        self.assertGreater(len(binary_data), 0)

if __name__ == "__main__":
    unittest.main()
