"""
> Python 3.8.10
> A.M.M.E (Version 2.0)
> https://github.com/Pulsar7/A.M.M.E/blob/main/README.md
"""
import math,sympy,sys,argparse,os,string,random
from rich.console import Console
from rich import (pretty)
from rich.columns import Columns
from rich.panel import Panel

pretty.install()

class Encryption():
    def __init__(self,console,all_characters,vector_min_num,vector_max_num,max_failed_number,save_filepath,fast_mode):
        (self.console,self.all_characters,self.calculated,self.fast_mode) = (console,all_characters,{},fast_mode)
        self.encr_state = True
        (self.min_num,self.max_num,self.max_failed_number,self.save_filepath) = (vector_min_num,vector_max_num,
            max_failed_number,save_filepath
        )
        self.angles_counter = 0

    def generate_vectors(self):
        # d_v_1 = "direction-vector-1"
        # d_v_2 = "direction-vector-2"
        # s_v_1 = "support-vector-1"
        # s_v_2 = "support_vector-2"
        elements = [
            'd_v_1',
            's_v_1',
            's_v_2',
            'd_v_2'
        ]
        while True:
            vectors = {}
            for element in elements:
                vectors[element] = (random.randint(self.min_num,self.max_num),random.randint(self.min_num,self.max_num))
            t = sympy.symbols("t") # creating symbols for the equation
            solution_1 = sympy.solve(sympy.Eq((vectors['d_v_1'][0]*t),(vectors['d_v_2'][0])),t)
            solution_2 = sympy.solve(sympy.Eq((vectors['d_v_1'][1]*t),(vectors['d_v_2'][1])),t)
            if (solution_1 != solution_2):
                break
        return vectors

    def calculate_angle(self,element):
        (vectors,angle) = ({},None)
        self.calculated[element] = {}
        self.calculated[element]['angle'] = angle
        vectors = self.generate_vectors()
        if (len(vectors) > 0):
            # equate straight line equations
            (r,s) = sympy.symbols("r s") # creating symbols for the equation
            equation_a = sympy.Eq((vectors['s_v_1'][0]+r*vectors['d_v_1'][0]),
                (vectors['s_v_2'][0]+s*vectors['d_v_2'][0]))
            equation_b = sympy.Eq((vectors['s_v_1'][1]+r*vectors['d_v_1'][1]),
                (vectors['s_v_2'][1]+s*vectors['d_v_2'][1]))
            solution = sympy.solve((equation_a,equation_b),(r,s))
            if (len(solution) > 1): # check if there is any solution
                # check if both solutions are the same
                if (
                    (vectors['s_v_1'][0]+solution[r]*vectors['d_v_1'][0]) == (vectors['s_v_2'][0]+solution[s]*vectors['d_v_2'][0]) and (vectors['s_v_1'][1]+solution[r]*vectors['d_v_1'][1]) == (vectors['s_v_2'][1]+solution[s]*vectors['d_v_2'][1])):
                    # found intersection
                    s = (vectors['d_v_1'][0]*vectors['d_v_2'][0]+vectors['d_v_1'][1]*vectors['d_v_2'][1]) # calculating the scalar product of the direction vectors 'd_v_1' & 'd_v_2'
                    # self.console.log(s)
                    one = ((vectors['d_v_1'][0])**2+(vectors['d_v_1'][1])**2)
                    two = ((vectors['d_v_2'][0])**2+(vectors['d_v_2'][1])**2)
                    if (one >= 0 & two >= 0): # check if the square roote is not negative
                        p = ((math.sqrt(one))*(math.sqrt(two))) # calculating the product of the two lengths
                        # calculating angle between the line-equations
                        a_rad = math.acos((s)/(p)) # in RAD
                        a_deg = (a_rad*(360/(2*math.pi))) # in DEGREE
                        if (self.fast_mode == "True"):
                            a_deg = round(a_deg,5)
                        else:
                            a_deg = round(a_deg,15)
                        angle = a_deg
                    else:
                        # self.console.log("[red]SQUARE ROOTE IS NEGATIVE")
                        pass
                else:
                    # print("BOTH SOLUTIONS ARE NOT THE SAME")
                    pass
            else:
                # self.console.log("[red]NO SOLUTION: ",solution)
                pass
        return (vectors,angle)

    def check_if_angle_is_unique(self,angle):
        state = True
        for element in self.calculated:
            if (element != "vectors"):
                if (angle == self.calculated[element]['angle']):
                    state = False
                    break
        return state

    def encrypt(self,message):
        self.console.log(f"[yellow]Encrypting message '{message}' ({len(message)} Bytes)")
        with self.console.status(f"[bold yellow]Generating angles for {len(self.all_characters)} characters...") as status:
            for element in self.all_characters:
                failed_counter = 0
                while (self.encr_state == True):
                    try:
                        (vectors,angle) = self.calculate_angle(element)
                        if (angle != None and self.check_if_angle_is_unique(angle) == True):
                            self.angles_counter += 1
                            if ("." in str(angle)):
                                args = str(angle).split(".")
                                this_angle = "".join(args)+str(len(args[0]))
                            else:
                                this_angle = angle
                            this_angle = str(this_angle)
                            self.calculated[element]['angle'] = this_angle
                            self.calculated[element]['vectors'] = {}
                            for n in vectors: self.calculated[element]['vectors'][n] = vectors[n]
                            vectors.clear()
                            break
                        else:
                            if (self.max_failed_number != "infinite"):
                                failed_counter += 1
                                if (failed_counter > self.max_failed_number):
                                    self.encr_state = False
                                    self.console.log(f"[red]Too many errors while calculating angle for character '{element}'")
                                    break
                    except KeyboardInterrupt:
                        self.console.log("[red]Keyboard interrupt")
                        self.encr_state = False
                        break
            if (len(self.calculated) > 0 and self.encr_state == True):
                self.console.log(f"[green]Calculated angles for {self.angles_counter} characters")
                encrypted_msg_vectors = []
                for element in message:
                    for character in self.calculated:
                        if (character == element):
                            for vector in self.calculated[character]['vectors']:
                                encrypted_msg_vectors.append(self.calculated[character]['vectors'][vector])
                (key,encrypted_msg) = ("","")
                vectors = [f"{vector[0]}-{vector[1]}-" for vector in encrypted_msg_vectors]
                encrypted_msg = "".join(vectors)
                for element in self.calculated:
                    key = key+element+":*"+self.calculated[element]['angle']+"x."
                # self.console.log(f"[bold green]Key:[cyan] {key}")
                # self.console.log(f"[bold green]Encrypted-Message:[cyan] {encrypted_msg}")
                user_renderables = [Panel(f"Saved message & key in {self.save_filepath}",expand = True)]
                self.console.print(Columns(user_renderables))
                with open(self.save_filepath,'w') as file:
                    file.write(f"<<MESSAGE>>\n{encrypted_msg}")
                    file.write(f"\n\n<<KEY>>\n{key}_FAST_{self.fast_mode}\n")
            else:
                self.console.log(f"[red]Could not calculate angles for {len(self.all_characters)-self.angles_counter} characters!")
                self.encr_state = False
        if (self.encr_state == False):
            self.console.log(f"[bold red]Encryption failed!")
        else:
            self.console.log(f"[bold green]Encrypted message successfully!")
        self.calculated.clear()


