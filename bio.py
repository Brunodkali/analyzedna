from Bio.Seq import Seq
import random

# Tabela de propriedades dos aminoácidos
amino_acid_properties = {
    'A': 'hydrophobic', 'C': 'polar', 'D': 'charged', 'E': 'charged',
    'F': 'hydrophobic', 'G': 'polar', 'H': 'charged', 'I': 'hydrophobic',
    'K': 'charged', 'L': 'hydrophobic', 'M': 'hydrophobic', 'N': 'polar',
    'P': 'hydrophobic', 'Q': 'polar', 'R': 'charged', 'S': 'polar',
    'T': 'polar', 'V': 'hydrophobic', 'W': 'hydrophobic', 'Y': 'polar'
}

# Exemplo de sequência de DNA
dna_sequence = Seq("ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG")

# Função para gerar uma mutação simples (substituição de base)
def mutate_sequence(sequence, mutation_rate=0.01, mutation_type='substitution'):
    sequence_list = list(sequence)
    bases = ['A', 'T', 'C', 'G']

    # Escolher tipo de mutação
    if mutation_type == 'substitution':
        for i in range(len(sequence_list)):
            if random.random() < mutation_rate:
                # Escolhe uma base aleatória diferente da original
                original_base = sequence_list[i]
                new_base = random.choice([b for b in bases if b != original_base])
                sequence_list[i] = new_base
                print(f"Mutação (Substituição): {original_base} para {new_base} na posição {i+1}")
    
    elif mutation_type == 'insertion':
        # Escolhe uma posição aleatória para inserir
        if random.random() < mutation_rate:
            insertion_point = random.randint(0, len(sequence_list))
            new_base = random.choice(bases)
            sequence_list.insert(insertion_point, new_base)
            print(f"Mutação (Inserção): {new_base} na posição {insertion_point+1}")
    
    elif mutation_type == 'deletion':
        if random.random() < mutation_rate and len(sequence_list) > 1:
            deletion_point = random.randint(0, len(sequence_list) - 1)
            deleted_base = sequence_list.pop(deletion_point)
            print(f"Mutação (Deleção): {deleted_base} removido da posição {deletion_point+1}")
    
    elif mutation_type == 'duplication':
        if random.random() < mutation_rate and len(sequence_list) > 1:
            dup_start = random.randint(0, len(sequence_list) - 2)
            dup_length = random.randint(1, len(sequence_list) - dup_start - 1)
            dup_segment = sequence_list[dup_start:dup_start + dup_length]
            insert_point = random.randint(0, len(sequence_list))
            sequence_list[insert_point:insert_point] = dup_segment
            print(f"Mutação (Duplicação): Segmento {dup_segment} duplicado e inserido na posição {insert_point+1}")

    return Seq("".join(sequence_list))

def translate_dna(sequence):
    try:
        return sequence.translate()
    except:
        return "Erro na tradução: Tamanho inválido de sequência (não múltiplo de 3)"

# Função para avaliar gravidade da mutação
def evaluate_mutation_impact(original_protein, mutated_protein):
    impact = "silenciosa"
    for i in range(min(len(original_protein), len(mutated_protein))):
        if original_protein[i] != mutated_protein[i]:
            original_property = amino_acid_properties.get(original_protein[i], "unknown")
            mutated_property = amino_acid_properties.get(mutated_protein[i], "unknown")
            if original_property != mutated_property:
                impact = "impactante (substituição não conservativa)"
            else:
                impact = "moderada (substituição conservativa)"
            print(f"Alteração no aminoácido: {original_protein[i]} ({original_property}) "
                  f"para {mutated_protein[i]} ({mutated_property}) na posição {i+1}")
    return impact

# Função para simular condições ambientais
def environmental_effects(base_mutation_rate, environment="normal"):
    if environment == "high_radiation":
        return base_mutation_rate * 2  # Dobra a taxa de mutação
    elif environment == "high_pressure":
        return base_mutation_rate * 0.5  # Reduz a taxa de mutação pela metade
    return base_mutation_rate  # Taxa de mutação normal

# Função para comparar proteínas e analisar o impacto
def analyze_impact(original_dna, mutated_dna):
    original_protein = translate_dna(original_dna)
    mutated_protein = translate_dna(mutated_dna)
    
    print(f"\nProteína Original: {original_protein}")
    print(f"Proteína Mutada: {mutated_protein}")

    impact = evaluate_mutation_impact(original_protein, mutated_protein)
    print(f"Gravidade da mutação: {impact}")

# Função para simular várias gerações com análise de impacto e condições ambientais
def simulate_generations(sequence, generations=10, base_mutation_rate=0.01, environment="normal", mutation_type="substitution"):
    current_sequence = sequence
    for generation in range(generations):
        print(f"\nGeração {generation+1}")

        mutation_rate = environmental_effects(base_mutation_rate, environment)
        mutated_sequence = mutate_sequence(current_sequence, mutation_rate, mutation_type)
        analyze_impact(current_sequence, mutated_sequence)
        current_sequence = mutated_sequence
    return current_sequence

# Simulando 5 gerações com inserções sob alta radiação
simulate_generations(dna_sequence, generations=5, base_mutation_rate=0.05, environment="high_radiation", mutation_type='duplication')

# Simulando 5 gerações com deleções em pressão seletiva alta
# simulate_generations(dna_sequence, generations=5, base_mutation_rate=0.05, environment="high_pressure", mutation_type='deletion')

# Simulando 5 gerações com duplicações no ambiente normal
# simulate_generations(dna_sequence, generations=5, base_mutation_rate=0.05, environment="normal", mutation_type='duplication')