"""
Python 3.8.10

Artificial
Manifactured
Menial
Encryption
"""
import random,string,math,sys,sympy,pprint
sys.dont_write_bytecode = True

class AMME():
    def __init__(self):
        self.data = {
            'letters': {}
        }
        self.alphabet = string.ascii_uppercase+" "+","+"!"+"?"+"Ü"+"Ö"+"Ä"
        self.min_number = 0
        self.max_number = 55
        self.alp_while_code = True

    def generate_vectors(self,letter):
        alphabet_vectors = {}
        #generate 8 vectors, or 4 vectors per letter
        for i in range(0,2):
            alphabet_vectors[letter] = {
                'u1': (random.randint(self.min_number,self.max_number),
                    random.randint(self.min_number,self.max_number)),
                'v1': (random.randint(self.min_number,self.max_number),
                    random.randint(self.min_number,self.max_number)),
                'u2': (random.randint(self.min_number,self.max_number),
                    random.randint(self.min_number,self.max_number)),
                'v2': (random.randint(self.min_number,self.max_number),
                    random.randint(self.min_number,self.max_number)),
            }
        return alphabet_vectors

    def calculate_letter(self,this_letter):
        status = True
        if (len(this_letter) > 0):
            alphabet_vectors = self.generate_vectors(this_letter)
            #calculate intersection
            for letter in alphabet_vectors:
                u1 = alphabet_vectors[letter]['u1']
                v1 = alphabet_vectors[letter]['v1']
                v2 = alphabet_vectors[letter]['v2']
                u2 = alphabet_vectors[letter]['u2']

                (r, s) = sympy.symbols("r s")
                equation_1 = sympy.Eq(
                    (u1[0]+v1[0]*s),
                    (u2[0]+v2[0]*r)
                )
                equation_2 = sympy.Eq(
                    (u1[1]+v1[1]*s),
                    (u2[1]+v2[1]*r)
                )
                solution = sympy.solve((equation_1,equation_2),(r,s))
                #check if it's a true solution
                if ((u1[0]+v1[0]*solution[s]) == u2[0]+v2[0]*solution[r]):
                    schnittpunkt_found = True
                else:
                    schnittpunkt_found = False
                    status = False
                if (schnittpunkt_found == True):
                    s = (
                        u1[0]+solution[s]*v1[0],
                        u1[1]+solution[s]*v1[1]
                    )
                    F = v1[0]*v2[0]+v1[1]*v2[1]
                    if (F < 0):
                        F = -F
                    len_vec = (
                        math.sqrt(v1[0]**2+v1[1]**2)*math.sqrt(v2[0]**2+v2[1]**2)
                    )
                    winkel_rad = math.acos(F/len_vec) #in rad
                    #convert in degree (360° = 2*PI)
                    winkel = round(winkel_rad*(360/(2*math.pi)))#in Degree
                    for letter in self.data['letters']:
                        if (winkel == self.data['letters'][letter]['winkel']):
                            status = False
                            break
                    self.data['letters'][this_letter] = {
                        'schnittpunkt': s,
                        'vectors': {
                            'u1': u1,
                            'u2': u2,
                            'v1': v1,
                            'v2': v2
                        },
                        'winkel': winkel
                    }
                else:
                    status = False
        return status

    def generate_alphabet_numbers(self):
        for letter in self.alphabet:
            while True:
                status = self.calculate_letter(letter)
                if (status == True):
                    break
        pprint.pprint(self.data['letters'])
            
    def encrypt_message(self):
        nachricht = input("Nachricht> ").upper()
        encrypted_elements = []
        key_data = {}
        for letter in self.data['letters']:
            key_data[letter] = self.data['letters'][letter]['winkel']
        for letter in nachricht:
            vectors = self.data['letters'][letter]['vectors']
            for vector in vectors:
                this_vector_args = "".join(f"{vectors[vector]}".split("("))
                this_vector = "".join(this_vector_args.split(")"))
                encrypted_elements.append(f"{this_vector}")
        encrypted_msg = ";".join(encrypted_elements)
        key = ""
        for element in key_data:
            key = key+f"{element}-{key_data[element]}+"
        print(f"[+] Encrypted-Message: {encrypted_msg}")
        print(f"[+] Key: {key}")
        try:
            dateiname = f"encrypted_message_{len(nachricht)}.txt"
            file = open(dateiname,'a')
            file.write(encrypted_msg+"\n"+"\n"+key)
            file.close()
            print(f"[+] Abgespeichert in {dateiname}")
        except Exception as error:
            print("[!] Datei konnte nicht abgespeichert werden!")
            print(error)

    def run(self):
        option = input("d[ecrypt]|e[ncrypt]: ")
        if (option == "e"):
            self.generate_alphabet_numbers()
            self.encrypt_message()
        else:
            self.decrypt_message()
        
    def decrypt_message(self):
        encrypted_msg = input("Verschlüsselte-Nachricht> ")
        key = input("Schlüssel> ")
        key_args = key.split("+")
        key_elements = {}
        for arg in key_args:
            elements = arg.split("-")
            if (len(elements) > 1): 
                key_elements[elements[0]] = int(elements[1])
        args = "".join(encrypted_msg.split(" "))
        msg_elements = args.split(";")
        elements = {}
        i = 1
        counter = {str(i):0}
        elements[i] = []
        for element in msg_elements:
            this_args = element.split(",")
            if (counter[str(i)] <= 3):
                elements[i].append((int(this_args[0]),int(this_args[1])))
            else:
                i += 1
                counter[str(i)] = 0
                elements[i] = [(int(this_args[0]),int(this_args[1]))]
            counter[str(i)] += 1
        #pprint.pprint(elements)
        encrypted_msg_elements = []
        for element in elements:
            u1 = elements[element][0]
            u2 = elements[element][1]
            v1 = elements[element][2]
            v2 = elements[element][3]
            (r, s) = sympy.symbols("r s")
            equation_1 = sympy.Eq(
                (u1[0]+v1[0]*s),
                (u2[0]+v2[0]*r)
            )
            equation_2 = sympy.Eq(
                (u1[1]+v1[1]*s),
                (u2[1]+v2[1]*r)
            )
            solution = sympy.solve((equation_1,equation_2),(r,s))
            this_s = solution[s]
            #print(solution)
            s = (
                u1[0]+this_s*v1[0],
                u1[1]+this_s*v1[1]
            )
            F = v1[0]*v2[0]+v1[1]*v2[1]
            if (F < 0):
                F = -F
            len_vec = (
                math.sqrt(v1[0]**2+v1[1]**2)*math.sqrt(v2[0]**2+v2[1]**2)
            )
            winkel_rad = math.acos(F/len_vec) #in rad
            #convert in degree (360° = 2*PI)
            winkel = round(winkel_rad*(360/(2*math.pi)))#in Degree
            encrypted_msg_elements.append(winkel)

        decrypted_msg_elements = []
        for winkel in encrypted_msg_elements:
            for element in key_elements:
                if (key_elements[element] == winkel):
                    decrypted_msg_elements.append(element)
                    break
        decrypted_msg = "".join(decrypted_msg_elements)
        print(f"[+] Decrypted Message> {decrypted_msg}")

if (__name__ == '__main__'):
    amme = AMME()
    amme.run()


