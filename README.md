This is an automation to fix the "Breaking Change: Mixed Declarations" issue:

https://sass-lang.com/documentation/breaking-changes/mixed-decls/

If you see this error on many files, you can try this script.

> Sass's behavior for declarations that appear after nested rules will be changing to match the behavior specified by CSS in an upcoming version. To keep the existing behavior, move the declaration above the nested rule. To opt into the new behavior, wrap the declaration in & {}.

Install dependencies

```
pip3 install pyparser
```

To use on one file
```
python3 run.py NAME_OF_SCSS_FILE
```

To use on a folder
```
python3 run.py NAME_OF_FOLDER
```
