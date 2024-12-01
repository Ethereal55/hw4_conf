import unittest
import os
from interpreter import VMInterpreter

class TestInterpreter(unittest.TestCase):
    def setUp(self):
        """Создание тестовых файлов перед каждым тестом."""
        self.binary_file = "test_output.bin"
        self.result_file = "test_result.xml"
        
        # Создаем бинарный файл для теста
        with open(self.binary_file, "wb") as f:
            f.write(b"\x9a\x00\x00\x00\x00\x00\x00\x00\x0a\x00\x00\x00")  # LOAD_CONST 154 10
            f.write(b"\xd8\x00\x00\x00\x00\x00\x00\x00\x1e\x00\x00\x00")  # READ_MEM 216 30
            f.write(b"\x8e\x00\x00\x00\x00\x00\x00\x00\x32\x00\x00\x00\x46")  # WRITE_MEM 142
            f.write(b"\x4b\x00\x00\x00\x00\x00\x00\x00\x50\x00\x00\x00\x64")  # SHIFT_LEFT 75
    
    def tearDown(self):
        """Удаление тестовых файлов после каждого теста."""
        if os.path.exists(self.binary_file):
            os.remove(self.binary_file)
        if os.path.exists(self.result_file):
            os.remove(self.result_file)

    def test_interpret(self):
        """Тест на успешную интерпретацию бинарного файла."""
        memory_range = (0, 100)
        interpreter = VMInterpreter(self.binary_file, self.result_file, memory_range)
        interpreter.interpret()
        
        # Проверяем, что файл результатов создан
        self.assertTrue(os.path.exists(self.result_file))
        
        # Проверяем содержимое файла
        with open(self.result_file, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("<memory>", content)
        self.assertIn("</memory>", content)

if __name__ == "__main__":
    unittest.main()
