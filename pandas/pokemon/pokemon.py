import pandas as pd

df = pd.read_csv('pokemon.csv', usecols=['Number', 'Name', 'Type_1', 'Type_2', 'Generation', 'Height_m'])

## =============================================
## QUANTOS TIPOS DIFERENTES DE POKEMONS EXISTEM?
## =============================================

#   Agrupa todos os elementos das colunas selecionados do dataframe em um único array usando "values.ravel"
#   e remove os elementos repetentes usando "pd.unique"
uniques = pd.unique(df[['Type_1', 'Type_2']].values.ravel())
#   Removendo o tipo NaN
df_uniques = pd.DataFrame(uniques).dropna()
#   Contando o número de elementos
differentPokemonTypesCount = df_uniques.shape[0]

print('Tipos de pokemons diferentes:', differentPokemonTypesCount)

## ===============================================
## QUAL GERAÇÃO POSSUI MAIS POKEMONS DO TIPO FIRE?
## ===============================================

#   Filtrando todos os pokemnos que possuem tipo 1 ou tipo 2 o valor Fire
df_filtered = df[(df['Type_1']=='Fire')|(df['Type_2']=='Fire')]

#   Contando valores baseado na 'Generation' usando value_counts e pegando o id da geração com maior valor em idxmax
#   value_counts é um método de dataframes que retorna um tipo "Series" 
mostFireGeneration = df_filtered.Generation.value_counts(sort=True).idxmax()

print('A geração com mais pokemons de fogo é a de número', mostFireGeneration)

## ===============================================
## QUAL AS COMBINAÇÕES TIPO_1 E TIPO_2 MAIS RARAS?
## ===============================================

#   Agrupa os pokemons por combinação "Typo_1" e "Typo_2" e retorna um novo dataframe com coluna "count"
df_grouped_types = df.groupby(['Type_1', 'Type_2']).size().reset_index().rename(columns={0:'count'})

#   Filtra o dataframe pelos menores valores de coluna "count"
df_most_rare_combinations = df_grouped_types[ df_grouped_types['count'] == df_grouped_types['count'].min()]

#   Remove a coluna count pois não é mais necessária
df_most_rare_combinations = df_most_rare_combinations.drop(columns=['count'])

#   Detecta as combinações que, invertendo, são as mesmas (Ex: Water e Fire é a mesma coisa que Fire e Water)
#   e cria um dataframe com o resultado das combinações "repetentes"
df_repeating_types = pd.DataFrame(columns=['Type_1', 'Type_2'])
for type_1, type_2 in zip(df_most_rare_combinations['Type_1'], df_most_rare_combinations['Type_2']):
    # Verifica se essa iteração atual invertida já foi adicionada de forma invertida (para não acabar removendo as duas combinações)
    alreadyAddedIteration = df_repeating_types[(df_repeating_types['Type_1']==type_2) & (df_repeating_types['Type_2']==type_1)].shape[0] > 0
    if not alreadyAddedIteration:
        # Checa se essa iteração atual invertida repete no dataframe original
        df_filtered_combinations = df_most_rare_combinations[df_most_rare_combinations['Type_2']==type_1]
        for filtered_type_1 in df_filtered_combinations['Type_1']:
            if type_2 == filtered_type_1:
                df_repeating_types = df_repeating_types.append({'Type_1': type_1, 'Type_2': type_2}, ignore_index=True)

#   Retira os elementos "repetentes" encontrados do dataframe original e coloca os nomes dos pokemons
keys = list(df_repeating_types.columns.values)
i1 = df_most_rare_combinations.set_index(keys).index
i2 = df_repeating_types.set_index(keys).index
df_most_rare_combinations = df_most_rare_combinations[~i1.isin(i2)]
df_complete_list_with_names = pd.merge(df, df_most_rare_combinations, left_on=['Type_1','Type_2'], right_on = ['Type_1','Type_2']).set_index('Number')
count_most_rare_combinations = df_most_rare_combinations.shape[0]
# print('Existem no total', count_most_rare_combinations, 'combinações de tipos que são únicas, então não foi possível selecionar apenas 3. Elas são:')
# print(df_complete_list_with_names)


print(df.Height_m.describe())

# RASCUNHO

# types = df.groupby('Type_1')

# print(types.groups)

# for Name, HP in types:
#     print(Name)

# print(types.get_group('Flying'))


# CONTA FREQUENCIA DE CADA COLUNA
# print(df.apply(pd.Series.value_counts, axis=0))

# LISTA COMBINAÇÃO ÚNICA DE TIPO_1 e TIPO_2
# grouped = df.groupby(['Type_1', 'Type_2']).size().reset_index().rename(columns={0:'count'})

