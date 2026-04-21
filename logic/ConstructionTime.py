from colorama import Fore

class ConstructionTimeCalculator:
    def __init__(self) -> None:
        
        self.params = {};
        self.sheet = {};
        
        return

    def import_spreadsheet(self, path: str) -> None:
        with open(path, 'r') as f:
            lines = f.readlines();

            if len(lines) == 0:
                raise Exception(f'({path}): Sheet is empty or corrupted.');

            flags = [0, 0];
            for line in lines:
                if len(line) == 0 or line == '\n':
                    continue
                kws = line.split();
                if kws[0] == '.section':
                    if flags[1] == 1:
                        raise SyntaxError(f"'\u007b' was not closed in file {path}.");
                    match kws[1]:
                        case '@':
                            flags[0] = 1;
                            flags[1] = 1;
                        case '$':
                            flags[0] = 2;
                            flags[1] = 1;
                
                elif kws[0] == '.end':
                    flags[1] = 0;
                
                else:       
                    if not flags[1] == 1:
                        raise SyntaxError(f"Data provided without section defined in file {path}.");
                    match flags[0]:
                        case 1:
                            params = line.split();
                            if len(params) == 2:
                                self.params[params[0]] = params[1];
                            elif len(params) == 3:
                                self.params[params[0]] = (((params[2] == "int" or params[2] == "integer") and int(params[1])) or params[1]);
                            else:
                                raise SyntaxError(f'Argument count for the Param Section needs to be two (+ optional type), {len(params)} given in file {path}.');

                                
                        case 2:
                            times = line.split();
                            if len(times) == 2:
                                self.sheet[times[0]] = times[1];
                            else:
                                raise SyntaxError(f'Argument count for the Sheet Section needs to be exactly two, {len(times)} given in file {path}.');

    def __str__(self) -> str:
        return Fore.CYAN + '[ * PARAMETERS * ]\n' + Fore.RESET + ''.join([f'*{str.upper(p)}: {v}\n' for p,v in self.params.items()]) + Fore.GREEN + '\n[ * SHEET * ]' + Fore.RESET + ''.join([f'\n{str.upper(p)}: {v}' for p,v in self.sheet.items()]);
        
import os


PATH = os.getcwd() + '\\sheets\\ConstructionSpreadSheet1.csh';




constr = ConstructionTimeCalculator();
constr.import_spreadsheet(PATH);
print(constr);