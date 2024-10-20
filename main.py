import hashlib
import datetime as date
import json

# Structure Blockchain:
class InputTraceability:
    def __init__(self, code: str, timestamp: date, value: any):
        self.code = code
        self.timestamp = timestamp
        self.value = value

class Block:
    def __init__(self, index: int, timestamp: date, data: InputTraceability, previous_hash: str):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(str(self.index).encode('utf-8') +
                   str(self.timestamp).encode('utf-8') +
                   str(self.data).encode('utf-8') +
                   str(self.previous_hash).encode('utf-8'))
        return sha.hexdigest()
    
class Blockchain:
    def __init__(self):
        self.chain = [self.create_generate_block()]

    def create_generate_block(self):
        return Block(0, date.datetime.now(), InputTraceability('GB0000', date.datetime.now(), 'Genesis Block'), '0')
    
    def add_block(self, new_block):
        new_block.previous_hash = self.chain[-1].hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)
    
    def is_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            if (current_block.hash != current_block.calculate_hash() or 
                current_block.previous_hash != previous_block.hash):
                return False
            
            return True

# Input values

current_blockchain = Blockchain()

def get_data():
    return int(input('Deseja inserir um novo registro? \nDigite "1" para continuar e "0" para finalizar o programa: '))

index_count: int = 0
while(get_data() == 1):
    index_count += 1
    input_value = InputTraceability(input('Digite o código de rastreabilidade: '),
                                    date.datetime.now(),
                                    input('Digite o valor da rastreabilidade: '))
            
    current_blockchain.add_block(Block(index_count, 
                                       date.datetime.now(), 
                                       input_value, 
                                       current_blockchain.chain[index_count-1].hash))
    
    print('Valor registrado com sucesso!')
    print(20*'---')

# show values

if (index_count > 0):
    def input_traceability_to_dict(input_traceability: InputTraceability):
        return {
            "code": input_traceability.code,
            "timestamp": input_traceability.timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
            "value": input_traceability.value
        }
    
    def block_to_dict(block: Block):
        return {
            "index": block.index,
            "timestamp": block.timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
            "data": input_traceability_to_dict(block.data),
            "previous_hash": block.previous_hash,
            "hash": block.hash
        }

    def blockchain_to_dict(blockchain: Blockchain):
        return {
            "chain": [block_to_dict(block) for block in blockchain.chain]
        }

    return_blockchain_json = json.dumps(blockchain_to_dict(current_blockchain), indent=4)

    print(return_blockchain_json)

print('Programa Encerrado.')

