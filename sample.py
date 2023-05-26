import re

from flask import Flask, render_template_string


app = Flask(__name__, static_folder='.', static_url_path='')


def php_to_html(php_code):
    # Regex patterns for PHP statements
    var_string_pattern = r'<\?php\s+\$(\w+)\s+=\s+"(.*?)";\s+\?>'
    var_number_pattern = r'<\?php\s+\$(\w+)\s+=\s+(\d+);\s+\?>'
    array_pattern = r'<\?php\s+\$(\w+)\s+=\s+array\((.*?)\);\s+\?>'
    echo_var_pattern = r'<\?php\s+echo\s+\$(\w+);\s+\?>'
    foreach_pattern = r'<\?php\s+foreach\(\$(\w+)\s+as\s+\$(\w+)\)\s+\{\s+echo\s+\$\w+;\s+\}\s+\?>'
    if_else_pattern = r'<\?php\s+if\(\$(\w+)\s+==\s+"(.*?)"\)\s+\{\s+echo\s+"(.*?)";\s+\}\s+else\s+\{\s+echo\s+"(.*?)";\s+\}\s+\?>'
    function_pattern = r'<\?php\s+function\s+(\w+)\(\)\s+\{\s+echo\s+"(.*?)";\s+\}\s+\?>'
    function_call_pattern = r'<\?php\s+(\w+)\(\);\s+\?>'

    # Store variables and functions in a dict
    vars = {}
    funcs = {}

    # Handle string variables
    for var_name, value in re.findall(var_string_pattern, php_code):
        vars[var_name] = value
        php_code = php_code.replace(f'<?php ${var_name} = "{value}"; ?>', '')

    # Handle number variables
    for var_name, value in re.findall(var_number_pattern, php_code):
        vars[var_name] = int(value)
        php_code = php_code.replace(f'<?php ${var_name} = {value}; ?>', '')

    # Handle arrays
    for var_name, values in re.findall(array_pattern, php_code):
        vars[var_name] = [v.strip(' "') for v in values.split(',')]
        php_code = php_code.replace(f'<?php ${var_name} = array({values}); ?>', '')

    # Handle variable echo statements
    for var_name in re.findall(echo_var_pattern, php_code):
        if var_name in vars:
            php_code = php_code.replace(f'<?php echo ${var_name}; ?>', f'<p>{vars[var_name]}</p>')

    # Handle foreach statements
    for array_name, _ in re.findall(foreach_pattern, php_code):
        if array_name in vars and isinstance(vars[array_name], list):
            foreach_html = ''.join([f'<p>{value}</p>' for value in vars[array_name]])
            php_code = php_code.replace(f'<?php foreach(${array_name} as $value) {{ echo $value; }} ?>', foreach_html)

    # Handle if-else statements
    for var_name, compare_value, if_value, else_value in re.findall(if_else_pattern, php_code):
        if var_name in vars:
            if vars[var_name] == compare_value:
                php_code = php_code.replace(f'<?php if(${var_name} == "{compare_value}") {{ echo "{if_value}"; }} else {{ echo "{else_value}"; }} ?>', f'<p>{if_value}</p>')
            else:
                php_code = php_code.replace(f'<?php if(${var_name} == "{compare_value}") {{ echo "{if_value}"; }} else {{ echo "{else_value}"; }} ?>', f'<p>{else_value}</p>')

    # Handle function definitions
    for func_name, echo_value in re.findall(function_pattern, php_code):
        funcs[func_name] = echo_value
        php_code = php_code.replace(f'<?php function {func_name}() {{ echo "{echo_value}"; }} ?>', '')

    # Handle function calls
    for func_name in re.findall(function_call_pattern, php_code):
        if func_name in funcs:
            php_code = php_code.replace(f'<?php {func_name}(); ?>', f'<p>{funcs[func_name]}</p>')

    return php_code


@app.route('/')
def index():
    html_output = php_to_html(open('index.html', 'r').read())
    return render_template_string(html_output)


if __name__ == '__main__':
    app.run(port=8080, debug=True)
