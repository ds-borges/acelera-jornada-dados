import csv
import json
import statistics
import os

"""
Processamento de dados de funcionários a partir do arquivo 'funcionarios.csv'.

Este script realiza as seguintes tarefas:

1. Lê e valida os dados dos funcionários com base nas regras:
   - Nome não pode estar vazio nem conter números.
   - Área deve estar dentro da lista predefinida.
   - Salário deve ser número positivo ou zero.
   - Bônus percentual deve estar entre 0 e 1 (inclusive).
   
2. Calcula o bônus final para cada funcionário válido seguindo a fórmula:
   bonus_final = 1000 + salario * bonus_percentual

3. Agrupa salários por área e calcula a média salarial por área.

4. Identifica os 3 maiores salários para geração do top 3.

5. Imprime:
   - Lista de funcionários válidos com bônus calculado.
   - Lista de registros inválidos com motivo.
   - KPIs agregados: média salarial por área.
   - Top 3 maiores salários com seus dados completos.

Obs.: Ainda não gera os arquivos CSV ou JSON, mas estrutura os dados para essa finalidade.

Requisitos:
- arquivo "funcionarios.csv" presente no diretório "data/"
- encoding UTF-8 para leitura do arquivo
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
