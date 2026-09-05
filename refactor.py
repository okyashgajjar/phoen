import os
import glob
import re

files = glob.glob('src/components/*.jsx')
for f in files:
    with open(f, 'r') as file:
        content = file.read()
    
    if 'setActiveTab' in content:
        # Replace the prop setActiveTab
        content = re.sub(r'\{\s*setActiveTab(?:,\s*[^}]+)?\s*\}', lambda m: m.group(0).replace('setActiveTab,', '').replace(', setActiveTab', '').replace('setActiveTab', ''), content)
        # Clean up empty destructurings like {}
        content = re.sub(r'function \w+\(\{\s*\}\)', lambda m: m.group(0).replace('{}', ''), content)
        
        # We need to import useNavigate
        if 'useNavigate' not in content:
            if "from 'react-router-dom'" in content:
                content = content.replace("from 'react-router-dom'", ", useNavigate } from 'react-router-dom'")
            else:
                content = content.replace("import React", "import React\nimport { useNavigate } from 'react-router-dom'")
        
        # We need to initialize navigate
        # Find the component definition and insert const navigate = useNavigate();
        # Looking for export default function ComponentName(...) {
        content = re.sub(r'(export default function \w+\([^)]*\)\s*\{)', r'\1\n  const navigate = useNavigate();\n', content)
        
        # Replace setActiveTab('...') with navigate('/...')
        content = re.sub(r'setActiveTab\(([^)]+)\)', r"navigate('/' + \1)", content)
        
        # Fix quotes if it becomes navigate('/' + 'approvals') -> navigate('/approvals')
        content = re.sub(r"navigate\('/' \+ '([^']+)'\)", r"navigate('/\1')", content)
        
        with open(f, 'w') as file:
            file.write(content)
