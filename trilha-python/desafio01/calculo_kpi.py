import csv
import json
import statistics
import os

"""
Processamento completo de dados de funcionários a partir do arquivo 'funcionarios.csv'.

Este script realiza:

1. Leitura e validação dos dados de cada funcionário conforme regras:
   - Nome não pode estar vazio nem conter números.
   - Área deve pertencer a uma lista predefinida de áreas válidas.
   - Salário deve ser um número positivo ou zero.
   - Bônus percentual deve ser número entre 0 e 1 (inclusive).

2. Cálculo do bônus final para cada funcionário válido usando a fórmula:
   bonus_calculado = 1000 + salario * bonus_percentual

3. Agrupamento dos salários por área e cálculo da média salarial de cada área.

4. Identificação dos 3 maiores salários para formar o top 3.

5. Armazenamento dos dados:
   - Geração de 'relatorio_individual.csv' contendo funcionários válidos com bônus calculado.
   - Geração de 'erros.csv' com registros inválidos e motivo do erro.
   - Geração de 'kpis.json' com KPIs agregados, contendo:
     * salários por área,
     * média salarial por área,
     * total geral de bônus pagos,
     * top 3 funcionários com maiores salários.

6. Preparação do ambiente para criação dos arquivos, verificando/criando diretório 'output'.

Requisitos:
- Arquivo 'funcionarios.csv' deve estar no diretório 'data/'.
- Codificação UTF-8 para leitura e escrita dos arquivos.
- Python 3.x com módulos padrão csv, json, statistics e os.

Esse código oferece um fluxo completo para validar, processar e gerar relatórios confiáveis e organizados para análise de recursos humanos.
"""

file_path="data/funcionarios.csv"

with open(file_path, newline='', encoding='utf-8') as csvfile:
    employee_dict = csv.DictReader(csvfile)

    required_areas = ['Vendas', 'TI', 'Financeiro', 'RH', 'Operações']
    valid_employees = []
    invalid_employees  = []
    salaries_by_area = {}
    average_salary_by_area = {}
    top_salaries = []
    bonus_total = 0
    kpis_data = {}

    try:
        for usuario in employee_dict:
            
            is_valido=True

            #O trabalhador esta sem nome registrado
            if "nome" not in usuario or not usuario["nome"]:
                is_valido = False
                usuario['Erros'] = "Nome não registrado"
                invalid_employees .append(usuario)
            
            #O trabalhador tem numeros no nome
            if any(c.isdigit() for c in usuario["nome"]):
                is_valido = False
                usuario['Erros'] = "Nome registrado com números"
                invalid_employees .append(usuario)

            #A area do funcionario esta errada
            if usuario["area"] not in required_areas:
                is_valido = False
                usuario['Erros'] = "Função registrada incorretamente"
                invalid_employees .append(usuario)

            #O salario esta negativo
            if float(usuario["salario"]) < 0:
                is_valido = False
                usuario['Erros'] = "Salário registrado errado"
                invalid_employees .append(usuario)
            
            #Não tem letras mas o bonus está errado        
            if not any(c.isalpha() for c in usuario["bonus_percentual"]):    
                bonus = float(usuario["bonus_percentual"])
                if not (0 <= bonus <= 1):
                    is_valido = False
                    usuario['Erros'] = "Bonus registrado negativo"
                    invalid_employees .append(usuario)
                
            #Tem letras no bonus
            else: 
                is_valido = False
                usuario['Erros'] = "Bonus está registrado com letras"
                invalid_employees .append(usuario)

            if is_valido:
                #Criar uma lista com os usuários que estão corretos
                valid_employees.append(usuario)


                #Criar uma lista com os salarios agrupadas
                if usuario['area'] not in salaries_by_area:
                    salaries_by_area[usuario['area']] = []
                salaries_by_area[usuario['area']].append(float(usuario['salario']))

                #Identificar os maiores salarios
                if len(top_salaries) < 3 :
                    top_salaries.append(usuario)
                else:
                    # Só insere se o novo usuário tiver salário maior que o menor do top_salaries
                    if float(usuario['salario']) > float(top_salaries[-1]['salario']):
                        top_salaries.append(usuario)
                        top_salaries = sorted(top_salaries, key=lambda x: float(x['salario']), reverse=True) #Ordena os salarios do maior para o menor
                        top_salaries = top_salaries[:3]     #Manter a lista com 3 posições
                                                        
    except (ValueError, IndexError, KeyError, TypeError) as e:
            print(f"\nErros: Verifique o formato da sua entrada. Detalhes: {e}")

# print("\nTrabalhadores com registros corretos\n")
with open('output/relatorio_individual.csv', mode='w', newline='', encoding='utf-8') as file:
    fieldnames = ['id', 'nome', 'area', 'salario', 'bonus_percentual', 'bonus_calculado']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for usuario in valid_employees:
        usuario['bonus_calculado'] = 1000 + (float(usuario['salario']) * float(usuario['bonus_percentual']))
        writer.writerow(usuario)
        #Calcular o bonus geral
        bonus_total=bonus_total+float(usuario['bonus_calculado'])

# os.makedirs('output', exist_ok=True)

# print("\n\nTrabalhadores com problemas nos registros\n")
with open('output/erros.csv', mode='w', newline='', encoding='utf-8') as file:
    fieldnames = ['id', 'nome', 'area', 'salario', 'bonus_percentual', 'Erros']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for usuario in invalid_employees:
        writer.writerow(usuario)

# print("\n\nKPIs\n")
# print(salaries_by_area)
kpis_data['salarios_por_area']=salaries_by_area

# print("\n\nMedia salarial de cada area\n")
for area in required_areas:
    if area in salaries_by_area:
        average_salary_by_area[area] = statistics.mean(salaries_by_area[area])
kpis_data['media_salarial_por_area'] = average_salary_by_area

kpis_data['bonus_total_geral']=bonus_total

# print("\n\nAltos salarios\n")
kpis_data['top_salarios'] = top_salaries

with open('output/kpis.json', mode='w', encoding='utf-8') as file:
    json.dump(kpis_data, file, ensure_ascii=False, indent=4)
