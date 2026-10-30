import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def generar_clave_bb84(num_bits=64):
    """
    Simula el protocolo BB84 entre un Emisor (Alice) y un Receptor (Bob).
    Retorna una clave secreta compartida en formato de cadena binaria.
    """
    simulator = AerSimulator()
    
    # 1. Alice genera bits aleatorios y elige bases aleatorias (0 = Rectilínea +, 1 = Diagonal X)
    alice_bits = np.random.randint(0, 2, num_bits)
    alice_bases = np.random.randint(0, 2, num_bits)
    
    # 2. Bob elige bases aleatorias para medir
    bob_bases = np.random.randint(0, 2, num_bits)
    
    bob_results = []
    
    # 3. Transmisión cuántica bit por bit
    for i in range(num_bits):
        qc = QuantumCircuit(1, 1)
        
        # Alice prepara el estado del cúbit
        if alice_bits[i] == 1:
            qc.x(0)  # Aplica X si el bit es 1
            
        if alice_bases[i] == 1:
            qc.h(0)  # Aplica Hadamard si la base de Alice es Diagonal
            
        # Bob mide en la base que seleccionó
        if bob_bases[i] == 1:
            qc.h(0)  # Aplica Hadamard antes de medir si la base de Bob es Diagonal
            
        qc.measure(0, 0)
        
        # Ejecución en el simulador
        result = simulator.run(qc, shots=1, memory=True).result()
        measured_bit = int(result.get_memory()[0])
        bob_results.append(measured_bit)
        
    # 4. Reconciliación de bases (Sifting): Solo conservan bits donde coinciden las bases
    clave_compartida = []
    for i in range(num_bits):
        if alice_bases[i] == bob_bases[i]:
            clave_compartida.append(str(alice_bits[i]))
            
    # Convertir la lista de bits coincidentes a un string binario
    clave_string = "".join(clave_compartida)
    
    return clave_string


def cifrar_password_xor(password: str, clave_binaria: str) -> str:
    """
    Cifra la contraseña usando la clave BB84 mediante una operación XOR básica.
    Retorna la contraseña cifrada en formato hexadecimal.
    """
    # Convertimos la contraseña a bytes y luego a un número entero
    pass_bytes = password.encode('utf-8')
    pass_int = int.from_bytes(pass_bytes, byteorder='big')
    
    # Convertimos la clave binaria cuántica a un entero
    clave_int = int(clave_binaria, 2)
    
    # Operación XOR clásica entre la contraseña y la clave cuántica
    cifrado_int = pass_int ^ clave_int
    
    # Retornamos en formato hexadecimal para guardarlo limpiamente en PostgreSQL
    return hex(cifrado_int)


if __name__ == "__main__":
    # Prueba individual del script cuántico
    clave_generada = generar_clave_bb84(64)
    print("Clave secreta obtenida por BB84:", clave_generada)
    
    password_prueba = "12345678"
    password_cifrada = cifrar_password_xor(password_prueba, clave_generada)
    
    print("Contraseña original:", password_prueba)
    print("Contraseña cifrada (Hex):", password_cifrada)