import pprint
import pyparsing as pp

pp.ParserElement.set_default_whitespace_chars('')

def format_nested_list(input_list, indent_level=0):
    result = []
    
    for item in input_list:
        if isinstance(item, list):
            formatted_sublist = format_nested_list(item, indent_level + 1)
            result.append(formatted_sublist)
        else:
            lines = item.split('\n')
            formatted_lines = []
            
            for i, line in enumerate(lines):
                if line.strip():
                    prefix = '\n'
                    suffix = ''
                    formatted_lines.append(f"{prefix}{line}{suffix}")
            result.extend(formatted_lines)
    
    return result

def create_sass_parser():

    pp.ParserElement.set_default_whitespace_chars('')
    content = pp.CharsNotIn('{}').setName('content')
    
    nested = pp.Forward()
    nested << (
        pp.Suppress('{') +
        pp.Group(
            pp.ZeroOrMore(
                nested |
                content
            )
        ) +
        pp.Suppress('}')
    )
    
    return nested

def parse(input_str):
    parser = create_sass_parser()
    try:
        result = parser.parseString("{" + input_str + "}")
        return result.asList()
    except pp.ParseException as e:
        print(f"Parsing failed: {str(e)}")
        return None

if __name__ == "__main__":
    #txt = get_sass("test.sass")
    #txt = "{a b c d}"

    input_str = """selector
{
  a:b;
  c:d;
  selector
  {
    a:b;
    c:d;
  }
  y:z;
}"""

    my_output = parse(input_str)

    expected_output = ["selector\n",["\n  a:b;", "\n  c:d;", "\n  selector\n",["\n    a:b;","\n    c:d;\n"],"\n  y:z;\n"]]

    print("Input: ")
    print(input_str)
    print("Expected Output: ")
    pprint.pp(expected_output)

    my_output = format_nested_list(my_output)

    print("Your output: ")
    pprint.pp(my_output)

    if my_output == expected_output:
        print("test passed!!")
    else:
        print("test failed :{")
