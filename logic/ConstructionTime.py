from colorama import Fore
from stdconst import apply_overhead, ignore, mutate

class ConstructionTimeCalculator:
    def __init__(self) -> None:
        
        self.params = {};
        self.sheet = {};
        self.muters = {};

        self.functions = {};
        
        return

    def add_functions(self, fcs: dict[str, callable]) -> None:
        self.functions.update(fcs);

    def import_spreadsheet(self, path: str) -> None:
        with open(path, 'r') as f:
            lines = f.readlines();

            if len(lines) == 0:
                raise Exception(f'({path}): Sheet is empty or corrupted.');

            flags = [0, 0];
            for line in lines:
                if len(line) == 0 or line == '\n' or line[0] == '#':
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

                            if len(params) > 0 and params[0] == "param":
                    
                                if len(params) == 3:
                                    self.params[params[1]] = params[2];
                                
                                elif len(params) == 4:
                                    self.params[params[1]] = (
                                    
                                        ((params[3] == "num" or params[3] == "number") and float(params[2]))
                                        or
                                        ((params[3] == "percent" or params[3] == "percentage") and float(params[2])/100) 
                                        or params[2]

                                    );
                                else:
                                    raise SyntaxError(f'Argument count for the Param Section needs to be 3 (+ optional type), {len(params)} given in file {path}.');

                            elif len(params) > 0:
                                temp = [];
                                l = len(params);

                                for i in range(len(params)):
                                    if i == 0 or params[i] in ['percent', 'percentage', 'num', 'number']:
                                        continue;
                                    elif '$' in str(params[i]):
                                        temp.append(params[i]);
                                    else:
                                        if l > i+1:
                                            temp.append((
                                                ((params[i+1] in ['percent', 'percentage']) and float(params[i])/100)
                                                or
                                                ((params[i+1] in ['num', 'number']) and float(params[i]))
                                                or
                                                (params[i])
                                            )
                                            );
                                        else:
                                            temp.append(params[i]);

                                self.muters[params[0]] = temp;
                                
                        case 2:
                            times = line.split();
                            if len(times) == 2:
                                self.sheet[times[0]] = float(times[1]);
                            else:
                                raise SyntaxError(f'Argument count for the Sheet Section needs to be exactly two, {len(times)} given in file {path}.');

    def calculate(self) -> int | float:
        sh_sum = 0;


        for k, v in self.sheet.items():
            st = v;
            for p, _v in self.muters.items():
                if f'${k}' in _v:
                    _v_changed = list(map(lambda x: st if '$' in str(x) else x, _v.copy()));
                    st = self.functions[p](_v_changed);
        
            sh_sum += st
    
        sh_sum += sh_sum * self.params.get('overhead', 0);
    
        return sh_sum;

    def __str__(self) -> str:
        return (Fore.LIGHTMAGENTA_EX + 
                '\n----- [ INFO ] -----\n' 
                + Fore.CYAN 
                
                + '\n[ * PARAMETERS * ]\n' + Fore.RESET 
                
                + ''.join([f'*{str.upper(p)}: {v}\n' for p,v in self.params.items()]) 
                + Fore.YELLOW 

                + '\n[ * MUTERS * ]\n' + Fore.RESET 
                
                + ''.join([f'*{str.upper(p)}: &{v}\n' for p,v in self.muters.items()]) 
                + Fore.GREEN 
                
                + '\n[ * SHEET * ]\n' + Fore.RESET 
                
                + ''.join([f'{str.upper(p)}: {v}\n' for p,v in self.sheet.items()]) 
                + Fore.LIGHTMAGENTA_EX 
                
                + '\n----- [ END ] -----' 
                + Fore.RESET);
    
    def write_to_file(self, path: str = 'scratch_workoutput.csho') -> None:
        with open(path, 'w+') as f:
            f.write(Fore.LIGHTMAGENTA_EX + 
                '\n----- [ INFO ] -----\n' 
                
                + '\n[ * PARAMETERS * ]\n'
                
                + ''.join([f'*{str.upper(p)}: {v}\n' for p,v in self.params.items()]) 

                + '\n[ * MUTERS * ]\n'
                
                + ''.join([f'*{str.upper(p)}: &{v}\n' for p,v in self.muters.items()]) 
                
                + '\n[ * SHEET * ]\n'
                
                + ''.join([f'{str.upper(p)}: {v}\n' for p,v in self.sheet.items()]) 
                
                + '\n----- [ END ] -----'
                
                + f'\nTOTAL SUM OF WORKHOURS: {self.calculate()}'
                );
        
import os


PATH = os.getcwd() + '\\sheets\\ConstructionSpreadSheet1.csh';



constr = ConstructionTimeCalculator();
constr.import_spreadsheet(PATH);
print(constr);

constr.add_functions({'apply_overhead': apply_overhead, 'ignore': ignore, 'mutate': mutate});

print('Total time for construction:', constr.calculate());

constr.write_to_file();