class Decryption():
    def __init__(self,console,all_characters,vector_min_num,vector_max_num,max_failed_number,save_filepath):
        (self.console,self.all_characters) = (console,all_characters)
        (self.vector_min_num,self.vector_max_num,self.max_failed_number,self.save_filepath) = (vector_min_num,
            vector_max_num,max_failed_number,save_filepath
        )
        self.decr_state = True
        self.calculated = {}
        self.fast_mode = False

    def calculate_angles(self,vectors):
        state = True
        this_vectors = vectors
        for vectors in this_vectors:
            this_using_element_vectors = vectors
            self.calculated[vectors] = {}
            if (len(vectors) > 0):
                vectors = this_vectors[vectors]
                # equate straight line equations
                (r,s) = sympy.symbols("r s") # creating symbols for the equation
                equation_a = sympy.Eq((vectors['s_v_1'][0]+r*vectors['d_v_1'][0]),
                    (vectors['s_v_2'][0]+s*vectors['d_v_2'][0]))
                equation_b = sympy.Eq((vectors['s_v_1'][1]+r*vectors['d_v_1'][1]),
                    (vectors['s_v_2'][1]+s*vectors['d_v_2'][1]))
                solution = sympy.solve((equation_a,equation_b),(r,s))
                if (len(solution) > 1): # check if there is any solution
                    # check if both solutions are the same
                    if (
                        (vectors['s_v_1'][0]+solution[r]*vectors['d_v_1'][0]) == (vectors['s_v_2'][0]+solution[s]*vectors['d_v_2'][0]) and (vectors['s_v_1'][1]+solution[r]*vectors['d_v_1'][1]) == (vectors['s_v_2'][1]+solution[s]*vectors['d_v_2'][1])):
                        # found intersection
                        s = (vectors['d_v_1'][0]*vectors['d_v_2'][0]+vectors['d_v_1'][1]*vectors['d_v_2'][1]) # calculating the scalar product of the direction vectors 'd_v_1' & 'd_v_2'
                        one = ((vectors['d_v_1'][0])**2+(vectors['d_v_1'][1])**2)
                        two = ((vectors['d_v_2'][0])**2+(vectors['d_v_2'][1])**2)
                        if (one >= 0 & two >= 0): # check if the square roote is not negative
                            p = ((math.sqrt(one))*(math.sqrt(two))) # calculating the product of the two lengths
                            # calculating angle between the line-equations
                            a_rad = math.acos((s)/(p)) # in RAD
                            a_deg = (a_rad*(360/(2*math.pi))) # in DEGREE
                            if (self.fast_mode == True):
                                a_deg = round(a_deg,5)
                            else:
                                a_deg = round(a_deg,15)
                            angle = a_deg
                            self.calculated[this_using_element_vectors]['angle'] = angle
                        else:
                            state = False
                    else:
                        state = False
                else:
                    state = False
        return state

    def decrypt(self,encrypted_message):
        self.console.log(f"[green]Decrypting message '{encrypted_message}' ({len(encrypted_message)} Bytes)...")
        try:
            key = input("Please insert key> ")
            print("")
            with self.console.status(f"[bold yellow]Reading encryption-key...") as status:
                if ("x." in key and ":*" in key and "_FAST_" in key):
                    key_elements = {}
                    args = key.split("x.")
                    for arg in args:
                        if (arg != "" and arg != " " and "_FAST_" not in arg):
                            elements = arg.split(":*")
                            this_angle = elements[1]
                            comma_pos = this_angle[len(this_angle)-1]
                            this_angle = this_angle[:-1]
                            angle_elements = [element for element in this_angle]
                            angle_elements.insert(int(comma_pos),".")
                            this_angle = float("".join(angle_elements))
                            key_elements[elements[0]] = this_angle
                        if ("_FAST_" in arg):
                            self.fast_mode = arg.split("_FAST_")[1]
                else:
                    self.console.log(f"[red]Invalid Key!")
                    self.decr_state = False
            if (self.decr_state == True):
                self.console.log(f"[green]The specified key was accepted ({len(key)} Bytes)")
                with self.console.status(f"[bold yellow]Reading encrypted message...") as status:
                    if ("-" in encrypted_message):
                        args = encrypted_message.split("-")
                        elements = [
                            'd_v_1',
                            's_v_1',
                            's_v_2',
                            'd_v_2'
                        ]
                        this_vectors = {}
                        counter = 1
                        v_counter = 1
                        for arg in args:
                            if (arg != "" and arg != " "):
                                if (v_counter == 1):
                                    this_vectors[str(counter)] = []
                                    this_vectors[str(counter)].append(arg)
                                else:
                                    this_vectors[str(counter)].append(arg)
                                v_counter += 1
                                if (v_counter == 9):
                                    counter += 1
                                    v_counter = 1
                        vectors = {}
                        for element in this_vectors:
                            v_counter = 0
                            counter = 0
                            vectors[element] = {}
                            for coordinate in this_vectors[element]:
                                if (counter == 0):
                                    vectors[element][elements[v_counter]] = []
                                vectors[element][elements[v_counter]].append(int(coordinate))
                                counter += 1
                                if (counter == 2):
                                    v_counter += 1
                                    counter = 0
                        self.console.log("[green]Found vectors in message")
                        state = self.calculate_angles(vectors)
                        self.console.log("[green]Calculated angle of each character")
                        if (state == True):
                            decrypted_msg = []
                            for element in self.calculated:
                                this_angle = self.calculated[element]['angle']
                                for key_element in key_elements:
                                    if (key_elements[key_element] == this_angle):
                                        decrypted_msg.append(key_element)
                            decrypted_msg = "".join(decrypted_msg)
                            user_renderables = [Panel(f"[bold cyan]{decrypted_msg}",expand = True)]
                            self.console.print(Columns(user_renderables))
                        else:
                            self.console.log(f"[red]Invalid message! [bold red](vectors)")
                            self.decr_state = False
                    else:
                        self.console.log(f"[red]Invalid message!")
                        self.decr_state = False
        except KeyboardInterrupt as e:
            print("")
            self.console.log("[red]Keyboard interrupt")
            self.decr_state = False
        if (self.decr_state == True):
            self.console.log("[bold green]Decrypted message successfully!")
        else:
            self.console.log("[bold red]Decryption failed!")
        self.calculated.clear()

