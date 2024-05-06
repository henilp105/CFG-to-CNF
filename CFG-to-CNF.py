import copy
from itertools import combinations
import re
import streamlit as st


def addAndSymbol(input_list):
    operators = ['|','>','-','.']
    for rule in range(len(input_list)):
        rules = list(input_list[rule])
        insert_offset = 0
        for i in range(1, len(input_list[rule])):
            if input_list[rule][i] not in operators and input_list[rule][i-1] not in operators:
                a = rules[i]
                b = rules[i-1]
                rules.insert(i + insert_offset,'.')
                insert_offset += 1
        input_list[rule] = ''.join(rules)
    return input_list

def stringListToCFG(input_list):
    input_list = addAndSymbol(input_list)
    input_list = [x.split('->') for x in input_list]
    input_list = [{x[0]:set(x[1].split('|'))} for x in input_list]
    return input_list

def remove_indices(string_, to_remove):
    positions_toremove = []
    for j in range(len(string_)):
        if string_[j] == to_remove:
            positions_toremove.append(j)
    indecies = []
    for j in range(1, len(positions_toremove) + 1):
        indecies.extend(list(combinations(positions_toremove, r=j)))
    return indecies   

def generate_combinations(string_, indecies):
    temp_str = set()
    c = list(string_)
    for i in indecies:
        x = c.copy()
        for j in i:
            x[j] = ''
        added = ''.join(x)
        if len(added) == 0:
            temp_str.add('ε') 
        else:
            temp_str.add(added) 
    return temp_str   

def no_null(CFG, start):
    for key, values in CFG.items():
        if "ε" in values and key != start:
            return False
    return True

def remove_null_production(CFG, start):
    while not no_null(CFG, start):
        for key, values in CFG.items():
            if "ε" in values and key != start:
                CFG[key].remove('ε')
                for keys2, values2 in CFG.items():
                    for j in values2: 
                        if key in ''.join(list(j)):   
                            CFG[keys2] = CFG[keys2].union(generate_combinations(j,remove_indices(j,key)))
                CFGcopy = copy.deepcopy(CFG)
                for i in CFGcopy:
                    for j in CFGcopy[i]:
                        CFG[i].add(j.replace('..', '.'))
                        if (j != j.replace('..', '.')):
                            CFG[i].remove(j)
                            j = j.replace('..', '.')
                        if (j[0] == '.' or j[-1] == '.'):
                            CFG[i].add(j.strip('.'))
                            CFG[i].remove(j)
    return CFG

def contain_nonterminal(set_value):
    set_of_nonterminals = set()
    for i in set_value:
        if len(i) == 1 and i.isupper():
            set_of_nonterminals.add(i)
    return set_of_nonterminals

def done(CFG):
    for k, v in CFG.items():
        if len(contain_nonterminal(v)) != 0:
            return False
    return True

def remove_unit_production(CFG):
    while not done(CFG):
        for primary_key, set_value in CFG.items():
            set_non_terminals = contain_nonterminal(set_value)
            if len(set_non_terminals) != 0:
                for i in set_non_terminals:
                    CFG[primary_key].remove(i)
                    CFG[primary_key] =  CFG[primary_key].union(CFG[i])
                    if i == primary_key and i in CFG[primary_key]:
                        CFG[primary_key].remove(i)
    return CFG

def eliminateUselessProd(cfg, start):
    testCopy = copy.deepcopy(cfg)
    non_generating = set()
    for i in cfg[start]:
        for j in i:
            if (j not in cfg.keys() and j.isupper()): 
                non_generating.add(j)
                continue
            if ((j.isupper()) and ('' not in cfg[j]) and (len(cfg[j]) == 1)):
                for k in str(cfg[j]):
                    if k.isupper():
                        non_generating.add(j)
    for i in testCopy[start]:
        for j in i:
            if ((j in non_generating)):    
                cfg[start].remove(i)
    for i in non_generating:
        del cfg[i]              
    reachable = {}
    non_reachable = {}
    for i in cfg[start]:
        for j in i:
            if (j.isupper()):
                reachable[j] = cfg[j]   
    for i in cfg.keys():
        if ((i not in reachable.keys()) and i != start):
            non_reachable[i] = cfg[i]        
    for i in testCopy:
        if i in non_reachable:
            del cfg[i]            
    return cfg

