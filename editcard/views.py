from django.shortcuts import render
import json
from django.conf import settings
# Create your views here.

# def load():

def initialContext():
    context = dict()
    context['name'] = 'Card Name'
    return context

def getInputs(post):
    inputs = dict()
    inputs['name'] = post['name']
    inputs['type'] = post['type']
    inputs['energy_cost'] = post['energy_cost']
    inputs['damage_target'] = post['damage_target']
    inputs['damage_block_info'] = {
        'damage' : post['damage'],
        'damage_instances' : post['damage_instances'],
        'block' : post['block']
    }
    inputs['card_life_cycle_info'] = {
        'copies_in_discard_pile_when_played' : post['copies_in_discard_pile_when_played'],
        'draw_card' : post['draw_card']
    }
    inputs['buffs_info'] = {
        'Weakened' : {
            'value' : post['Weakened_value'],
            'target' : post['Weakened_target']
        },
        'Vulnerable' : {
            'value' : post['Vulnerable_value'],
            'target' : post['Vulnerable_target']
        },
        'Strength' : {
            'value' : post['Strength_value'],
            'target' : post['Strength_target']
        },
        'Artifact' : {
            'value' : post['Artifact_value'],
            'target' : post['Artifact_target']
        },
        'Thorns' : {
            'value' : post['Thorns_value'],
            'target' : post['Thorns_target']
        },
        'Barricade' : {
            'value' : post['Barricade_value'],
            'target' : post['Barricade_target']
        },
        'Metallicise' : {
            'value' : post['Metallicise_value'],
            'target' : post['Metallicise_target']
        },
        'Plated Armor' : {
            'value' : post['Plated Armor_value'],
            'target' : post['Plated Armor_target']
        },
        'Intangible' : {
            'value' : post['Intangible_value'],
            'target' : post['Intangible_target']
        },
        'Regen' : {
            'value' : post['Regen_value'],
            'target' : post['Regen_target']
        },
        'Frail' : {
            'value' : post['Frail_value'],
            'target' : post['Frail_target']
        },
        'Dexterity' : {
            'value' : post['Dexterity_value'],
            'target' : post['Dexterity_target']
        },
        'Entangled' : {
            'value' : post['Entangled_value'],
            'target' : post['Entangled_target']
        },
        'Flex' : {
            'value' : post['Flex_value'],
            'target' : post['Flex_target']
        },
        'Blur' : {
            'value' : post['Blur_value'],
            'target' : post['Blur_target']
        },
        'DrawReduction' : {
            'value' : post['DrawReduction_value'],
            'target' : post['DrawReduction_target']
        },
        'Minion' : {
            'value' : post['Minion_value'],
            'target' : post['Minion_target']
        },
        'Poison' : {
            'value' : post['Poison_value'],
            'target' : post['Poison_target']
        },
        'Shackled' : {
            'value' : post['Shackled_value'],
            'target' : post['Shackled_target']
        },
    }


    return inputs

def writeToFile(context):
    with open('editcard/cards/test.json', 'w') as f:
        f.write(json.dumps(context))

def home(request):
    return render(request, 'editcard/index.html', {})

def UI(request):

    # # read data
    # # print(settings.BASE_DIR)
    # data = open('editcard/cards/Anger.json').read()
    # jsonData = json.loads(data) #converts to a json structure
    # print(jsonData)
    # print('----')
    # print(jsonData[0]['type'])

    # if get, initial to some card
    if request.method == 'GET':
        context = initialContext()
        return render(request, 'editcard/cardsUI.html', context)

    # if post(submit), get context and write to file
    context = getInputs(request.POST)
    writeToFile(context)

    return render(request, 'editcard/cardsUI.html', context)