# Example File
This program converts a text file wich is human readable to a json file.
## Decorations
- "=\=text==" - Highlights the ==text==
- "*\*text**" - Bolds the **text**
- "-\-text--" - Strikeouts the <s>text</s>
- "_\_text__" - Underlines the <u>text</u>

### Input
``` 
#example-text.txt

@g group 1
1: ==q1==
2: **q2**
3: --q3--
4: __q4__

@e enum1
1
2
3

@oe oenum1
1
2
3
```

### Output
```json
{
    "group 1": {
        "mode": 0,
        "items": {
            "==q1==": "1",
            "**q2**": "2",
            "--q3--": "3",
            "__q4__": "4"
        }
    },
    "enum1": {
        "mode": 1,
        "items": [
            "1",
            "2",
            "3"
        ]
    },
    "oenum1": {
        "mode": 2,
        "items": [
            "1",
            "2",
            "3"
        ]
    }
}
```