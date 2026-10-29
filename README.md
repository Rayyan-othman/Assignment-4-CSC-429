# Laptop Advisor Expert System - CSC Assignment 4

This project completes the professor's Python starter files and implements all 10 IF-THEN rules from Assignment 4_rules.docx.

## Requirements
Python 3.8 or later; no external Python packages needed.

## Run
From the project directory:

```bash
python main.py
```

Answer the budget, yes/no, and operating-system questions. The program displays matching laptop recommendations, suggested specifications, and the rules that produced each result.

## Test
```bash
python -m unittest discover -s tests -v
```

## How inference works
`assert_facts` stores the user's responses. `can_fire` checks whether every condition of a rule is present and its conclusion is not already known. `run` selects the highest-priority eligible rule, adds its conclusion, records an explanation, and repeats until no more rules can fire. `conclusions` separates recommendations, specifications, and other facts. Priority ties preserve the original JSON order.

The 10 rules are located in `kb/laptop_rules.json`. `kb_loader.py` is retained from the starter project. See `Project_Report.pdf` for a short explanation and test summary.
