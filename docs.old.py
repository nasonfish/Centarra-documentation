#!/usr/bin/env python

# A program to read views files in order to automatically document the API pages.

import re
import subprocess

each = re.compile(r"(?s)(\r?\n|^)@.*?\r?\n {4}.*?(\r?\n(?=@)|$)")

parse_one = re.compile(r"""^$|^(?:@(?P<module_name>[a-z]*)\.route\('(?P<route>[^']+)'\)|(?P<login_required>@login_required)|def (?P<function_name>[a-z_]+)\((?P<func_def_args>[^)]*)\):)$|^ {4}(?:(?:(?P<definition>[a-z_A-Z]) ?= ?(?:.*?\.query\.(.*?)\.(?P<query_method>first|all|first_or_404)\(\))|request\.form(\.get\(['"](?P<safe_post_get>[^'"]*)['"](?:, ['"](?P<default_post_get>[^'"])['"]?\))|\[['"](?P<post_get>[^'"]*)['"]\])|(?:(?P<return>return) (?:(?P<any_resp>render_template_or_json)\("[^]+"(?P<list_passed>, [^ ]+)*\)|(?P<redirect>redirect)\(url_for\(['"](?P<url_str>[^'"]+)['"].*\)\)))|.*)$""")

l = subprocess.check_output(["find", "-name", "views.py"]).split('\n')
for file in l:
    if file == "":
        continue
    with open(file, "r") as f:
        data = f.read()
    for view in each.finditer(data):
        view = view.group(0)
        if "@admin_required" in view or "@require_permission" in view:
            continue
        # I think reading it line-by-line will work, so we can capture all of the if statements and display them, to an extent.
        for line in view.split("\n"):
            print line
            match = parse_one.match(line)
            print(match.groups())
