from ASTLIBRA_config import (
    SUGGESTION_NUMS,
    LEFT_SCALES_NUMS,
    RIGHT_SCALES_NUMS,
    ITEMS_EXCEL_LOCATION,
    score_of_item_id,
    items_wheter_holding,
)

effect_name_of_item_id = {
    "0": "最大體力",
    "1": "精力提升量",
    "2": "效果時間",
    "3": "體力回復量",
    "4": "使用速度",
    "5": "重量減輕",
    "6": "經驗獲取",
    "7": "金錢獲取",
    "8": "攻擊力",
    "9": "防禦力",
    "10": "格擋耐久",
    "11": "異常耐性",
    "12": "適應力",
    "13": "魔導力",
    "14": "最大精力",
    "15": "緩慢回復",
}

score_level_of_id = {
    0: [1, 1.6, 2, 3],          # "最大體力"
    1: [1, 2, 3, 5],            # "精力提升量"
    2: [1, 2, 3, 4.5],          # "效果時間"
    3: [1, 1.5, 2, 2.5],        # "體力回復量"
    4: [1, 1.5, 2, 2.5],        # "使用速度"
    5: [1, 1.5, 2, 2.5],        # "重量減輕"
    6: [1, 2, 3, 4],            # "經驗獲取"
    7: [1, 1.5, 2, 2.5],        # "金錢獲取"
    8: [1, 1.66, 2.66, 6.66],   # "攻擊力"
    9: [1, 1.66, 2.66, 6.66],   # "防禦力"
    10: [1, 1.33, 1.66, 2],     # "格擋耐久"
    11: [1, 1.33, 1.66, 2],     # "異常耐性"
    12: [1, 2, 3, 4],           # "適應力"
    13: [2, 3, 3, 5],           # "魔導力"
    14: [1, 1.5, 2, 3],         # "最大精力"
    15: [1, 1.25, 1.5, 1.75],   # "緩慢回復"
}

item_id_of_effect_name = {
    '取得経験': 6, 
    '攻撃力': 8, 
    'ST上昇量': 1, 
    '適応力': 12, 
    '魔導力': 13, 
    '最大HP': 0, 
    '石化耐性': 11, 
    '麻痺耐性': 11, 
    '防御力': 9, 
    '重量軽減': 5, 
    '最大ST': 14, 
    'HP回復量': 3, 
    '取得金額': 7, 
    '使用速度': 4, 
    'GD耐久力': 10, 
    '出血耐性': 11, 
    '猛毒耐性': 11, 
    '効果時間': 2, 
    '暗闇耐性': 11, 
    '徐々回復': 15
}

item_id_of_power_name = {
    '極': 2,
    '強': 1,
    '普': 0
}

item_2_weight = {}

hold_items = set()
for x in items_wheter_holding:
    if x[2] == 1:
        hold_items.add(x[1])
        hold_items.add(''.join(x[1].split(' ')))

# print(f'{hold_items=}')

import pandas as pd
import copy
from collections import defaultdict, Counter

df = pd.read_excel(ITEMS_EXCEL_LOCATION)
all_items = defaultdict(list)

last_item_name = ''
for row in df.itertuples(index=False):
    if isinstance(row[0], str):
        item_name = row[0]
    else:    
        item_name = last_item_name
    last_item_name = item_name

    for attr in row:
        if isinstance(attr, str) and any(effect == attr or (effect in attr and '[' in attr) for effect in item_id_of_effect_name):
            item_effect = attr.split('[')[0]
            power = attr.split('[')[1].strip(']') if '[' in attr else '普'
            # print(f'{type(item_name)=}, {type(item_effect)=}, {type(power)=}')
            all_items[item_name].append((item_effect, power))
        elif isinstance(attr, int) or (isinstance(attr, str) and attr.isnumeric()):
            item_2_weight[item_name] = int(attr)
    if item_name not in hold_items and item_name in all_items:
        del all_items[item_name]

item_names = list(all_items.keys())


def get_weight_of_combine(combine):
    weight = 0
    for item_name in combine.keys():
        weight += item_2_weight[item_name]

    return weight


def get_score_of_effects(effects):
    score = 0
    for effect in effects:
        score += score_of_item_id[item_id_of_effect_name[effect[0]]] * score_level_of_id[item_id_of_effect_name[effect[0]]][item_id_of_power_name[effect[1]]]
    
    return score

from tqdm import tqdm

def dfs(start_idx, balance_nums, cur, combines):
    if len(cur) == balance_nums:
        weight = get_weight_of_combine(cur)
        combines[weight].append(copy.deepcopy(cur))
        return

    for i in range(start_idx, len(item_names)):
        if start_idx == 0:
            print(f'starting point: {item_names[i]}, {i+1}/{len(item_names)}')
        cur[item_names[i]] = all_items[item_names[i]]
        dfs(i+1, balance_nums, cur, combines)
        del cur[item_names[i]]

left_scale_nums, right_scale_nums = LEFT_SCALES_NUMS, RIGHT_SCALES_NUMS 
left_combines, right_combines = defaultdict(list), defaultdict(list)

dfs(0, left_scale_nums, {}, left_combines)
if right_scale_nums == left_scale_nums:
    right_combines = left_combines
else:
    dfs(0, right_scale_nums, {}, right_combines)



# check total combines
for x in [left_combines, right_combines]:
    total_combines = 0
    for weight, combines in x.items():
        total_combines += len(combines)
    print(f'weight_combines = {len(x)}, {total_combines=}')



import heapq
suggestion_sets = []
suggestion_nums = SUGGESTION_NUMS


for idx, weight in tqdm(enumerate(left_combines.keys()), total=len(left_combines)):
    # print(f'generate suggestion sets: {idx+1}/{len(left_combines.keys())}')
    for left_combine in left_combines[weight]:
        for right_combine in right_combines[weight]:
            combine_effects = Counter()
            left_combine_item_names = set(left_combine.keys())
            right_combine_item_names = set(right_combine.keys())
            score = 0
            for combine in [left_combine, right_combine]:
                for effects in combine.values():
                    combine_effects += Counter(effects)

            unique_effects = set()
            for effect_name, nums in combine_effects.items():
                if nums == 1:
                    unique_effects.add(effect_name)

            score = get_score_of_effects(unique_effects)
            if len(suggestion_sets) == SUGGESTION_NUMS:
                heapq.heappop(suggestion_sets)
            heapq.heappush(suggestion_sets, (score, left_combine_item_names, right_combine_item_names, unique_effects))

print('======== Suggestion genrater finished ========')
print('Suggestions:')
suggestion_sets.sort()
for idx, suggestion_set in enumerate(suggestion_sets):
    print(f'suggestion {idx}:')
    print(f'score: {suggestion_set[0]}, left_items: {suggestion_set[1]}, right_items: {suggestion_set[2]}, all_effects: {suggestion_set[3]}')
    print('------------------------')






