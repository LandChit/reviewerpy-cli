from json import dump as jdump

class Translate():
    def __init__(self, path:str) -> None:
        self.path: str = path

    def clean(self, text:list[str]) -> list[str]:
        """Returns the list without line breaks and unecessary whitespaces

        Args:
            text (list[str]): Takes a list of strings

        Returns:
            list[str]: returns the list without these characters
            * \\n
        """        
        final:list = []
        for line in text:
            if line == "\n":
                continue
            line = line.replace("\n", "")
            line = line.split(":", maxsplit=1)
            line_ = []
            for l in line:
                line_.append(l.strip())
                
            final.append(":".join(line_))
            
        return final
            
    def readbyline(self) -> list[str]:
        return self.clean(open(self.path).readlines())

    def convert_todict(self, text:list[str]) -> dict:
        modes = {"norm":0, "group":1, "enum":2}
        data:dict = {}
        currentmode:int = 0
        
        for line in text:
            # mode change
            if line.startswith("@"):
                wmode = line.removeprefix("@").split()
                currentmode = modes[wmode[0]]
                try:
                    data[key] = val
                except:
                    print("0-0-0-STARTED-0-0-0")
            
            match currentmode:
                case 0:
                    if line.startswith("@"):
                        continue
                    val, key = line.split(":",1)
                    data[key] = val # This will get doubled but its fine
                
                case 1:
                    if line.startswith("@"):
                        wmode.pop(0)
                        key = " ".join(wmode)
                        val = {}
                        continue
                    try:
                        _val, _key = line.split(":", 1)
                        val[_key] = _val
                    except ValueError:
                        print("ERROR ON: ")
                        print(line)
                        print("--continuing--")

                case 2:
                    if line.startswith("@"):
                        wmode.pop(0)
                        key = " ".join(wmode)
                        val = []
                        continue
                    val.append(line)
                    
        data[key] = val
        return data
                
    

if __name__ == "__main__":
    file = Translate("PE.txt")
    dictf = file.convert_todict(file.readbyline())
    ofile = open("PE-quiz.json", "w+")
    jdump(dictf,ofile, indent=2)