def ReduceStringToEvens(rule, originalInput, currentDict, currentCounter):
    output = {}
    if rule.count('.') == 1:
        return rule, {}, currentCounter
    splitString = rule.split('.')
    if (len(splitString) % 2 == 1):
        evenRule = None
        firstTwoLiterals = rule[:rule.index('.', rule.index('.') + 1)]
        if {firstTwoLiterals} in originalInput.values():
            newRuleKey = list(originalInput.keys())[list(originalInput.values()).index({firstTwoLiterals})]
            evenRule = rule.replace(firstTwoLiterals, newRuleKey)
        elif {firstTwoLiterals} not in currentDict.values():
            newRuleKey = f'K{currentCounter}'
            currentCounter += 1
            newRuleValue = firstTwoLiterals
            output[newRuleKey] = {newRuleValue}
            evenRule = rule.replace(firstTwoLiterals, newRuleKey)
        else: 
            newRuleKey = list(currentDict.keys())[list(currentDict.values()).index({firstTwoLiterals})]
            evenRule = rule.replace(firstTwoLiterals, newRuleKey)
    else:
        evenRule = rule
    currentDict.update(output)
    if len(evenRule.split('.')) > 2:
        left = '.'.join(splitString[:len(splitString) // 2])
        right = '.'.join(splitString[len(splitString) // 2:])
        leftSet = {left}
        if leftSet in originalInput.values():
            leftKey = list(originalInput.keys())[list(originalInput.values()).index(leftSet)]
        elif leftSet in output.values():
            leftKey = list(output.keys())[list(output.values()).index(leftSet)]
        elif leftSet not in currentDict.values():
            leftKey = currentCounter
            currentCounter += 1
            leftKey = f'K{leftKey}'
        else:
            leftKey = list(currentDict.keys())[list(currentDict.values()).index({left})]
        splitStringLeft = ReduceStringToEvens(left, originalInput, currentDict, currentCounter)
        currentCounter = splitStringLeft[2]
        output.update(splitStringLeft[1])
        output[f'{leftKey}'] = {splitStringLeft[0]}
        rightSet = {right}
        if rightSet in originalInput.values():
            rightKey = list(originalInput.keys())[list(originalInput.values()).index(rightSet)]
        elif rightSet in output.values():
            rightKey = list(output.keys())[list(output.values()).index(rightSet)]
        elif rightSet not in currentDict.values():
            rightKey = currentCounter
            currentCounter += 1
            rightKey = f'K{rightKey}'
        else:
            rightKey = list(currentDict.keys())[list(currentDict.values()).index({left})]
        splitStringRight = ReduceStringToEvens(right, originalInput, currentDict, currentCounter)
        output[f'{rightKey}'] = {splitStringRight[0]}
        currentCounter = splitStringRight[2]
        output.update(splitStringRight[1])
        evenRule = f'{leftKey}.{rightKey}'
    return evenRule, output, currentCounter 

def ToCNF(input_dict):
    output = {}
    newRuleCounter = 0
    for k, v in input_dict.items():
        FinalValue = set()
        for rule in v:
            if len(rule) > 1:
                elements = rule.split('.')
                for i in range(len(elements)):
                    if(elements[i].islower()):
                        if {elements[i]} in input_dict.values():
                            newRuleKey = list(input_dict.keys())[list(input_dict.values()).index({elements[i]})]
                            elements[i] = newRuleKey
                        elif {elements[i]} not in output.values():
                            newRuleKey = f'K{newRuleCounter}'
                            newRuleCounter += 1
                            newRuleValue = elements[i]
                            output[newRuleKey] = {newRuleValue}
                            elements[i] = newRuleKey
                        else: 
                            newRuleKey = list(output.keys())[list(output.values()).index({elements[i]})]
                            elements[i] = newRuleKey
                rule = '.'.join(elements)
            if len(rule.split('.')) <= 2:
                FinalValue.add(rule)
                continue
            final = ReduceStringToEvens(rule, input_dict, output, newRuleCounter)
            newRuleCounter = final[2]
            output.update(final[1])
            evenRule = final[0]
            FinalValue.add(evenRule)
        output[k] = FinalValue
    sortedOutput = {}
    for k in input_dict.keys():
        sortedOutput[k] = output[k]
    sortedOutput.update(output)
    return sortedOutput
    
def format_dict(my_dict):
        formatted_dict = {}
        for key, values in my_dict.items():
            formatted_values = ' | '.join(sorted(values))
            formatted_dict[key] = ' -> '.join([key, formatted_values])
        return formatted_dict

def main():
    st.title('CFG to CNF converter')
    num_rules = st.number_input("Enter the number of production rules:", min_value=1, value=3)

    test = []
    for i in range(num_rules):
        rule = st.text_input(f"Enter production rule {i + 1}:")
        test.append(rule)

    if st.button("Convert"):
        st.write("Converting......")
        new_start = 'N->'+test[0][0]
        new_test = [None] * (len(test) + 1)
        new_test[0] = new_start
        new_test[1:] = test
        CFG = stringListToCFG(new_test)
        CFG_dict = {}
        for i in range(0, len(CFG)):
            CFG_dict.update(CFG[i])
        CFG = remove_null_production(CFG_dict, new_start[0])
        CFG = remove_unit_production(CFG)
        CFG = eliminateUselessProd(CFG, new_start[0])
        formatted_dict = format_dict(ToCNF(CFG))
        # st.title("Formatted Dictionary")
        for key, value in formatted_dict.items():
            st.write(value)



if _name_ == "_main_":
    main()