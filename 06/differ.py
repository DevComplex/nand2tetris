import sys

def load_file_data(file_path):
    f = open(file_path, "r")
    lines = f.readlines()
    return list(map(lambda x: x.strip(), lines))


class Differ:
    def __init__(self, f1_path, f2_path):
        assert f1_path
        assert f2_path

        self.f1_path = f1_path
        self.f2_path = f2_path
        self.f1_lines = None
        self.f2_lines = None

    def load_all_file_data(self):
        self.f1_lines = load_file_data(self.f1_path)
        self.f2_lines = load_file_data(self.f2_path)

    def equals(self):
        if len(self.f1_lines) == len(self.f2_lines):
            for i in range(0, len(self.f1_lines)):
                line_1 = self.f1_lines[i]
                line_2 = self.f2_lines[i]

                if line_1 != line_2:
                    return False
            return True
        return False

in_file_path = sys.argv[1]
out_file_path = sys.argv[2]

print(in_file_path)
print(out_file_path)

differ = Differ(in_file_path, out_file_path)
differ.load_all_file_data()
print(differ.equals())