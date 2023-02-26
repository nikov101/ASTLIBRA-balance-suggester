# ASTLIBRA balance suggester
### Configuration
Setup following configs in ASTLIBRA_config.py
1. SUGGESTION_NUMS
    1. Output nums of items set suggestion
2. LEFT_SCALES_NUMS
    1. The scale nums of left side balance
3. RIGHT_SCALES_NUMS
    1. The scale nums of right side balance
4. ITEMS_EXCEL_LOCATION
    1. the location of ASTLIBRA_items.xlsx
5. score_of_item_id
    1. The weights of score of each effect
6. items_wheter_holding
    1. The record of whether you have the item
    2. (weight, item_name, YES/NO)

### Usage
```bash
cd {the location of this REPO}
python3 -m pip install -r .\requirements.txt
python3 .\ASTLIBRA_balance_suggester.py
```

### Development Environment
Windows 11
