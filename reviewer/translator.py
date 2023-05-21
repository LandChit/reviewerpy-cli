

zero_width_space = "​"

class Translate:
    def __init__(self, path: str) -> None:
        remove_linebreak: list[str] = [
            line.replace("\n", "")
            for line in open(path, "r").readlines()
            if line != "\n" if line != ''
        ]
        self.data: list[str] = [
            line for line in remove_linebreak if not line.startswith("#")
        ]

    def convert(self) -> dict:
        modes = {0: "grouped", 1: "enumerated"}
        mode: int
        data: dict = {}
        key = None
        value = None
        for line in self.data:
            if line.startswith("@"):
                # to filter out blank groups
                if value is not None and value != [] and value != {}:
                    data[key] = value

                if line.startswith("@g"):
                    key = line.removeprefix("@g").strip().replace(zero_width_space, "")
                    value = {}
                    mode = 0
                if line.startswith("@og"):
                    key = zero_width_space + line.removeprefix("@og").strip()
                    value = {}
                    mode = 0
                if line.startswith("@e"):
                    key = line.removeprefix("@e").strip().replace(zero_width_space, "")
                    value = []
                    mode = 1
                if line.startswith("@oe"):
                    key = zero_width_space + line.removeprefix("@oe").strip()
                    value = []
                    mode = 1
                continue
            
            match modes[mode]:
                case "grouped":
                    try:
                        _value, _key = line.split(":", 1)
                        _key = _key.strip()
                        _value = _value.strip()
                        value[_key] = _value
                    except ValueError:
                        print("-----ERROR-----")
                        print(f"MODE: {modes[mode]}")
                        print(f"LINE: {line}")

                case "enumerated":  # enumerate
                    value.append(line)
        
        # last value
        if value is not None and value != [] and value != {}:
                    data[key] = value
                    
        return data

#for testing purposes
if __name__ == "__main__":
    test = Translate("test_text.txt")
    print(test.data)
    print(test.convert())
