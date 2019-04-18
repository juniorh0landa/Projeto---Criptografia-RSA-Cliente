from random import randint

class RSA:
    def __init__(self, n = 0, d = 0.1):
        def setup(d): #CRIAÇÃO DAS CHAVES PÚBLICA E PRIVADA
            while int(d) != d:
                primos = []
                for n in range(10, 300, 1):
                    for aux in range(2, n, 1):
                        if n % aux == 0:
                            break
                    else:
                        primos.append(n)
                aux = randint(0,len(primos) - 1)
                p = primos[aux]
                primos.pop(aux)
                aux = randint(0,len(primos) - 1)
                q = primos[aux]
                n =  p*q
                phi = (p - 1)*(q - 1)
                d = 4*((phi - 4)/6) + 3
            return n, int(d)
        
        if int(d) != d:
            self.PublicKey, self.PrivateKey = setup(d)
        else:
            self.PublicKey = n
            self.PrivateKey = d
            
        
    def encrypt(self, string): #CRIPTOGRAFIA
        n = self.PublicKey
        string = string.lower()
        ##teste se o texto é válido
        teste = []
        for x in range(0, len(string)):
            if ord(string[x]) == 32 or (ord(string[x]) >= 95 and ord(string[x]) <= 122):
                teste.append(0)
            else:
                teste.append(1)
                break
        ##codificação
        if sum(teste) == 0:
            encrypt = []
            for x in range(0, len(string)):
                encrypt.append(str(pow(ord(string[x]),3,n)))
            string = " ".join(encrypt)
        else:
            string = "Texto inválido"
        return string
    
    def decrypt(self, string): #DESCRIPTOGRAFIA
        n = self.PublicKey
        d = self.PrivateKey
        decrypt = []
        string = string.split(" ")
        for x in range(len(string)):
            decrypt.append(chr(pow(int(string[x]),d,n)))
        string = "".join(decrypt)
        return string

class Cliente(RSA):
    def __init__(self):
        #lê os usuários
        arquivo = []
        try:
            with open("usuarios.txt") as file:
                for line in file:
                    if str("\n") in line:
                        line, resto = line.split("\n")
                    arquivo.append(line)
    
            d, n = arquivo[0].split(") (")
            if len(n) != 0 and len(d) != 0:
                n = int(n[0:(len(n)-1)])
                d = int(d[1:len(d)])
                arquivo.pop(0)
        except:
            n = 0
            d = 0.1
        
        #descriptografa
        super().__init__(n, d)
        self.clientes = [[],[]]
        
        for i in range(len(arquivo)):
            if i%2 != 0:
                self.clientes[1].append(self.decrypt(arquivo[i]))
            else:
                self.clientes[0].append(self.decrypt(arquivo[i]))
    
    def __len__(self):
        return len(self.clientes[0])
    
    def verify(self, string):
        if string in self.clientes[0]:
            aux = self.clientes[0].index(string)
        else:
            aux = -1
        return aux
    
    def add(self, usuario, senha):
        aux = self.verify(usuario)
        if aux < 0:
            self.clientes[0].append(usuario)
            self.clientes[1].append(senha)
            print("Usuário ",usuario," adicionado")
        else:
            print("Usuário existente. Escolha outro nome")
    
    def delete(self, usuario):
        aux = self.verify(usuario)
        if aux < 0:
            print("Usuário inexistente. Escolha outro nome")
        else:
            confirm = str(input("Usuário encontrado. Confirmar exclusão? (s/n) "))
            if confirm.lower() == "s":
                print("Usuário ",usuario," excluído")
                self.clientes[0].pop(aux)
                self.clientes[1].pop(aux)
        return

p1 = Cliente()

options = 1
while options != 4:
    print("\n", len(p1.clientes[0]), " usuário(s)")
    print("\n[1] adicionar usuário \n[2] deletar usuário\n[3] verificar usuário\n[4] finalizar programa")
    options = int(input("Digite a opção: "))
    if options == 1:
        usuario = input("Digite o nome de usuário: ")
        senha = input("Digite  senha: ")
        p1.add(usuario, senha)
    elif options == 2:
        p1.delete(input("Digite o nome de usuário: "))
    elif options == 3:
        aux=p1.verify(input("Digite o nome de usuário: "))
        if aux < 0:
            print("Usuário inexistente.")
        else:
            print("Usuário existente.")
        

print("\nPROGRAMA FINALIZADO")

arquivo = open('usuarios.txt', 'w')
if len(p1.clientes[0]) != 0:
    novo=RSA()
    arquivo.write("("+str(novo.PrivateKey)+") ("+str(novo.PublicKey)+")")
    p1.PublicKey = novo.PublicKey
    p1.PrivateKey = novo.PrivateKey
    for i in range(len(p1.clientes[0])):
        for j in range(2):        
            arquivo.write('\n'+str(p1.encrypt(p1.clientes[j][i])))
del i, j, options, senha, usuario
arquivo.close()