console = Console()
#
default_all_characters = string.ascii_letters+string.punctuation+" "
path = os.path.realpath(__file__).split(__file__)[0]
(default_vector_min_number,default_vector_max_number,default_max_failed_number,
    default_filepath_to_save_msg
) = (0,999,"infinite",f'{path}msg.txt')
parser = argparse.ArgumentParser()
parser.add_argument('-e','--encrypt', action="store_true", help="Encrypts plaintext to encrypted message")
parser.add_argument('-d','--decrypt', action="store_true", help="Decrypts encrypted message to plaintext")
parser.add_argument('-m','--message', help="Message that should be encrypted/decrypted", type = str)
parser.add_argument('-s','--save', help=f"File path where the message is to be saved (Default = {default_filepath_to_save_msg})", type=str,
    default = default_filepath_to_save_msg
)
parser.add_argument('-i','--min',help=f"Minimal number of vector coordinate (Default = {default_vector_min_number})",
    default = default_vector_min_number, type = int
)
parser.add_argument('-a','--max',help=f"Maximal number of vector coordinate (Default = {default_vector_max_number})",
    default = default_vector_max_number, type = int
)
parser.add_argument('-f','--max_failed',help=f"Maximum failed number of attempts to find an angle (Default = {default_max_failed_number})",
    default = default_max_failed_number, type = str
)
parser.add_argument('-u','--fast',help="Activates the fast-mode to encrypt a message (Default = deactivated)",
    action = "store_true"
)
args = parser.parse_args()
try:
    max_failed_num = int(args.max_failed)
except Exception as error:
    if (args.max_failed.lower() != "infinite"):
        max_failed_num = False
        console.log(f"[red]{error}")
    else:
        max_failed_num = args.max_failed.lower()
if (args.encrypt == False and args.decrypt == False or args.message == "" or args.message == None or max_failed_num == False):
    parser.print_help()
    sys.exit()
#

if (args.fast == True):
    console.log(f"[bold red]Fast-mode is activated. Only as many elements are generated as the message is long!")
    console.log(f"[bold red]In Fast-mode, the decimal places after the point are also shorter!")
    all_characters = [element for element in args.message]
else:
    all_characters = default_all_characters+string.digits
(vector_min_num,vector_max_num,max_failed_number) = (args.min,args.max,max_failed_num)

if (__name__ == '__main__'):
    os.system("clear") # 
    if (args.encrypt == True):
        encr = Encryption(console,all_characters,vector_min_num,vector_max_num,max_failed_number,args.save,args.fast)
        encr.encrypt(args.message)
    if (args.decrypt == True):
        decr = Decryption(console,all_characters,vector_min_num,vector_max_num,max_failed_number,args.save)
        decr.decrypt(args.message)
